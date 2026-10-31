"""CSV / JSON exports. Every table keeps RAW FACTUAL COUNTS visible next to any
derived score, and carries enough identifiers to walk back to the evidence:

    ranking row -> company_id -> edge_ids -> source rows -> original URL
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from ..core.enums import TIER_BOUNDS, TIER_UNKNOWN

TIER_FILES = {
    "TIER_A_UNDER_500M": "tier_under_500m.csv",
    "TIER_B_500M_TO_1B": "tier_500m_to_1b.csv",
    "TIER_C_1B_TO_5B": "tier_1b_to_5b.csv",
    "TIER_D_5B_PLUS": "tier_over_5b.csv",
    TIER_UNKNOWN: "tier_unknown.csv",
}


def _write(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def _q(con, sql, params=()) -> list[dict]:
    return [dict(r) for r in con.execute(sql, params)]


def company_rows(con, tier: str | None = None) -> list[dict]:
    where = " WHERE cs.valuation_tier = ?" if tier else ""
    params = (tier,) if tier else ()
    rows = _q(con,
        "SELECT c.company_id, c.canonical_name AS company, cs.best_valuation_usd AS valuation_usd,"
        " cs.best_valuation_date AS valuation_date, cs.best_valuation_type AS valuation_type,"
        " cs.best_valuation_confidence AS valuation_confidence, cs.staleness_band,"
        " cs.valuation_tier, c.public_or_private, c.ticker, c.country,"
        " c.industry_primary AS sector, c.current_status,"
        " cs.raw_overlap_count AS raw_people_count,"
        " cs.confirmed_person_count_strict AS strict_people_count,"
        " cs.confirmed_person_count_broad AS broad_people_count,"
        " cs.information_network_count, cs.weighted_person_score AS weighted_score,"
        " cs.independence_adjusted_score, cs.independence_adjusted_delta0,"
        " cs.independence_adjusted_delta1, cs.distinct_information_clusters,"
        " cs.distinct_domains_represented, cs.cross_domain_score,"
        " cs.technical_elite_count, cs.technical_elite_score,"
        " cs.number_of_founder_operators, cs.number_of_professional_investors,"
        " cs.number_of_domain_specialists, cs.number_of_billionaire_founders,"
        " cs.elite_density, cs.technical_elite_density, cs.independent_signal_density,"
        " cs.dated_edge_person_count, cs.elite_connections_24m_ago,"
        " cs.elite_connections_12m_ago, cs.elite_connections_6m_ago, cs.elite_connections_now,"
        " cs.elite_network_momentum_12m, cs.elite_network_momentum_6m,"
        " cs.earliest_elite_entry_date, cs.valuation_at_earliest_elite_entry,"
        " cs.current_to_entry_multiple, cs.best_source_tier AS source_quality, cs.people_list"
        " FROM company_scores cs JOIN companies c ON c.company_id = cs.company_id"
        + where + " ORDER BY cs.raw_overlap_count DESC, cs.weighted_person_score DESC",
        params)
    for r in rows:
        pl = json.loads(r.pop("people_list") or "[]")
        r["names_of_people"] = "; ".join(p["name"] or p["person_key"] for p in pl)
        r["people_detail"] = "; ".join(
            f"{p['name'] or p['person_key']} [{'/'.join(p['relationship_types'])}"
            f"{'' if not p.get('earliest_investment_date') else ' @' + p['earliest_investment_date']}]"
            for p in pl)
        r["technical_elite_names"] = "; ".join(
            p["name"] or p["person_key"] for p in pl if p.get("technical_elite"))
        r["edge_ids"] = ";".join(eid for p in pl for eid in p.get("edge_ids", []))
    return rows


def export_all(con, out_dir: str | Path) -> dict[str, int]:
    out = Path(out_dir)
    counts: dict[str, int] = {}

    counts["people.csv"] = _write(out / "people.csv", _q(con,
        "SELECT p.person_key, p.full_name, p.signal_class, p.primary_affiliation, p.country,"
        " p.archetypes, p.domains, s.access_score, s.technical_intelligence_score,"
        " s.early_stage_track_record, s.founder_network_score, s.capital_flexibility,"
        " s.independence_score, s.investment_visibility, s.herding_risk,"
        " s.general_investment_signal, s.domain_information_signal, s.person_weight,"
        " s.score_method_version, p.rationale, p.added_by"
        " FROM people p LEFT JOIN people_scores s ON s.person_key=p.person_key"
        " ORDER BY s.person_weight DESC NULLS LAST, p.full_name"))

    # INVESTOR / PERSON SCORECARD -- NULL, never invented precision
    counts["person_scorecard.csv"] = _write(out / "person_scorecard.csv", _q(con,
        "SELECT p.person_key, p.full_name AS name, p.domains AS primary_and_secondary_domains,"
        " p.archetypes AS role, p.signal_class, s.access_score AS estimated_access_score,"
        " s.technical_intelligence_score AS technical_information_score,"
        " s.early_stage_track_record AS historical_earliness_score,"
        " o.number_verified_investments AS verified_investment_count,"
        " o.number_major_outliers AS verified_major_outlier_count,"
        " o.number_failures AS failure_count_if_known, o.hit_rate_proxy,"
        " o.disclosure_completeness, s.investment_visibility AS visibility_score,"
        " s.herding_risk, s.independence_score, s.general_investment_signal,"
        " s.domain_information_signal, s.person_weight, o.reliability_caveat AS confidence,"
        " p.rationale AS reason_for_inclusion"
        " FROM people p LEFT JOIN people_scores s ON s.person_key=p.person_key"
        " LEFT JOIN person_outcomes o ON o.person_key=p.person_key"
        " ORDER BY s.person_weight DESC NULLS LAST"))

    counts["companies.csv"] = _write(out / "companies.csv", _q(con,
        "SELECT company_id, canonical_name, former_names, aliases, website, country, city,"
        " industry_primary, industry_secondary, company_description, public_or_private,"
        " ticker, exchange, founding_year, founders, current_status, acquired_status,"
        " parent_company_id, total_funding_usd, notes, added_by, date_added"
        " FROM companies ORDER BY canonical_name"))

    edge_sql = (
        "SELECT e.edge_id, e.person_key, p.full_name AS person_name, e.company_id,"
        " c.canonical_name AS company, e.raw_company_name, e.relationship_type,"
        " e.overlap_class, e.investment_vehicle, e.investment_date, e.round_name,"
        " e.amount_personally_invested_usd, e.round_total_usd, e.entry_valuation_usd,"
        " e.entry_valuation_type, e.ownership_percentage, e.entry_multiple_to_current,"
        " e.verification_status, e.verification_notes, e.date_verified, e.collected_by,"
        " e.edge_weight,"
        " (SELECT GROUP_CONCAT(s.url, ' | ') FROM sources s WHERE s.parent_kind='edge'"
        "   AND s.parent_id=e.edge_id) AS source_urls,"
        " (SELECT GROUP_CONCAT(s.source_type, ' | ') FROM sources s WHERE s.parent_kind='edge'"
        "   AND s.parent_id=e.edge_id) AS source_types,"
        " (SELECT GROUP_CONCAT(s.tier, ' | ') FROM sources s WHERE s.parent_kind='edge'"
        "   AND s.parent_id=e.edge_id) AS source_tiers,"
        " (SELECT GROUP_CONCAT(s.evidence_summary, ' || ') FROM sources s"
        "   WHERE s.parent_kind='edge' AND s.parent_id=e.edge_id) AS evidence_summaries"
        " FROM person_company_edges e JOIN people p ON p.person_key=e.person_key"
        " JOIN companies c ON c.company_id=e.company_id WHERE e.is_confirmed={}"
        " ORDER BY c.canonical_name, p.full_name")
    counts["edges_confirmed.csv"] = _write(out / "edges_confirmed.csv",
                                           _q(con, edge_sql.format(1)))
    counts["edges_unverified.csv"] = _write(out / "edges_unverified.csv",
                                            _q(con, edge_sql.format(0)))

    counts["valuations.csv"] = _write(out / "valuations.csv", _q(con,
        "SELECT v.valuation_id, v.company_id, c.canonical_name AS company, v.valuation_usd,"
        " v.valuation_type, v.valuation_date, v.valuation_confidence, v.staleness_band,"
        " v.staleness_days, v.is_current_best, v.share_price, v.shares_outstanding, v.notes,"
        " v.collected_by,"
        " (SELECT GROUP_CONCAT(s.url, ' | ') FROM sources s WHERE s.parent_kind='valuation'"
        "   AND s.parent_id=v.valuation_id) AS source_urls,"
        " (SELECT GROUP_CONCAT(s.evidence_summary, ' || ') FROM sources s"
        "   WHERE s.parent_kind='valuation' AND s.parent_id=v.valuation_id) AS evidence"
        " FROM valuations v JOIN companies c ON c.company_id=v.company_id"
        " ORDER BY c.canonical_name, v.valuation_date DESC"))

    counts["company_overlap_scores.csv"] = _write(out / "company_overlap_scores.csv",
                                                  company_rows(con))
    for tier, fname in TIER_FILES.items():
        counts[fname] = _write(out / fname, company_rows(con, tier))

    # COMPANY DISCOVERY VIEW -- everything under $5B, tuned for filtering
    disc = [r for r in company_rows(con)
            if r["valuation_tier"] in ("TIER_A_UNDER_500M", "TIER_B_500M_TO_1B",
                                       "TIER_C_1B_TO_5B", TIER_UNKNOWN)]
    counts["company_discovery.csv"] = _write(out / "company_discovery.csv", disc, fieldnames=[
        "company_id", "company", "valuation_usd", "valuation_date", "valuation_tier", "sector",
        "public_or_private", "country", "raw_people_count", "strict_people_count",
        "technical_elite_count", "distinct_information_clusters", "distinct_domains_represented",
        "weighted_score", "independence_adjusted_score", "cross_domain_score",
        "elite_density", "technical_elite_density", "independent_signal_density",
        "earliest_elite_entry_date", "valuation_at_earliest_elite_entry",
        "current_to_entry_multiple", "elite_network_momentum_12m", "elite_network_momentum_6m",
        "source_quality", "valuation_confidence", "staleness_band",
        "names_of_people", "people_detail", "technical_elite_names", "edge_ids"])

    counts["person_person_network.csv"] = _write(out / "person_person_network.csv", _q(con,
        "SELECT r.rel_id, r.person_key_a, a.full_name AS name_a, r.person_key_b,"
        " b.full_name AS name_b, r.correlation_type, r.strength, r.derived, r.evidence,"
        " r.source_url FROM investor_relationships r"
        " JOIN people a ON a.person_key=r.person_key_a"
        " JOIN people b ON b.person_key=r.person_key_b"
        " ORDER BY r.derived, r.strength DESC"))

    counts["rejected_edges.csv"] = _write(out / "rejected_edges.csv", _q(con,
        "SELECT rejected_id, person_key, company_name, suspected_relationship, reason_rejected,"
        " source_url, date_checked, rejected_by FROM rejected_edges ORDER BY person_key"))
    counts["research_queue.csv"] = _write(out / "research_queue.csv", _q(con,
        "SELECT queue_id, claim, person_key, company_name, reason_unresolved, sources_checked,"
        " next_source_to_check, priority, raised_by, date_raised FROM research_queue"
        " ORDER BY CASE priority WHEN 'HIGH' THEN 0 WHEN 'MEDIUM' THEN 1 ELSE 2 END"))
    counts["sources.csv"] = _write(out / "sources.csv", _q(con,
        "SELECT source_id, parent_kind, parent_id, url, source_type, tier, publisher,"
        " published_date, accessed_date, url_http_status, url_checked_at, evidence_summary"
        " FROM sources ORDER BY tier, publisher"))

    # RECENT-ENTRY SIGNAL -- confirmed dates only
    counts["recent_entries.csv"] = _write(out / "recent_entries.csv", _q(con,
        "SELECT e.investment_date, c.canonical_name AS company, cs.valuation_tier,"
        " cs.best_valuation_usd AS valuation_usd, p.full_name AS person, p.signal_class,"
        " e.relationship_type, e.overlap_class, cs.raw_overlap_count, e.edge_id, e.company_id"
        " FROM person_company_edges e JOIN people p ON p.person_key=e.person_key"
        " JOIN companies c ON c.company_id=e.company_id"
        " LEFT JOIN company_scores cs ON cs.company_id=e.company_id"
        " WHERE e.is_confirmed=1 AND e.investment_date IS NOT NULL"
        " ORDER BY e.investment_date DESC"))

    counts["backtest_observations.csv"] = _write(out / "backtest_observations.csv", _q(con,
        "SELECT b.obs_id, c.canonical_name AS company, b.as_of_date, b.valuation_usd,"
        " b.elite_people_count, b.people_list, b.outcome_label, b.notes"
        " FROM backtest_observations b JOIN companies c ON c.company_id=b.company_id"
        " ORDER BY c.canonical_name, b.as_of_date"))

    return counts
