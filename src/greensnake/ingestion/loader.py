"""Load validated research batches into elite_graph.sqlite.

Nothing reaches the database without passing core.schema validation first.
Records that fail are written to data/processed/ingest_rejects.jsonl with the
reason -- they are never coerced into valid ones.

Determinism: every id is a hash of the record's natural key, so re-running the
pipeline on the same batches produces byte-identical ids.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import yaml

from ..core.enums import (
    BROAD_TYPES, CONFIRMED_STATUSES, CORRELATION_STRENGTH_DEFAULT,
    RELATIONSHIP_WEIGHT, STATUS_WEIGHT, STRICT_TYPES,
)
from ..core.schema import validate_record
from ..entity_resolution.dedupe import AliasMap, CompanyResolver, tight_key

BATCH_FILES = {
    "people": "people.jsonl",
    "companies": "companies.jsonl",
    "edges": "edges.jsonl",
    "valuations": "valuations.jsonl",
    "correlations": "correlations.jsonl",
    "rejected": "rejected.jsonl",
    "queue": "queue.jsonl",
}

SHORT_SCORE_KEYS = {
    "access": "access_score",
    "technical": "technical_intelligence_score",
    "early_stage": "early_stage_track_record",
    "network": "founder_network_score",
    "capital": "capital_flexibility",
    "independence": "independence_score",
}


def _hash(*parts: Any) -> str:
    h = hashlib.sha1("||".join("" if p is None else str(p) for p in parts).encode())
    return h.hexdigest()[:16]


def read_jsonl(path: Path) -> Iterable[tuple[int, dict]]:
    if not path.exists():
        return
    for i, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        try:
            yield i, json.loads(line)
        except json.JSONDecodeError:
            yield i, {"__parse_error__": line[:200]}


def overlap_class(rel_type: str) -> str:
    if rel_type in STRICT_TYPES:
        return "STRICT"
    if rel_type in BROAD_TYPES:
        return "BROAD"
    return "INFO_NETWORK"


def edge_weight(rel_type: str, status: str) -> float:
    return RELATIONSHIP_WEIGHT.get(rel_type, 0.0) * STATUS_WEIGHT.get(status, 0.0)


class Ingestor:
    def __init__(self, con, alias_map_path: str | Path, reject_log: Path):
        self.con = con
        self.resolver = CompanyResolver(AliasMap(alias_map_path))
        self.reject_log = Path(reject_log)
        self.reject_log.parent.mkdir(parents=True, exist_ok=True)
        self.rejects: list[dict] = []
        self.stats: dict[str, int] = {}
        self._known_people: set[str] = set()
        self._company_rows: dict[str, dict] = {}
        self._pending_orphan_people: set[str] = set()

    # ---------------------------------------------------------------- utils
    def _bump(self, k: str, n: int = 1) -> None:
        self.stats[k] = self.stats.get(k, 0) + n

    def _reject(self, kind: str, source: str, lineno: int, rec: dict, msgs: list[str]) -> None:
        self.rejects.append({"kind": kind, "file": source, "line": lineno,
                             "errors": msgs, "record": rec})
        self._bump(f"rejected_{kind}")

    def resolve_company(self, raw_name: str, agent: str) -> str:
        """Resolve a raw name to a company_id AND guarantee the row exists.

        Edges and valuations carry foreign keys to companies, so the stub must
        be written the moment an id is minted; finalise_companies() later fills
        in whatever detail the agents supplied.
        """
        cid = self.resolver.resolve(raw_name, resolved_by=agent)
        self.con.execute(
            "INSERT OR IGNORE INTO companies (company_id, canonical_name, public_or_private,"
            " current_status, added_by, date_added) VALUES (?,?,'UNKNOWN','UNKNOWN',?,?)",
            (cid, self.resolver.canonical_name(cid), agent, date.today().isoformat()))
        return cid

    def _put_sources(self, parent_kind: str, parent_id: str, sources: list[dict]) -> None:
        for s in sources:
            sid = _hash(parent_kind, parent_id, s.get("url"), s.get("source_type"))
            self.con.execute(
                "INSERT OR REPLACE INTO sources (source_id, parent_kind, parent_id, url, "
                "source_type, tier, publisher, published_date, accessed_date, evidence_summary) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (sid, parent_kind, parent_id, s["url"], s["source_type"], s["tier"],
                 s.get("publisher") or s.get("title"), s.get("published_date"),
                 s.get("accessed_date"), s["evidence_summary"]))
            self._bump("sources")

    # ------------------------------------------------------------- universe
    def load_people_universe(self, path: str | Path) -> None:
        doc = yaml.safe_load(Path(path).read_text())
        for p in doc["people"]:
            scores = {SHORT_SCORE_KEYS[k]: v for k, v in (p.get("scores") or {}).items()
                      if k in SHORT_SCORE_KEYS}
            rec = {"person_key": p["key"], "full_name": p["name"],
                   "signal_class": p["signal_class"], "archetypes": p.get("archetypes"),
                   "domains": p.get("domains"), "rationale": p["rationale"],
                   "scores": {k: v for k, v in scores.items() if v is not None}}
            errs = validate_record(rec, "person")
            # a null early_stage_track_record is legitimate ("no record to judge")
            errs = [e for e in errs if "early_stage_track_record" not in e
                    or scores.get("early_stage_track_record") is not None]
            if errs:
                self._reject("person", str(path), 0, rec, errs)
                continue
            self.con.execute(
                "INSERT OR REPLACE INTO people (person_key, full_name, signal_class, archetypes,"
                " domains, primary_affiliation, country, rationale, added_by, date_added)"
                " VALUES (?,?,?,?,?,?,?,?,?,?)",
                (p["key"], p["name"], p["signal_class"], json.dumps(p.get("archetypes") or []),
                 json.dumps(p.get("domains") or []), p.get("affiliation"), p.get("country"),
                 p["rationale"], "orchestrator", doc.get("compiled")))
            self.con.execute(
                "INSERT OR REPLACE INTO people_scores (person_key, access_score,"
                " technical_intelligence_score, early_stage_track_record, founder_network_score,"
                " capital_flexibility, independence_score, score_method_version, rationale)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                (p["key"], scores.get("access_score"), scores.get("technical_intelligence_score"),
                 scores.get("early_stage_track_record"), scores.get("founder_network_score"),
                 scores.get("capital_flexibility"), scores.get("independence_score"),
                 doc.get("method_version"), p["rationale"]))
            self._known_people.add(p["key"])
            self._bump("people_universe")
        self.con.commit()

    # --------------------------------------------------------------- batches
    def load_batch(self, batch_dir: Path) -> None:
        agent = batch_dir.name
        # people first so edges can reference them
        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["people"]):
            if "__parse_error__" in rec:
                self._reject("person", agent, lineno, rec, ["unparseable JSON"]); continue
            errs = validate_record(rec, "person")
            if errs:
                self._reject("person", agent, lineno, rec, errs); continue
            if rec["person_key"] in self._known_people:
                continue
            sc = rec.get("scores") or {}
            self.con.execute(
                "INSERT OR REPLACE INTO people (person_key, full_name, signal_class, archetypes,"
                " domains, primary_affiliation, country, rationale, added_by, date_added)"
                " VALUES (?,?,?,?,?,?,?,?,?,?)",
                (rec["person_key"], rec["full_name"], rec["signal_class"],
                 json.dumps(rec.get("archetypes") or []), json.dumps(rec.get("domains") or []),
                 rec.get("affiliation"), rec.get("country"), rec["rationale"], agent,
                 date.today().isoformat()))
            self.con.execute(
                "INSERT OR REPLACE INTO people_scores (person_key, access_score,"
                " technical_intelligence_score, early_stage_track_record, founder_network_score,"
                " capital_flexibility, independence_score, score_method_version, rationale)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                (rec["person_key"], sc.get("access_score"), sc.get("technical_intelligence_score"),
                 sc.get("early_stage_track_record"), sc.get("founder_network_score"),
                 sc.get("capital_flexibility"), sc.get("independence_score"),
                 "agent-asserted", rec["rationale"]))
            self._known_people.add(rec["person_key"])
            self._bump("people_added_by_agents")

        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["companies"]):
            if "__parse_error__" in rec:
                self._reject("company", agent, lineno, rec, ["unparseable JSON"]); continue
            errs = validate_record(rec, "company")
            if errs:
                self._reject("company", agent, lineno, rec, errs); continue
            cid = self.resolve_company(rec["canonical_name"], agent)
            for a in (rec.get("aliases") or []) + (rec.get("former_names") or []):
                self.resolver._raw_seen[a] = cid
                self.resolver._by_tight.setdefault(tight_key(a), cid)
            prev = self._company_rows.get(cid, {})
            merged = {**prev}
            for k, v in rec.items():
                if v not in (None, [], "") and (k not in merged or merged.get(k) in (None, [], "")):
                    merged[k] = v
            merged.setdefault("_agents", [])
            if agent not in merged["_agents"]:
                merged["_agents"] = merged["_agents"] + [agent]
            self._company_rows[cid] = merged
            self._bump("company_records")

        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["edges"]):
            if "__parse_error__" in rec:
                self._reject("edge", agent, lineno, rec, ["unparseable JSON"]); continue
            errs = validate_record(rec, "edge")
            if errs:
                self._reject("edge", agent, lineno, rec, errs); continue
            if rec["person_key"] not in self._known_people:
                self._reject("edge", agent, lineno, rec,
                             [f"person_key {rec['person_key']!r} is not in the people universe "
                              f"and was not declared in people.jsonl"])
                self._pending_orphan_people.add(rec["person_key"])
                continue
            cid = self.resolve_company(rec["company_name"], agent)
            eid = _hash(rec["person_key"], cid, rec["relationship_type"],
                        rec.get("investment_date"), rec.get("round_name"))
            st = rec["verification_status"]
            self.con.execute(
                "INSERT OR REPLACE INTO person_company_edges (edge_id, person_key, company_id,"
                " relationship_type, investment_vehicle, investment_date, round_name,"
                " amount_personally_invested_usd, round_total_usd, entry_valuation_usd,"
                " entry_valuation_type, ownership_percentage, verification_status,"
                " verification_notes, date_verified, collected_by, raw_company_name,"
                " is_confirmed, overlap_class, edge_weight)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (eid, rec["person_key"], cid, rec["relationship_type"],
                 rec.get("investment_vehicle"), rec.get("investment_date"), rec.get("round_name"),
                 rec.get("amount_personally_invested_usd"), rec.get("round_total_usd"),
                 rec.get("entry_valuation_usd"), rec.get("entry_valuation_type"),
                 rec.get("ownership_percentage"), st, rec.get("verification_notes"),
                 rec["date_verified"], agent, rec["company_name"],
                 1 if st in CONFIRMED_STATUSES else 0,
                 overlap_class(rec["relationship_type"]), edge_weight(rec["relationship_type"], st)))
            self._put_sources("edge", eid, rec["sources"])
            self._bump("edges")
            self._bump(f"edges_{st}")

        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["valuations"]):
            if "__parse_error__" in rec:
                self._reject("valuation", agent, lineno, rec, ["unparseable JSON"]); continue
            errs = validate_record(rec, "valuation")
            if errs:
                self._reject("valuation", agent, lineno, rec, errs); continue
            cid = self.resolve_company(rec["company_name"], agent)
            vid = _hash(cid, rec["valuation_type"], rec["valuation_date"], rec["valuation_usd"])
            self.con.execute(
                "INSERT OR REPLACE INTO valuations (valuation_id, company_id, valuation_usd,"
                " valuation_type, valuation_date, valuation_confidence, share_price,"
                " shares_outstanding, notes, collected_by) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (vid, cid, float(rec["valuation_usd"]), rec["valuation_type"],
                 rec["valuation_date"], rec["valuation_confidence"], rec.get("share_price"),
                 rec.get("shares_outstanding"), rec.get("notes"), agent))
            self._put_sources("valuation", vid, rec["sources"])
            self._bump("valuations")

        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["correlations"]):
            if "__parse_error__" in rec:
                self._reject("correlation", agent, lineno, rec, ["unparseable JSON"]); continue
            errs = validate_record(rec, "correlation")
            if errs:
                self._reject("correlation", agent, lineno, rec, errs); continue
            a, b = sorted([rec["person_key_a"], rec["person_key_b"]])
            if a not in self._known_people or b not in self._known_people:
                self._reject("correlation", agent, lineno, rec,
                             ["one or both person_keys are outside the people universe"])
                continue
            rid = _hash(a, b, rec["correlation_type"])
            strength = rec.get("strength") or CORRELATION_STRENGTH_DEFAULT.get(
                rec["correlation_type"], 0.4)
            self.con.execute(
                "INSERT OR REPLACE INTO investor_relationships (rel_id, person_key_a,"
                " person_key_b, correlation_type, strength, evidence, source_url, derived)"
                " VALUES (?,?,?,?,?,?,?,0)",
                (rid, a, b, rec["correlation_type"], float(strength), rec["evidence"],
                 rec.get("source_url")))
            self._bump("correlations")

        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["rejected"]):
            if "__parse_error__" in rec:
                continue
            rid = _hash(rec.get("person_key"), rec.get("company_name"),
                        rec.get("suspected_relationship"), rec.get("reason_rejected"))
            self.con.execute(
                "INSERT OR REPLACE INTO rejected_edges (rejected_id, person_key, company_name,"
                " suspected_relationship, reason_rejected, source_url, date_checked, rejected_by)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (rid, rec.get("person_key"), rec.get("company_name"),
                 rec.get("suspected_relationship"), rec.get("reason_rejected"),
                 rec.get("source_url"), rec.get("date_checked"), rec.get("rejected_by") or agent))
            self._bump("rejected_edges_recorded")

        for lineno, rec in read_jsonl(batch_dir / BATCH_FILES["queue"]):
            if "__parse_error__" in rec:
                continue
            qid = _hash(rec.get("claim"), rec.get("person_key"), rec.get("company_name"))
            self.con.execute(
                "INSERT OR REPLACE INTO research_queue (queue_id, claim, person_key,"
                " company_name, reason_unresolved, sources_checked, next_source_to_check,"
                " priority, raised_by, date_raised) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (qid, rec.get("claim"), rec.get("person_key"), rec.get("company_name"),
                 rec.get("reason_unresolved"), rec.get("sources_checked"),
                 rec.get("next_source_to_check"), rec.get("priority"),
                 rec.get("raised_by") or agent, rec.get("date_raised")))
            self._bump("research_queue")

        self.con.commit()

    # ------------------------------------------------------------- finalise
    def finalise_companies(self) -> None:
        """Write the company master table. Every company_id referenced by an edge
        or a valuation gets a row, even if no agent supplied a full record."""
        referenced = {r[0] for r in self.con.execute(
            "SELECT DISTINCT company_id FROM person_company_edges "
            "UNION SELECT DISTINCT company_id FROM valuations")}
        for cid in sorted(referenced | set(self._company_rows)):
            rec = self._company_rows.get(cid, {})
            # The curated alias map wins over whatever spelling an agent happened to
            # use, so the canonical table shows one agreed name per entity.
            curated = self.resolver.alias_map.explicit.get(
                tight_key(rec.get("canonical_name") or self.resolver.canonical_name(cid)))
            name = curated or rec.get("canonical_name") or self.resolver.canonical_name(cid)
            self.con.execute(
                "INSERT OR REPLACE INTO companies (company_id, canonical_name, former_names,"
                " aliases, website, country, city, industry_primary, industry_secondary,"
                " company_description, public_or_private, ticker, exchange, founding_year,"
                " founders, current_status, acquired_status, total_funding_usd, notes,"
                " added_by, date_added) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (cid, name, json.dumps(rec.get("former_names") or []),
                 json.dumps(rec.get("aliases") or []), rec.get("website"), rec.get("country"),
                 rec.get("city"), rec.get("industry_primary"), rec.get("industry_secondary"),
                 rec.get("company_description"), rec.get("public_or_private") or "UNKNOWN",
                 rec.get("ticker"), rec.get("exchange"), rec.get("founding_year"),
                 json.dumps(rec.get("founders") or []),
                 rec.get("current_status") or "UNKNOWN", rec.get("acquired_status"),
                 rec.get("total_funding_usd"), rec.get("notes"),
                 ",".join(rec.get("_agents") or []) or "inferred_from_edges",
                 date.today().isoformat()))
        for a in self.resolver.audit:
            self.con.execute(
                "INSERT OR REPLACE INTO company_aliases (alias_norm, alias_raw, company_id,"
                " resolved_by, note) VALUES (?,?,?,?,?)",
                (a["alias_norm"], a["alias_raw"], a["company_id"], a["resolved_by"], a["note"]))
        self.con.commit()
        self._bump("companies", len(referenced | set(self._company_rows)))

    def write_reject_log(self) -> None:
        with self.reject_log.open("w") as fh:
            for r in self.rejects:
                fh.write(json.dumps(r) + "\n")
