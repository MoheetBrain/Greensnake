"""Pick the best defensible CURRENT valuation for each company, and bucket it.

Rules (STEP 5 of the research contract), applied in order:
  PUBLIC  -> latest public_market_cap.
  PRIVATE -> latest primary_round_post_money, else a credible tender/secondary,
             else an acquisition price, else reliable reported_valuation.
  A shut-down company is worth 0 and belongs in TIER_A, not TIER_U -- but only
  when a source says it shut down.
  No sourced valuation -> CURRENT_VALUATION_UNKNOWN -> TIER_U. Never guessed.

Recency beats type: a 2026 secondary is a better *current* read than a 2022
round. So candidates are ranked by (freshness band, type preference, date).
"""
from __future__ import annotations

from datetime import date

from ..core.enums import STALENESS_BANDS, TIER_BOUNDS, TIER_UNKNOWN

# Preference among valuation types, higher is better, used to break ties
# *within* the same freshness band.
TYPE_PREFERENCE = {
    "public_market_cap": 100,
    "primary_round_post_money": 90,
    "tender_or_secondary": 80,
    "acquisition_price": 70,
    "reported_valuation": 50,
    "primary_round_pre_money": 40,
    "shut_down_zero": 95,
}
CONFIDENCE_RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


def parse_partial_date(s: str) -> date:
    """YYYY | YYYY-MM | YYYY-MM-DD -> a concrete date.

    Partial dates resolve to the START of the period, which makes a valuation
    look *older*, never fresher. Erring stale is the safe direction.
    """
    parts = s.split("-")
    y = int(parts[0])
    m = int(parts[1]) if len(parts) > 1 else 1
    d = int(parts[2]) if len(parts) > 2 else 1
    return date(y, m, d)


def staleness(valuation_date: str, as_of: date) -> tuple[str, int]:
    days = (as_of - parse_partial_date(valuation_date)).days
    days = max(days, 0)
    for band, lo, hi in STALENESS_BANDS:
        if lo <= days < hi:
            return band, days
    return STALENESS_BANDS[-1][0], days


FRESHNESS_RANK = {"LT_6M": 5, "6_TO_12M": 4, "12_TO_18M": 3, "18_TO_36M": 2, "GT_36M": 1}


def assign_tier(valuation_usd: float | None) -> str:
    if valuation_usd is None:
        return TIER_UNKNOWN
    for name, lo, hi in TIER_BOUNDS:
        if lo <= valuation_usd < hi:
            return name
    return TIER_UNKNOWN


def resolve_current_valuations(con, as_of: date | None = None) -> dict[str, dict]:
    """Mark one valuation per company as is_current_best and return a summary."""
    as_of = as_of or date.today()
    con.execute("UPDATE valuations SET is_current_best = 0")

    rows = list(con.execute(
        "SELECT valuation_id, company_id, valuation_usd, valuation_type, valuation_date,"
        " valuation_confidence FROM valuations"))
    by_company: dict[str, list] = {}
    for r in rows:
        band, days = staleness(r["valuation_date"], as_of)
        con.execute("UPDATE valuations SET staleness_band=?, staleness_days=? WHERE valuation_id=?",
                    (band, days, r["valuation_id"]))
        by_company.setdefault(r["company_id"], []).append((r, band, days))

    out: dict[str, dict] = {}
    for cid, cands in by_company.items():
        best = max(cands, key=lambda c: (
            FRESHNESS_RANK.get(c[1], 0),
            TYPE_PREFERENCE.get(c[0]["valuation_type"], 0),
            CONFIDENCE_RANK.get(c[0]["valuation_confidence"], 0),
            -c[2],
        ))
        r, band, days = best
        con.execute("UPDATE valuations SET is_current_best=1 WHERE valuation_id=?",
                    (r["valuation_id"],))
        out[cid] = {
            "valuation_id": r["valuation_id"],
            "valuation_usd": r["valuation_usd"],
            "valuation_type": r["valuation_type"],
            "valuation_date": r["valuation_date"],
            "valuation_confidence": r["valuation_confidence"],
            "staleness_band": band,
            "staleness_days": days,
            "tier": assign_tier(r["valuation_usd"]),
            "n_candidates": len(cands),
        }
    con.commit()
    return out


def entry_multiples(con) -> int:
    """current_valuation / valuation_at_entry, where BOTH are known. Never imputed."""
    n = 0
    best = {r["company_id"]: r["valuation_usd"] for r in con.execute(
        "SELECT company_id, valuation_usd FROM valuations WHERE is_current_best=1")}
    for r in con.execute(
            "SELECT edge_id, company_id, entry_valuation_usd FROM person_company_edges"
            " WHERE entry_valuation_usd IS NOT NULL AND entry_valuation_usd > 0"):
        cur = best.get(r["company_id"])
        if cur is None:
            continue
        con.execute("UPDATE person_company_edges SET entry_multiple_to_current=? WHERE edge_id=?",
                    (cur / r["entry_valuation_usd"], r["edge_id"]))
        n += 1
    con.commit()
    return n
