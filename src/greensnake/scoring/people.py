"""Person scoring. METHOD VERSION: person-score-v1.

Layer discipline:
  FACT     -- the edges and their sources. Untouched by anything here.
  ASSERTED -- ordinal 0-5 bands set in research/people/people_universe.yaml,
              each with a written rationale. ANALYTICAL INTERPRETATION.
  DERIVED  -- investment_visibility and herding_risk, computed FROM this graph.
              They change when the data changes; they are never hand-set.

Nothing in this module alters a raw count. Weighted scores are presented next
to raw counts, never instead of them.
"""
from __future__ import annotations

import json
from collections import defaultdict

from ..core.enums import PERSON_CLASS_WEIGHT
from ..graph.correlation import CorrelationGraph, person_domain_clusters

METHOD_VERSION = "person-score-v1"

# Composite weights over the ASSERTED ordinal bands. Deliberately round numbers:
# the inputs are 0-5 ordinals, so fine-grained weights would be false precision.
COMPOSITE_WEIGHTS = {
    "access_score": 0.30,
    "technical_intelligence_score": 0.25,
    "early_stage_track_record": 0.25,
    "founder_network_score": 0.20,
}
# Light multiplier for research class. Signal_class is mostly a research-priority
# label; the penalty exists because poor visibility means the edges we DO see are
# an unrepresentative sample of that person's real activity.
CLASS_MULTIPLIER = {
    "CORE_HIGH_SIGNAL": 1.00,
    "EXTENDED_SIGNAL": 0.90,
    "DOMAIN_SPECIALIST": 0.90,
    "WATCHLIST": 0.70,
    "LOW_SIGNAL_OR_POOR_VISIBILITY": 0.50,
}
TECHNICAL_ARCHETYPES = {"RESEARCH_SCIENTIST", "ACADEMIC"}


def is_technical_elite(technical: int | None, archetypes: list[str]) -> bool:
    """Documented technical/scientific capability -- NOT celebrity.

    Qualifies if the person is a band-4+ technical node AND either holds a
    research/academic archetype, or is a band-5 technical founder-operator
    (i.e. an engineer who built the thing, not a famous name attached to it).
    """
    if technical is None or technical < 4:
        return False
    a = set(archetypes or [])
    if a & TECHNICAL_ARCHETYPES:
        return True
    return technical >= 5 and "FOUNDER_OPERATOR" in a


def compute_derived(con) -> dict[str, dict]:
    """investment_visibility and herding_risk, both derived from this graph."""
    cg = CorrelationGraph(con)
    conf_by_person: dict[str, set[str]] = defaultdict(set)
    tier_by_person: dict[str, list[str]] = defaultdict(list)
    for r in con.execute(
            "SELECT e.person_key, e.company_id, s.tier FROM person_company_edges e"
            " LEFT JOIN sources s ON s.parent_kind='edge' AND s.parent_id=e.edge_id"
            " WHERE e.is_confirmed=1"):
        conf_by_person[r["person_key"]].add(r["company_id"])
        if r["tier"]:
            tier_by_person[r["person_key"]].append(r["tier"])

    holders_per_company: dict[str, int] = defaultdict(int)
    for r in con.execute(
            "SELECT company_id, COUNT(DISTINCT person_key) n FROM person_company_edges"
            " WHERE is_confirmed=1 GROUP BY company_id"):
        holders_per_company[r["company_id"]] = r["n"]

    all_people = [r["person_key"] for r in con.execute("SELECT person_key FROM people")]
    out: dict[str, dict] = {}
    for pk in all_people:
        comps = conf_by_person.get(pk, set())
        n = len(comps)
        tiers = tier_by_person.get(pk, [])
        t1 = sum(1 for t in tiers if t == "TIER_1_PRIMARY")
        tier_quality = (t1 / len(tiers)) if tiers else 0.0
        # 0-5 band: how well can this person's portfolio actually be reconstructed?
        if n == 0:
            vis = 0.0
        elif n < 3:
            vis = 1.0
        elif n < 8:
            vis = 2.0
        elif n < 20:
            vis = 3.0
        elif n < 50:
            vis = 4.0
        else:
            vis = 5.0
        vis = round(min(5.0, vis + tier_quality), 2)

        # herding: what share of their confirmed book is crowded with the pool,
        # blended with how correlated they are with everyone else in the graph.
        crowded = sum(1 for c in comps if holders_per_company.get(c, 0) >= 3)
        crowd_frac = (crowded / n) if n else 0.0
        strengths = [cg.strength(pk, q) for q in all_people if q != pk]
        strong_links = sum(1 for s in strengths if s >= 0.5)
        link_frac = strong_links / max(1, len(all_people) - 1)
        herding = round(min(1.0, 0.7 * crowd_frac + 6.0 * link_frac), 3)

        out[pk] = {"investment_visibility": vis, "herding_risk": herding,
                   "confirmed_company_count": n, "primary_source_fraction": round(tier_quality, 3)}
    return out


def score_people(con) -> dict[str, dict]:
    derived = compute_derived(con)
    dom_clusters = person_domain_clusters(con)
    results: dict[str, dict] = {}

    rows = [dict(r) for r in con.execute(
        "SELECT p.person_key, p.signal_class, p.archetypes, p.domains, s.* FROM people p"
        " LEFT JOIN people_scores s ON s.person_key = p.person_key")]
    # Median of each asserted component, used to stand in for a null score so a
    # person with "no public investing record" is not silently scored as zero.
    comp_vals: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        for c in COMPOSITE_WEIGHTS:
            if r.get(c) is not None:
                comp_vals[c].append(r[c])
    medians = {c: (sorted(v)[len(v) // 2] if v else 0) for c, v in comp_vals.items()}

    for r in rows:
        pk = r.get("person_key")
        d = derived.get(pk, {})
        parts, imputed = {}, []
        for c, w in COMPOSITE_WEIGHTS.items():
            v = r.get(c)
            if v is None:
                v = medians[c]
                imputed.append(c)
            parts[c] = v * w
        composite = sum(parts.values())          # 0-5
        cls = r.get("signal_class")
        weight = round((composite / 5.0) * CLASS_MULTIPLIER.get(cls, 0.5), 4)

        # GENERAL vs DOMAIN signal are deliberately separate: a world-class
        # researcher with two investments has a weak general signal and a very
        # strong domain one.
        general = round(0.45 * (r.get("early_stage_track_record") if r.get("early_stage_track_record")
                                is not None else 0)
                        + 0.30 * (r.get("access_score") or 0)
                        + 0.25 * d.get("investment_visibility", 0.0), 3)
        tech = r.get("technical_intelligence_score")
        dom_signal = {}
        for cluster in dom_clusters.get(pk, set()):
            dom_signal[cluster] = round(min(5.0,
                0.55 * (tech or 0) + 0.30 * (r.get("access_score") or 0)
                + 0.15 * (r.get("independence_score") or 0)), 3)

        con.execute(
            "UPDATE people_scores SET investment_visibility=?, herding_risk=?,"
            " general_investment_signal=?, domain_information_signal=?, person_weight=?,"
            " score_method_version=? WHERE person_key=?",
            (d.get("investment_visibility"), d.get("herding_risk"), general,
             json.dumps(dom_signal), weight, METHOD_VERSION, pk))
        results[pk] = {
            "person_weight": weight, "composite": round(composite, 3),
            "general_investment_signal": general, "domain_information_signal": dom_signal,
            "imputed_components": imputed,
            "is_technical_elite": is_technical_elite(tech, json.loads(r.get("archetypes") or "[]")),
            "domain_clusters": sorted(dom_clusters.get(pk, set())),
            **d,
        }
    con.commit()
    return results


def person_outcomes(con) -> int:
    """Failure / survivorship metrics per person, computed only from what the
    graph actually knows. Where disclosure is incomplete the fields stay NULL
    and disclosure_completeness says so."""
    n = 0
    status_by_company = {r["company_id"]: (r["current_status"] or "UNKNOWN")
                         for r in con.execute("SELECT company_id, current_status FROM companies")}
    val_by_company = {r["company_id"]: r["valuation_usd"] for r in con.execute(
        "SELECT company_id, valuation_usd FROM valuations WHERE is_current_best=1")}
    by_person: dict[str, set[str]] = defaultdict(set)
    for r in con.execute("SELECT person_key, company_id FROM person_company_edges"
                         " WHERE is_confirmed=1"):
        by_person[r["person_key"]].add(r["company_id"])

    for pk, comps in by_person.items():
        statuses = [status_by_company.get(c, "UNKNOWN") for c in comps]
        known = [s for s in statuses if s != "UNKNOWN"]
        failures = sum(1 for s in statuses if s in ("SHUT_DOWN", "BANKRUPT"))
        exits = sum(1 for s in statuses if s in ("ACQUIRED", "MERGED", "OPERATING_PUBLIC"))
        outliers = sum(1 for c in comps if (val_by_company.get(c) or 0) >= 5_000_000_000)
        coverage = len(known) / len(comps) if comps else 0.0
        completeness = ("SUFFICIENT" if coverage >= 0.8 else
                        "PARTIAL" if coverage >= 0.4 else "INSUFFICIENT")
        reliable = completeness == "SUFFICIENT"
        con.execute(
            "INSERT OR REPLACE INTO person_outcomes (person_key, number_verified_investments,"
            " number_major_outliers, number_exits, number_failures, number_shutdowns,"
            " number_down_rounds, hit_rate_proxy, early_entry_outlier_score,"
            " disclosure_completeness, reliability_caveat) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (pk, len(comps), outliers, exits if reliable else None,
             failures if reliable else None, failures if reliable else None, None,
             round(outliers / len(comps), 4) if (comps and reliable) else None, None,
             completeness,
             "Outcome counts are suppressed where company status is known for <80% of the "
             "person's confirmed companies; absence of a recorded failure is NOT evidence "
             "of no failure. Angel losses are systematically under-reported."))
        n += 1
    con.commit()
    return n
