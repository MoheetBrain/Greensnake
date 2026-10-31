"""Data-quality and coverage report. Quantifies coverage rather than claiming it."""
from __future__ import annotations

import json
from collections import Counter, defaultdict

from ..core.enums import STALENESS_BANDS, TIER_BOUNDS, TIER_UNKNOWN, VERIFICATION_STATUSES


def _scalar(con, sql, params=()):
    row = con.execute(sql, params).fetchone()
    return row[0] if row else 0


def build(con) -> dict:
    q: dict = {}
    q["people_total_in_universe"] = _scalar(con, "SELECT COUNT(*) FROM people")
    by_class = {r["signal_class"]: r["n"] for r in con.execute(
        "SELECT signal_class, COUNT(*) n FROM people GROUP BY 1")}
    q["people_by_signal_class"] = by_class
    q["people_core_high_signal"] = by_class.get("CORE_HIGH_SIGNAL", 0)
    q["people_extended_signal"] = by_class.get("EXTENDED_SIGNAL", 0)
    q["people_domain_specialist"] = by_class.get("DOMAIN_SPECIALIST", 0)
    q["people_watchlist"] = by_class.get("WATCHLIST", 0)
    q["people_low_signal"] = by_class.get("LOW_SIGNAL_OR_POOR_VISIBILITY", 0)
    q["people_with_at_least_one_confirmed_edge"] = _scalar(
        con, "SELECT COUNT(DISTINCT person_key) FROM person_company_edges WHERE is_confirmed=1")
    q["people_with_zero_edges"] = q["people_total_in_universe"] - _scalar(
        con, "SELECT COUNT(DISTINCT person_key) FROM person_company_edges")

    q["companies_canonical_total"] = _scalar(con, "SELECT COUNT(*) FROM companies")
    q["company_raw_name_strings_seen"] = _scalar(con, "SELECT COUNT(*) FROM company_aliases")
    q["companies_merged_by_dedup"] = (q["company_raw_name_strings_seen"]
                                      - q["companies_canonical_total"])

    q["edges_total_investigated"] = (
        _scalar(con, "SELECT COUNT(*) FROM person_company_edges")
        + _scalar(con, "SELECT COUNT(*) FROM rejected_edges")
        + _scalar(con, "SELECT COUNT(*) FROM research_queue"))
    by_status = {r["verification_status"]: r["n"] for r in con.execute(
        "SELECT verification_status, COUNT(*) n FROM person_company_edges GROUP BY 1")}
    for s in sorted(VERIFICATION_STATUSES):
        q[f"edges_{s}"] = by_status.get(s, 0)
    q["edges_in_database"] = _scalar(con, "SELECT COUNT(*) FROM person_company_edges")
    q["edges_confirmed"] = _scalar(con, "SELECT COUNT(*) FROM person_company_edges"
                                        " WHERE is_confirmed=1")
    q["edges_rejected_table"] = _scalar(con, "SELECT COUNT(*) FROM rejected_edges")
    q["edges_in_research_queue"] = _scalar(con, "SELECT COUNT(*) FROM research_queue")

    conf = q["edges_confirmed"] or 1
    prim = _scalar(con, "SELECT COUNT(DISTINCT e.edge_id) FROM person_company_edges e"
                        " JOIN sources s ON s.parent_kind='edge' AND s.parent_id=e.edge_id"
                        " WHERE e.is_confirmed=1 AND s.tier='TIER_1_PRIMARY'")
    q["confirmed_edges_with_primary_evidence"] = prim
    q["pct_confirmed_with_primary_evidence"] = round(100.0 * prim / conf, 1)
    only_secondary = _scalar(
        con, "SELECT COUNT(*) FROM (SELECT e.edge_id FROM person_company_edges e"
             " JOIN sources s ON s.parent_kind='edge' AND s.parent_id=e.edge_id"
             " WHERE e.is_confirmed=1 GROUP BY e.edge_id"
             " HAVING SUM(CASE WHEN s.tier='TIER_1_PRIMARY' THEN 1 ELSE 0 END)=0"
             " AND SUM(CASE WHEN s.tier='TIER_2_SECONDARY' THEN 1 ELSE 0 END)>0)")
    q["confirmed_edges_secondary_only"] = only_secondary
    q["pct_confirmed_secondary_only"] = round(100.0 * only_secondary / conf, 1)
    q["sources_total"] = _scalar(con, "SELECT COUNT(*) FROM sources")
    q["sources_by_tier"] = {r["tier"]: r["n"] for r in con.execute(
        "SELECT tier, COUNT(*) n FROM sources GROUP BY 1")}
    q["distinct_source_domains"] = len({
        (r[0].split("//")[-1].split("/")[0].lower().replace("www.", ""))
        for r in con.execute("SELECT url FROM sources") if r[0]})

    by_rel = {r["relationship_type"]: r["n"] for r in con.execute(
        "SELECT relationship_type, COUNT(*) n FROM person_company_edges"
        " WHERE is_confirmed=1 GROUP BY 1 ORDER BY n DESC")}
    q["confirmed_edges_by_relationship_type"] = by_rel

    n_comp = q["companies_canonical_total"] or 1
    with_val = _scalar(con, "SELECT COUNT(DISTINCT company_id) FROM valuations"
                            " WHERE is_current_best=1")
    q["companies_with_current_valuation"] = with_val
    q["pct_companies_with_valuation"] = round(100.0 * with_val / n_comp, 1)
    bands = {r["staleness_band"]: r["n"] for r in con.execute(
        "SELECT staleness_band, COUNT(*) n FROM valuations WHERE is_current_best=1 GROUP BY 1")}
    q["valuation_staleness_counts"] = {b: bands.get(b, 0) for b, _, _ in STALENESS_BANDS}
    q["valuation_staleness_pct_of_valued"] = {
        b: (round(100.0 * bands.get(b, 0) / with_val, 1) if with_val else 0.0)
        for b, _, _ in STALENESS_BANDS}
    q["companies_valuation_unknown"] = n_comp - with_val

    tiers = {r["valuation_tier"]: r["n"] for r in con.execute(
        "SELECT valuation_tier, COUNT(*) n FROM company_scores GROUP BY 1")}
    q["companies_by_tier"] = {t: tiers.get(t, 0) for t, _, _ in TIER_BOUNDS}
    q["companies_by_tier"][TIER_UNKNOWN] = tiers.get(TIER_UNKNOWN, 0)
    q["companies_public"] = _scalar(con, "SELECT COUNT(*) FROM companies"
                                         " WHERE public_or_private='PUBLIC'")
    q["companies_private"] = _scalar(con, "SELECT COUNT(*) FROM companies"
                                          " WHERE public_or_private='PRIVATE'")
    q["companies_public_private_unknown"] = _scalar(
        con, "SELECT COUNT(*) FROM companies WHERE public_or_private NOT IN ('PUBLIC','PRIVATE')"
             " OR public_or_private IS NULL")
    q["companies_with_entry_valuation"] = _scalar(
        con, "SELECT COUNT(DISTINCT company_id) FROM person_company_edges"
             " WHERE entry_valuation_usd IS NOT NULL")
    q["edges_with_investment_date"] = _scalar(
        con, "SELECT COUNT(*) FROM person_company_edges WHERE investment_date IS NOT NULL")
    q["pct_edges_dated"] = round(
        100.0 * q["edges_with_investment_date"] / max(1, q["edges_in_database"]), 1)

    q["correlations_asserted"] = _scalar(con, "SELECT COUNT(*) FROM investor_relationships"
                                              " WHERE derived=0")
    q["correlations_derived"] = _scalar(con, "SELECT COUNT(*) FROM investor_relationships"
                                             " WHERE derived=1")

    # people whose portfolio could not be reconstructed
    unreconstructed = [dict(r) for r in con.execute(
        "SELECT p.person_key, p.full_name, p.signal_class FROM people p"
        " WHERE NOT EXISTS (SELECT 1 FROM person_company_edges e"
        " WHERE e.person_key=p.person_key AND e.is_confirmed=1) ORDER BY p.signal_class, p.full_name")]
    q["people_without_reconstructable_portfolio"] = unreconstructed
    q["n_people_without_reconstructable_portfolio"] = len(unreconstructed)

    # sector / geography coverage -- where the graph is thin
    q["companies_by_sector"] = {r["s"]: r["n"] for r in con.execute(
        "SELECT COALESCE(NULLIF(TRIM(industry_primary),''),'(unlabelled)') s, COUNT(*) n"
        " FROM companies GROUP BY 1 ORDER BY n DESC")}
    q["companies_by_country"] = {r["c"]: r["n"] for r in con.execute(
        "SELECT COALESCE(NULLIF(TRIM(country),''),'(unstated)') c, COUNT(*) n"
        " FROM companies GROUP BY 1 ORDER BY n DESC")}
    q["companies_sector_unlabelled"] = q["companies_by_sector"].get("(unlabelled)", 0)
    q["companies_country_unstated"] = q["companies_by_country"].get("(unstated)", 0)
    q["edges_by_workstream"] = {r["w"]: r["n"] for r in con.execute(
        "SELECT collected_by w, COUNT(*) n FROM person_company_edges WHERE is_confirmed=1"
        " GROUP BY 1 ORDER BY n DESC")}

    dead = _scalar(con, "SELECT COUNT(*) FROM sources WHERE url_http_status IS NOT NULL"
                        " AND url_http_status >= 400")
    checked = _scalar(con, "SELECT COUNT(*) FROM sources WHERE url_http_status IS NOT NULL")
    q["source_urls_checked"] = checked
    q["source_urls_failing"] = dead
    q["pct_source_urls_resolving"] = (round(100.0 * (checked - dead) / checked, 1)
                                      if checked else None)
    return q


def completeness_assessment(q: dict) -> tuple[str, list[str]]:
    """An explicit, deliberately conservative completeness grade."""
    reasons = []
    people_cov = (q["people_with_at_least_one_confirmed_edge"]
                  / max(1, q["people_total_in_universe"]))
    val_cov = q["pct_companies_with_valuation"] / 100.0
    prim = q["pct_confirmed_with_primary_evidence"] / 100.0

    if people_cov < 0.5:
        reasons.append(f"only {people_cov:.0%} of the people universe has any confirmed edge")
    if val_cov < 0.5:
        reasons.append(f"only {val_cov:.0%} of companies carry a sourced current valuation")
    if prim < 0.5:
        reasons.append(f"only {prim:.0%} of confirmed edges rest on Tier-1 primary evidence")
    if q["pct_edges_dated"] < 60:
        reasons.append(f"only {q['pct_edges_dated']:.0f}% of edges carry an investment date, "
                       f"which limits every temporal metric")

    if people_cov >= 0.8 and val_cov >= 0.7 and prim >= 0.6 and not reasons:
        grade = "SUBSTANTIAL"
    elif people_cov >= 0.5 and val_cov >= 0.4:
        grade = "PARTIAL"
    else:
        grade = "EXPLORATORY"
    reasons.append("Angel and family-office investing is structurally under-disclosed: "
                   "absence of an edge is never evidence of absence of an investment.")
    reasons.append("Losses and write-offs are disclosed far less often than wins, so the "
                   "failure database understates true failure rates.")
    return grade, reasons
