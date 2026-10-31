"""Company overlap scoring. METHOD VERSION: company-score-v1.

FACT              raw_overlap_count, strict/broad counts, the people_list.
DERIVED           weighted_person_score, independence_adjusted_score, densities.
INTERPRETATION    what any of it means. Not computed here.

Double-count guard: a person contributes ONCE per company, using their single
strongest edge, no matter how many rounds they participated in. Multiple rounds
are preserved as separate edge rows for temporal analysis, but never inflate a
count or a score.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import date

from ..graph.correlation import (CorrelationGraph, independence_adjusted,
                                 person_domain_clusters, person_primary_cluster)
from ..scoring.people import is_technical_elite
from ..valuation.current import assign_tier, parse_partial_date

METHOD_VERSION = "company-score-v1"
DELTA_DEFAULT = 0.35


def _months_ago(as_of: date, months: int) -> date:
    y, m = as_of.year, as_of.month - months
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, min(as_of.day, 28))


def score_companies(con, as_of: date | None = None, delta: float = DELTA_DEFAULT) -> int:
    as_of = as_of or date.today()
    cg = CorrelationGraph(con)
    dom_clusters = person_domain_clusters(con)
    primary_cluster = person_primary_cluster(con)

    people = {r["person_key"]: dict(r) for r in con.execute(
        "SELECT p.person_key, p.full_name, p.signal_class, p.archetypes, p.domains,"
        " s.person_weight, s.technical_intelligence_score, s.capital_flexibility"
        " FROM people p LEFT JOIN people_scores s ON s.person_key=p.person_key")}

    best_val = {r["company_id"]: dict(r) for r in con.execute(
        "SELECT company_id, valuation_usd, valuation_type, valuation_date,"
        " valuation_confidence, staleness_band FROM valuations WHERE is_current_best=1")}

    tier_rank = {"TIER_1_PRIMARY": 3, "TIER_2_SECONDARY": 2, "TIER_3_DATABASE": 1}
    best_tier: dict[str, str] = {}
    for r in con.execute(
            "SELECT e.company_id, s.tier FROM person_company_edges e"
            " JOIN sources s ON s.parent_kind='edge' AND s.parent_id=e.edge_id"
            " WHERE e.is_confirmed=1"):
        cur = best_tier.get(r["company_id"])
        if cur is None or tier_rank.get(r["tier"], 0) > tier_rank.get(cur, 0):
            best_tier[r["company_id"]] = r["tier"]

    # --- collapse edges to one contribution per (company, person) -------------
    per_company: dict[str, dict[str, dict]] = defaultdict(dict)
    for r in con.execute(
            "SELECT edge_id, company_id, person_key, relationship_type, overlap_class,"
            " edge_weight, investment_date, entry_valuation_usd, verification_status"
            " FROM person_company_edges WHERE is_confirmed=1"):
        slot = per_company[r["company_id"]].setdefault(r["person_key"], {
            "relationship_types": [], "overlap_classes": [], "edge_ids": [],
            "max_edge_weight": 0.0, "dates": [], "entry_valuations": [],
            "verification_statuses": [],
        })
        slot["relationship_types"].append(r["relationship_type"])
        slot["overlap_classes"].append(r["overlap_class"])
        slot["edge_ids"].append(r["edge_id"])
        slot["verification_statuses"].append(r["verification_status"])
        slot["max_edge_weight"] = max(slot["max_edge_weight"], r["edge_weight"] or 0.0)
        if r["investment_date"]:
            slot["dates"].append(r["investment_date"])
        if r["entry_valuation_usd"]:
            slot["entry_valuations"].append((r["investment_date"], r["entry_valuation_usd"]))

    con.execute("DELETE FROM company_scores")
    n = 0
    for cid, members in per_company.items():
        keys = sorted(members)
        contrib = {}
        for pk in keys:
            pw = (people.get(pk, {}) or {}).get("person_weight")
            contrib[pk] = (pw if pw is not None else 0.0) * members[pk]["max_edge_weight"]

        strict = sum(1 for pk in keys if "STRICT" in members[pk]["overlap_classes"])
        broad = sum(1 for pk in keys if {"STRICT", "BROAD"} & set(members[pk]["overlap_classes"]))
        info = len(keys)                     # any confirmed relationship
        raw = info                           # raw == info-network count by construction

        weighted = sum(contrib.values())
        founders_of_this = {pk for pk in keys
                            if "FOUNDER_EQUITY" in members[pk]["relationship_types"]}
        clusters = cg.clusters(keys, exclude_company=cid,        # leave-one-out
                               co_founders=founders_of_this)
        ia = independence_adjusted(clusters, contrib, delta)
        ia0 = independence_adjusted(clusters, contrib, 0.0)
        ia1 = independence_adjusted(clusters, contrib, 1.0)

        arche = {pk: json.loads((people.get(pk) or {}).get("archetypes") or "[]") for pk in keys}
        founders = sum(1 for pk in keys if "FOUNDER_OPERATOR" in arche[pk])
        pros = sum(1 for pk in keys if "PROFESSIONAL_INVESTOR" in arche[pk])
        specialists = sum(1 for pk in keys
                          if (people.get(pk) or {}).get("signal_class") == "DOMAIN_SPECIALIST")
        techs = [pk for pk in keys if is_technical_elite(
            (people.get(pk) or {}).get("technical_intelligence_score"), arche[pk])]
        # PROXY, not a sourced net-worth claim: founder-operators whose
        # capital_flexibility band is 5 (effectively unconstrained personal capital).
        big_founders = sum(1 for pk in keys if "FOUNDER_OPERATOR" in arche[pk]
                           and ((people.get(pk) or {}).get("capital_flexibility") or 0) >= 5)

        # Cross-domain diversity counts ONE primary lens per person, so a few
        # multi-domain people cannot manufacture apparent breadth.
        dcl: dict[str, float] = {}
        for pk in keys:
            d = primary_cluster.get(pk, "OTHER")
            dcl[d] = max(dcl.get(d, 0.0), contrib[pk])
        cross_domain = round(sum(dcl.values()), 4)
        tech_score = round(sum(contrib[pk] for pk in techs), 4)

        bv = best_val.get(cid)
        val = bv["valuation_usd"] if bv else None
        tier = assign_tier(val)
        logv = math.log(1.0 + val) if val is not None else None
        dens = (round(weighted / logv, 5) if logv else None)
        tdens = (round(tech_score / logv, 5) if logv else None)
        idens = (round(ia / logv, 5) if logv else None)

        # --- temporal (dated edges only; undated edges are EXCLUDED) ----------
        first_dates = {pk: min(members[pk]["dates"]) for pk in keys if members[pk]["dates"]}
        dated_n = len(first_dates)
        cuts = {"24": _months_ago(as_of, 24), "12": _months_ago(as_of, 12),
                "6": _months_ago(as_of, 6)}
        counts = {k: sum(1 for d in first_dates.values() if parse_partial_date(d) <= cut)
                  for k, cut in cuts.items()}
        now_ct = dated_n
        earliest = min(first_dates.values()) if first_dates else None
        entry_val = None
        if first_dates:
            cands = [(d, v) for pk in keys for (d, v) in members[pk]["entry_valuations"] if d]
            if cands:
                entry_val = min(cands, key=lambda x: parse_partial_date(x[0]))[1]
        multiple = (round(val / entry_val, 3) if (val and entry_val) else None)

        people_list = []
        for pk in sorted(keys, key=lambda k: -contrib[k]):
            m = members[pk]
            people_list.append({
                "person_key": pk,
                "name": (people.get(pk) or {}).get("full_name"),
                "signal_class": (people.get(pk) or {}).get("signal_class"),
                "relationship_types": sorted(set(m["relationship_types"])),
                "strongest_overlap_class": ("STRICT" if "STRICT" in m["overlap_classes"]
                                            else "BROAD" if "BROAD" in m["overlap_classes"]
                                            else "INFO_NETWORK"),
                "verification_statuses": sorted(set(m["verification_statuses"])),
                "earliest_investment_date": first_dates.get(pk),
                "person_weight": (people.get(pk) or {}).get("person_weight"),
                "contribution": round(contrib[pk], 4),
                "technical_elite": pk in techs,
                "primary_cluster": primary_cluster.get(pk, "OTHER"),
                "domain_clusters": sorted(dom_clusters.get(pk, {"OTHER"})),
                "edge_ids": m["edge_ids"],
            })

        con.execute(
            "INSERT INTO company_scores (company_id, best_valuation_usd, best_valuation_date,"
            " best_valuation_type, best_valuation_confidence, staleness_band, valuation_tier,"
            " confirmed_person_count_strict, confirmed_person_count_broad,"
            " information_network_count, raw_overlap_count, weighted_person_score,"
            " independence_adjusted_score, independence_adjusted_delta0,"
            " independence_adjusted_delta1, distinct_information_clusters,"
            " number_of_founder_operators, number_of_technical_people,"
            " number_of_professional_investors, number_of_billionaire_founders,"
            " number_of_domain_specialists, distinct_domains_represented, cross_domain_score,"
            " technical_elite_score, best_source_tier, technical_elite_count, elite_density,"
            " technical_elite_density, independent_signal_density, dated_edge_person_count,"
            " elite_connections_24m_ago, elite_connections_12m_ago, elite_connections_6m_ago,"
            " elite_connections_now, elite_network_momentum_12m, elite_network_momentum_6m,"
            " earliest_elite_entry_date, valuation_at_earliest_elite_entry,"
            " current_to_entry_multiple, people_list)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (cid, val, bv["valuation_date"] if bv else None,
             bv["valuation_type"] if bv else None, bv["valuation_confidence"] if bv else None,
             bv["staleness_band"] if bv else None, tier, strict, broad, info, raw,
             round(weighted, 4), round(ia, 4), round(ia0, 4), round(ia1, 4), len(clusters),
             founders, len(techs), pros, big_founders, specialists, len(dcl), cross_domain,
             tech_score, best_tier.get(cid), len(techs), dens, tdens, idens, dated_n,
             counts["24"], counts["12"], counts["6"], now_ct,
             now_ct - counts["12"], now_ct - counts["6"],
             earliest, entry_val, multiple, json.dumps(people_list)))
        n += 1
    con.commit()
    return n
