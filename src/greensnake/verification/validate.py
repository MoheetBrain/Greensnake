"""The ten automated integrity tests, plus the data-quality report.

Run before any final output. A FAIL means a published number could be wrong;
a WARN means a human should look. Nothing here silently repairs data.
"""
from __future__ import annotations

import json
from collections import defaultdict

from ..core.enums import (
    BROAD_EXTRA_TYPES, CONFIRMED_STATUSES, STRICT_TYPES, TIER_BOUNDS, TIER_UNKNOWN,
)

FUND_MARKERS = ("ventures", "venture", " capital", "capital ", "partners", " fund",
                "fund ", "management", " lp", "l.p.", "associates")


class Result:
    def __init__(self, test_id, name):
        self.test_id, self.name = test_id, name
        self.status, self.detail, self.examples = "PASS", "", []

    def fail(self, detail, examples=None):
        self.status, self.detail = "FAIL", detail
        self.examples = (examples or [])[:10]
        return self

    def warn(self, detail, examples=None):
        self.status, self.detail = "WARN", detail
        self.examples = (examples or [])[:10]
        return self

    def ok(self, detail=""):
        self.detail = detail
        return self

    def as_dict(self):
        return {"test_id": self.test_id, "name": self.name, "status": self.status,
                "detail": self.detail, "examples": self.examples}


def t01_confirmed_edges_have_sources(con) -> Result:
    r = Result("T01", "Every confirmed edge has at least one valid source")
    bad = [row["edge_id"] for row in con.execute(
        "SELECT e.edge_id FROM person_company_edges e WHERE e.is_confirmed=1 AND NOT EXISTS ("
        " SELECT 1 FROM sources s WHERE s.parent_kind='edge' AND s.parent_id=e.edge_id)")]
    return r.fail(f"{len(bad)} confirmed edges have no source row", bad) if bad else \
        r.ok("all confirmed edges carry at least one source")


def t02_bucketed_companies_have_sourced_dated_valuation(con) -> Result:
    r = Result("T02", "Every company in a valuation bucket has valuation + date + source")
    bad = []
    for row in con.execute(
            "SELECT cs.company_id, cs.valuation_tier, cs.best_valuation_usd,"
            " cs.best_valuation_date FROM company_scores cs WHERE cs.valuation_tier != ?",
            (TIER_UNKNOWN,)):
        if row["best_valuation_usd"] is None or not row["best_valuation_date"]:
            bad.append({"company_id": row["company_id"], "why": "missing valuation or date"})
            continue
        n = con.execute(
            "SELECT COUNT(*) c FROM sources s JOIN valuations v ON v.valuation_id=s.parent_id"
            " WHERE s.parent_kind='valuation' AND v.company_id=? AND v.is_current_best=1",
            (row["company_id"],)).fetchone()["c"]
        if n == 0:
            bad.append({"company_id": row["company_id"], "why": "current valuation has no source"})
    return r.fail(f"{len(bad)} bucketed companies lack a sourced, dated valuation", bad) if bad \
        else r.ok("every bucketed company has a sourced, dated valuation")


def t03_no_duplicate_canonical_entities(con) -> Result:
    r = Result("T03", "No company exists under multiple canonical IDs without a stated reason")
    from ..entity_resolution.dedupe import tight_key
    seen: dict[str, list[str]] = defaultdict(list)
    for row in con.execute("SELECT company_id, canonical_name, parent_company_id FROM companies"):
        seen[tight_key(row["canonical_name"])].append(row["company_id"])
    dupes = {k: v for k, v in seen.items() if len(set(v)) > 1}
    if dupes:
        return r.fail(f"{len(dupes)} normalised names map to >1 company_id",
                      [{"key": k, "ids": sorted(set(v))} for k, v in dupes.items()])
    # Near-miss WARN: one name is a strict prefix of another. Pairs already
    # reviewed and recorded in the do_not_merge list are NOT re-flagged --
    # a warning a human has answered should stop nagging, or it trains people
    # to ignore the whole test.
    from ..entity_resolution.dedupe import AliasMap
    from pathlib import Path as _P
    am = AliasMap(_P(__file__).resolve().parents[3] / "data" / "company_aliases.yaml")
    names = [(row["company_id"], tight_key(row["canonical_name"]))
             for row in con.execute("SELECT company_id, canonical_name FROM companies")]
    near = []
    for i, (ca, ka) in enumerate(names):
        for cb, kb in names[i + 1:]:
            if len(ka) >= 7 and len(kb) >= 7 and ka != kb and (ka.startswith(kb) or kb.startswith(ka)):
                if am.blocked(ka, kb):
                    continue
                near.append({"a": ca, "b": cb})
    if near:
        return r.warn(f"{len(near)} near-miss company name pairs need human review", near)
    return r.ok("no duplicate or near-duplicate canonical entities")


def t04_ranking_counts_match_edges(con) -> Result:
    r = Result("T04", "Counts in ranking tables exactly equal their underlying edges")
    bad = []
    for row in con.execute("SELECT company_id, raw_overlap_count, confirmed_person_count_strict,"
                           " confirmed_person_count_broad, people_list FROM company_scores"):
        actual_raw = con.execute(
            "SELECT COUNT(DISTINCT person_key) c FROM person_company_edges"
            " WHERE company_id=? AND is_confirmed=1", (row["company_id"],)).fetchone()["c"]
        actual_strict = con.execute(
            "SELECT COUNT(DISTINCT person_key) c FROM person_company_edges"
            " WHERE company_id=? AND is_confirmed=1 AND overlap_class='STRICT'",
            (row["company_id"],)).fetchone()["c"]
        actual_broad = con.execute(
            "SELECT COUNT(DISTINCT person_key) c FROM person_company_edges"
            " WHERE company_id=? AND is_confirmed=1 AND overlap_class IN ('STRICT','BROAD')",
            (row["company_id"],)).fetchone()["c"]
        listed = len(json.loads(row["people_list"] or "[]"))
        if (actual_raw != row["raw_overlap_count"] or actual_strict != row["confirmed_person_count_strict"]
                or actual_broad != row["confirmed_person_count_broad"] or listed != actual_raw):
            bad.append({"company_id": row["company_id"], "stored_raw": row["raw_overlap_count"],
                        "actual_raw": actual_raw, "stored_strict": row["confirmed_person_count_strict"],
                        "actual_strict": actual_strict, "people_list_len": listed})
    return r.fail(f"{len(bad)} companies where a score disagrees with its edges", bad) if bad \
        else r.ok("every stored count reconciles exactly to the edge table")


def t05_tier_boundaries_disjoint(con) -> Result:
    r = Result("T05", "Tier boundaries are mutually exclusive and correctly applied")
    bad = []
    for row in con.execute("SELECT company_id, best_valuation_usd, valuation_tier"
                           " FROM company_scores"):
        v, t = row["best_valuation_usd"], row["valuation_tier"]
        if v is None:
            if t != TIER_UNKNOWN:
                bad.append({"company_id": row["company_id"], "why": f"no valuation but tier={t}"})
            continue
        expected = next((n for n, lo, hi in TIER_BOUNDS if lo <= v < hi), TIER_UNKNOWN)
        if t != expected:
            bad.append({"company_id": row["company_id"], "valuation": v,
                        "tier": t, "expected": expected})
    return r.fail(f"{len(bad)} companies in the wrong tier", bad) if bad \
        else r.ok("all companies sit in exactly the tier their valuation implies")


def t06_unknown_valuations_never_assigned(con) -> Result:
    r = Result("T06", "Unknown valuations are never silently given a bucket")
    bad = [dict(row) for row in con.execute(
        "SELECT company_id, valuation_tier FROM company_scores"
        " WHERE best_valuation_usd IS NULL AND valuation_tier != ?", (TIER_UNKNOWN,))]
    return r.fail(f"{len(bad)} companies bucketed without a valuation", bad) if bad \
        else r.ok("every company without a sourced valuation is in TIER_U_UNKNOWN")


def t07_no_blank_source_urls(con) -> Result:
    r = Result("T07", "No source URL is blank for a CONFIRMED record")
    q = ",".join("?" * len(CONFIRMED_STATUSES))
    bad = [dict(row) for row in con.execute(
        f"SELECT s.source_id, s.parent_id FROM sources s JOIN person_company_edges e"
        f" ON e.edge_id=s.parent_id WHERE s.parent_kind='edge'"
        f" AND e.verification_status IN ({q})"
        f" AND (s.url IS NULL OR TRIM(s.url)='' OR s.url NOT LIKE 'http%')",
        tuple(sorted(CONFIRMED_STATUSES)))]
    return r.fail(f"{len(bad)} confirmed-edge sources have a blank or non-http URL", bad) if bad \
        else r.ok("every confirmed-edge source has an http(s) URL")


def t08_no_double_counting_across_rounds(con) -> Result:
    r = Result("T08", "No person-company pair is double-counted across funding rounds")
    bad = []
    multi = list(con.execute(
        "SELECT company_id, person_key, COUNT(*) n FROM person_company_edges"
        " WHERE is_confirmed=1 GROUP BY company_id, person_key HAVING n > 1"))
    for row in multi:
        pl = con.execute("SELECT people_list FROM company_scores WHERE company_id=?",
                         (row["company_id"],)).fetchone()
        if not pl:
            continue
        occurrences = sum(1 for p in json.loads(pl["people_list"] or "[]")
                          if p["person_key"] == row["person_key"])
        if occurrences != 1:
            bad.append({"company_id": row["company_id"], "person_key": row["person_key"],
                        "edges": row["n"], "appearances_in_score": occurrences})
    detail = (f"{len(multi)} person-company pairs span multiple rounds; each contributes "
              f"exactly once to counts and scores")
    return r.fail(f"{len(bad)} pairs counted more than once", bad) if bad else r.ok(detail)


def t09_founder_equity_distinguishable(con) -> Result:
    r = Result("T09", "Founder equity is distinguishable from subsequent investing")
    counts = {row["relationship_type"]: row["n"] for row in con.execute(
        "SELECT relationship_type, COUNT(*) n FROM person_company_edges GROUP BY 1")}
    fe = counts.get("FOUNDER_EQUITY", 0)
    ext = sum(v for k, v in counts.items() if k in STRICT_TYPES and k != "FOUNDER_EQUITY")
    bad = [dict(row) for row in con.execute(
        "SELECT edge_id, person_key, company_id FROM person_company_edges"
        " WHERE relationship_type='FOUNDER_EQUITY' AND round_name IS NOT NULL"
        " AND LOWER(round_name) LIKE '%series%'")]
    if bad:
        return r.warn(f"{len(bad)} FOUNDER_EQUITY edges carry a priced-round name -- check "
                      f"whether these are founder shares or a later purchase", bad)
    return r.ok(f"{fe} FOUNDER_EQUITY vs {ext} other direct-exposure edges, separately typed")


def t10_controlled_funds_not_labelled_personal(con) -> Result:
    r = Result("T10", "Controlled-fund exposure is not mislabelled as personal investment")
    bad = []
    for row in con.execute(
            "SELECT edge_id, person_key, company_id, relationship_type, investment_vehicle"
            " FROM person_company_edges WHERE relationship_type IN"
            " ('PERSONAL_ANGEL_INVESTMENT','PERSONAL_EQUITY_INVESTMENT')"):
        v = (row["investment_vehicle"] or "").lower()
        if any(m in v for m in FUND_MARKERS):
            bad.append({"edge_id": row["edge_id"], "person_key": row["person_key"],
                        "vehicle": row["investment_vehicle"]})
    n_controlled = con.execute(
        "SELECT COUNT(*) c FROM person_company_edges WHERE relationship_type IN"
        f" ({','.join('?' * len(BROAD_EXTRA_TYPES))})", tuple(sorted(BROAD_EXTRA_TYPES))
    ).fetchone()["c"]
    n_partner = con.execute("SELECT COUNT(*) c FROM person_company_edges WHERE"
                            " relationship_type='VC_FUND_PARTNER_INVESTMENT'").fetchone()["c"]
    return r.fail(f"{len(bad)} PERSONAL_* edges name a fund as the vehicle", bad) if bad \
        else r.ok(f"{n_controlled} controlled-vehicle and {n_partner} fund-partner edges are "
                  f"typed separately from personal exposure")


def t11_no_edge_rests_only_on_dead_links(con) -> Result:
    """A dead citation does not make a claim false -- it makes it uncheckable.

    Skipped entirely when liveness has not been run (--check-urls), because
    reporting PASS on unchecked data would be worse than reporting nothing.
    """
    r = Result("T11", "No confirmed edge rests solely on non-resolving citations")
    checked = con.execute("SELECT COUNT(*) c FROM sources WHERE url_http_status IS NOT NULL"
                          " OR url_checked_at IS NOT NULL").fetchone()["c"]
    if checked == 0:
        return r.warn("source liveness has not been run -- rerun with --check-urls")
    from .url_check import ALIVE_EVEN_IF_ERROR
    alive = ",".join(str(x) for x in sorted(ALIVE_EVEN_IF_ERROR))
    bad = [dict(row) for row in con.execute(
        f"SELECT e.edge_id, e.person_key, e.company_id, e.verification_status"
        f" FROM person_company_edges e WHERE e.is_confirmed=1"
        f" AND NOT EXISTS (SELECT 1 FROM sources s WHERE s.parent_kind='edge'"
        f"   AND s.parent_id=e.edge_id AND s.url_checked_at IS NOT NULL"
        f"   AND s.url_http_status IS NOT NULL"
        f"   AND (s.url_http_status < 400 OR s.url_http_status IN ({alive})))"
        f" AND EXISTS (SELECT 1 FROM sources s WHERE s.parent_kind='edge'"
        f"   AND s.parent_id=e.edge_id AND s.url_checked_at IS NOT NULL)")]
    if bad:
        return r.warn(f"{len(bad)} confirmed edges have no citation that still resolves; "
                      f"they need re-sourcing before the claim can be re-checked", bad)
    return r.ok("every confirmed edge retains at least one resolving citation")


TESTS = [t01_confirmed_edges_have_sources, t02_bucketed_companies_have_sourced_dated_valuation,
         t03_no_duplicate_canonical_entities, t04_ranking_counts_match_edges,
         t05_tier_boundaries_disjoint, t06_unknown_valuations_never_assigned,
         t07_no_blank_source_urls, t08_no_double_counting_across_rounds,
         t09_founder_equity_distinguishable, t10_controlled_funds_not_labelled_personal,
         t11_no_edge_rests_only_on_dead_links]


def run_all(con) -> list[dict]:
    return [t(con).as_dict() for t in TESTS]
