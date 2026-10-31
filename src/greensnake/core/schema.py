"""Record-level validation for everything entering the graph.

Hard rule enforced here (ABSOLUTE CONSTRAINT: ZERO UNSOURCED CLAIMS):
an edge may not carry a CONFIRMED_* status unless it has real sources of the
right tier with a non-trivial evidence summary. Bad records are never coerced
into good ones -- they are downgraded and routed to the research queue or the
rejected table, with the reason recorded.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

from .enums import (
    CONFIRMED_STATUSES, COMPANY_STATUSES, CORRELATION_TYPES, DOMAINS,
    NON_CONFIRMING_SOURCE_TYPES, PERSON_ARCHETYPES, PERSON_SIGNAL_CLASSES,
    RELATIONSHIP_TYPES, SCORE_COMPONENTS_ASSERTED, SCORE_MAX, SCORE_MIN,
    SOURCE_TYPES, TIER_OF_SOURCE_TYPE, VALUATION_CONFIDENCE, VALUATION_TYPES,
    VERIFICATION_STATUSES,
)

SLUG_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://[^\s<>\"]+$", re.I)
# YYYY | YYYY-MM | YYYY-MM-DD
PARTIAL_DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

MIN_EVIDENCE_CHARS = 40
# Upper bound so collectors summarise rather than paste copyrighted text.
MAX_EVIDENCE_CHARS = 700


class RecordError(Exception):
    pass


def _err(errors: list[str], cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


def _is_partial_date(v: Any) -> bool:
    return isinstance(v, str) and bool(PARTIAL_DATE_RE.match(v))


def _is_iso_date(v: Any) -> bool:
    if not isinstance(v, str):
        return False
    try:
        date.fromisoformat(v)
        return True
    except ValueError:
        return False


def _nonneg_number(v: Any) -> bool:
    return v is None or (isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0)


# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------
def validate_source(src: Any, idx: int) -> list[str]:
    e: list[str] = []
    if not isinstance(src, dict):
        return [f"sources[{idx}]: not an object"]
    url = src.get("url")
    _err(e, isinstance(url, str) and bool(URL_RE.match(url)),
         f"sources[{idx}].url: missing or not an http(s) URL")
    st = src.get("source_type")
    _err(e, st in SOURCE_TYPES, f"sources[{idx}].source_type: {st!r} not in controlled vocabulary")
    tier = src.get("tier")
    if st in SOURCE_TYPES:
        expected = TIER_OF_SOURCE_TYPE[st]
        _err(e, tier == expected,
             f"sources[{idx}].tier: {tier!r} contradicts source_type {st!r} (must be {expected})")
    ev = src.get("evidence_summary")
    _err(e, isinstance(ev, str) and len(ev.strip()) >= MIN_EVIDENCE_CHARS,
         f"sources[{idx}].evidence_summary: must be >= {MIN_EVIDENCE_CHARS} chars explaining "
         f"why this source proves the relationship")
    if isinstance(ev, str):
        _err(e, len(ev) <= MAX_EVIDENCE_CHARS,
             f"sources[{idx}].evidence_summary: > {MAX_EVIDENCE_CHARS} chars -- summarise, "
             f"do not paste source text")
    pd = src.get("published_date")
    _err(e, pd is None or _is_partial_date(pd),
         f"sources[{idx}].published_date: must be YYYY[-MM[-DD]] or null")
    ad = src.get("accessed_date")
    _err(e, _is_iso_date(ad), f"sources[{idx}].accessed_date: must be YYYY-MM-DD")
    return e


# --------------------------------------------------------------------------
# Edges
# --------------------------------------------------------------------------
EDGE_REQUIRED = ("person_key", "company_name", "relationship_type",
                 "verification_status", "sources", "collected_by")


def validate_edge(rec: dict) -> list[str]:
    e: list[str] = []
    for f in EDGE_REQUIRED:
        _err(e, f in rec, f"missing required field {f!r}")
    pk = rec.get("person_key")
    _err(e, isinstance(pk, str) and bool(SLUG_RE.match(pk or "")),
         f"person_key: {pk!r} must be a lower_snake slug")
    cn = rec.get("company_name")
    _err(e, isinstance(cn, str) and len(cn.strip()) >= 2, "company_name: missing/too short")
    rt = rec.get("relationship_type")
    _err(e, rt in RELATIONSHIP_TYPES, f"relationship_type: {rt!r} not in controlled vocabulary")
    vs = rec.get("verification_status")
    _err(e, vs in VERIFICATION_STATUSES, f"verification_status: {vs!r} not in controlled vocabulary")

    for f in ("investment_date",):
        v = rec.get(f)
        _err(e, v is None or _is_partial_date(v), f"{f}: must be YYYY[-MM[-DD]] or null")
    _err(e, _is_iso_date(rec.get("date_verified")), "date_verified: must be YYYY-MM-DD")
    for f in ("amount_personally_invested_usd", "round_total_usd", "entry_valuation_usd"):
        _err(e, _nonneg_number(rec.get(f)), f"{f}: must be a non-negative number or null")
    op = rec.get("ownership_percentage")
    _err(e, op is None or (isinstance(op, (int, float)) and 0 <= op <= 100),
         "ownership_percentage: must be 0-100 or null")

    srcs = rec.get("sources")
    if not isinstance(srcs, list) or not srcs:
        e.append("sources: at least one source object is required -- no unsourced claims")
    else:
        for i, s in enumerate(srcs):
            e.extend(validate_source(s, i))

    # --- the anti-hallucination gate -------------------------------------
    if vs in CONFIRMED_STATUSES and isinstance(srcs, list) and srcs:
        types = [s.get("source_type") for s in srcs if isinstance(s, dict)]
        tiers = [TIER_OF_SOURCE_TYPE.get(t) for t in types]
        non_db = [t for t in types if t not in NON_CONFIRMING_SOURCE_TYPES]
        _err(e, bool(non_db),
             "verification_status is CONFIRMED_* but every source is a Tier-3 database; "
             "a database listing alone can never confirm an edge")
        if vs == "CONFIRMED_PRIMARY":
            _err(e, "TIER_1_PRIMARY" in tiers,
                 "CONFIRMED_PRIMARY requires at least one TIER_1_PRIMARY source")
        if vs == "CONFIRMED_MULTI_SOURCE":
            distinct = {s.get("url") for s in srcs if isinstance(s, dict)}
            _err(e, len(distinct) >= 2,
                 "CONFIRMED_MULTI_SOURCE requires >= 2 distinct source URLs")
            _err(e, len(non_db) >= 2,
                 "CONFIRMED_MULTI_SOURCE requires >= 2 non-database sources")
        if vs == "CONFIRMED_REPUTABLE_SECONDARY":
            _err(e, any(t == "TIER_2_SECONDARY" for t in tiers),
                 "CONFIRMED_REPUTABLE_SECONDARY requires a TIER_2_SECONDARY source")

    # Guard the single most common category error in this domain.
    veh = (rec.get("investment_vehicle") or "").strip().lower()
    if rt in ("PERSONAL_ANGEL_INVESTMENT", "PERSONAL_EQUITY_INVESTMENT"):
        bad = any(k in veh for k in ("ventures", "capital", "partners", "fund",
                                     "management", " lp", "llc fund"))
        _err(e, not bad,
             f"relationship_type {rt} but investment_vehicle {rec.get('investment_vehicle')!r} "
             f"names a fund -- use CONTROLLED_FUND_INVESTMENT or VC_FUND_PARTNER_INVESTMENT")
    return e


# --------------------------------------------------------------------------
# Companies, valuations, people
# --------------------------------------------------------------------------
def validate_company(rec: dict) -> list[str]:
    e: list[str] = []
    _err(e, isinstance(rec.get("canonical_name"), str) and len(rec["canonical_name"].strip()) >= 2,
         "canonical_name: missing/too short")
    pp = rec.get("public_or_private")
    _err(e, pp in ("PUBLIC", "PRIVATE", "SUBSIDIARY", "UNKNOWN", None),
         f"public_or_private: {pp!r} invalid")
    cs = rec.get("current_status")
    _err(e, cs is None or cs in COMPANY_STATUSES, f"current_status: {cs!r} invalid")
    fy = rec.get("founding_year")
    _err(e, fy is None or (isinstance(fy, int) and 1800 <= fy <= 2030),
         "founding_year: implausible")
    for f in ("former_names", "aliases", "founders"):
        v = rec.get(f)
        _err(e, v is None or isinstance(v, list), f"{f}: must be a list or null")
    ws = rec.get("website")
    _err(e, ws is None or (isinstance(ws, str) and bool(URL_RE.match(ws))),
         "website: must be an http(s) URL or null")
    return e


def validate_valuation(rec: dict) -> list[str]:
    e: list[str] = []
    _err(e, isinstance(rec.get("company_name"), str), "company_name: required")
    v = rec.get("valuation_usd")
    _err(e, isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0,
         "valuation_usd: required non-negative number (use null record instead of a guess)")
    vt = rec.get("valuation_type")
    _err(e, vt in VALUATION_TYPES, f"valuation_type: {vt!r} not in controlled vocabulary")
    _err(e, _is_partial_date(rec.get("valuation_date")),
         "valuation_date: required, YYYY[-MM[-DD]] -- a valuation without a date is unusable")
    vc = rec.get("valuation_confidence")
    _err(e, vc in VALUATION_CONFIDENCE, f"valuation_confidence: {vc!r} invalid")
    srcs = rec.get("sources")
    if not isinstance(srcs, list) or not srcs:
        e.append("sources: a valuation with no source is never accepted")
    else:
        for i, s in enumerate(srcs):
            e.extend(validate_source(s, i))
    return e


def validate_person(rec: dict) -> list[str]:
    e: list[str] = []
    pk = rec.get("person_key")
    _err(e, isinstance(pk, str) and bool(SLUG_RE.match(pk or "")),
         f"person_key: {pk!r} must be a lower_snake slug")
    _err(e, isinstance(rec.get("full_name"), str) and rec["full_name"].strip(),
         "full_name: required")
    sc = rec.get("signal_class")
    _err(e, sc in PERSON_SIGNAL_CLASSES, f"signal_class: {sc!r} invalid")
    arch = rec.get("archetypes") or []
    _err(e, isinstance(arch, list) and all(a in PERSON_ARCHETYPES for a in arch),
         f"archetypes: must be a list drawn from {sorted(PERSON_ARCHETYPES)}")
    doms = rec.get("domains") or []
    _err(e, isinstance(doms, list) and all(d in DOMAINS for d in doms),
         "domains: must be a list drawn from the DOMAINS vocabulary")
    scores = rec.get("scores") or {}
    _err(e, isinstance(scores, dict), "scores: must be an object")
    if isinstance(scores, dict):
        for comp in SCORE_COMPONENTS_ASSERTED:
            v = scores.get(comp)
            _err(e, isinstance(v, int) and SCORE_MIN <= v <= SCORE_MAX,
                 f"scores.{comp}: required integer {SCORE_MIN}-{SCORE_MAX} (ordinal band, "
                 f"not a fabricated decimal)")
    _err(e, isinstance(rec.get("rationale"), str) and len(rec.get("rationale", "")) >= 30,
         "rationale: required, >=30 chars, why this person is in the universe at this class")
    return e


def validate_correlation(rec: dict) -> list[str]:
    e: list[str] = []
    for f in ("person_key_a", "person_key_b"):
        v = rec.get(f)
        _err(e, isinstance(v, str) and bool(SLUG_RE.match(v or "")), f"{f}: must be a slug")
    _err(e, rec.get("person_key_a") != rec.get("person_key_b"), "self-correlation not allowed")
    ct = rec.get("correlation_type")
    _err(e, ct in CORRELATION_TYPES, f"correlation_type: {ct!r} invalid")
    s = rec.get("strength")
    _err(e, s is None or (isinstance(s, (int, float)) and 0 < s <= 1),
         "strength: must be in (0,1] or null to use the default for the type")
    _err(e, isinstance(rec.get("evidence"), str) and len(rec.get("evidence", "")) >= 20,
         "evidence: required, >=20 chars")
    return e


VALIDATORS = {
    "edge": validate_edge,
    "company": validate_company,
    "valuation": validate_valuation,
    "person": validate_person,
    "correlation": validate_correlation,
}


def validate_record(rec: dict, kind: str) -> list[str]:
    if kind not in VALIDATORS:
        return [f"unknown record kind {kind!r}"]
    if not isinstance(rec, dict):
        return ["record is not a JSON object"]
    return VALIDATORS[kind](rec)
