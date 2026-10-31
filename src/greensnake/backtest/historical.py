"""Historical backtest: would this graph have surfaced these companies early?

THE HINDSIGHT PROBLEM
An edge can be true in 2016 but only become *public* in a 2021 S-1. Counting it
as visible in 2016 would be cheating. So every snapshot is computed two ways:

  AS_INVESTED  edges whose investment_date <= T.
               What was TRUE at T. Upper bound. Contaminated by hindsight.
  AS_KNOWABLE  edges where BOTH investment_date <= T AND the earliest source
               publication date <= T.
               What a researcher running this system at T could actually have
               SEEN. This is the honest backtest number, and it is a STRICT
               LOWER BOUND: an edge whose source carries no publication date is
               excluded from it, even though the relationship existed by T.
               Those are counted separately as `excluded_source_undated`, and
               `knowable_upper_bound` = AS_KNOWABLE + that count. The true value
               lies between the two.

The gap between the two is itself a finding: it measures how much of the signal
is only visible in retrospect. A strategy can only trade AS_KNOWABLE.

Edges with no investment_date are excluded from both. They are counted and
reported as `undated_excluded` so the coverage of every snapshot is visible.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import date

from ..valuation.current import parse_partial_date

OUTCOME_LABELS = {"WINNER", "STRONG", "MEDIOCRE", "FAILURE", "UNRESOLVED"}


def _edge_rows(con):
    """Every confirmed edge with its investment date and earliest source date."""
    rows = []
    for r in con.execute(
            "SELECT e.edge_id, e.company_id, e.person_key, e.relationship_type,"
            " e.overlap_class, e.investment_date, e.edge_weight,"
            " (SELECT MIN(s.published_date) FROM sources s WHERE s.parent_kind='edge'"
            "  AND s.parent_id=e.edge_id AND s.published_date IS NOT NULL) AS first_pub"
            " FROM person_company_edges e WHERE e.is_confirmed=1"):
        rows.append(dict(r))
    return rows


def snapshot(con, company_id: str, as_of: str, edges=None, people=None) -> dict:
    """Elite overlap for one company at one historical date, both views."""
    edges = edges if edges is not None else _edge_rows(con)
    people = people or {r["person_key"]: dict(r) for r in con.execute(
        "SELECT p.person_key, p.full_name, p.signal_class, s.person_weight"
        " FROM people p LEFT JOIN people_scores s ON s.person_key=p.person_key")}
    cut = parse_partial_date(as_of)

    mine = [e for e in edges if e["company_id"] == company_id]
    undated = [e for e in mine if not e["investment_date"]]
    dated = [e for e in mine if e["investment_date"]]

    invested, knowable, undated_source = {}, {}, {}
    for e in dated:
        if parse_partial_date(e["investment_date"]) > cut:
            continue
        pk = e["person_key"]
        invested.setdefault(pk, e)
        fp = e["first_pub"]
        if fp and parse_partial_date(fp) <= cut:
            knowable.setdefault(pk, e)
        elif not fp:
            # The relationship existed by T, but no source carries a publication
            # date, so we cannot say when it became public. Counted separately
            # rather than assumed either way.
            undated_source.setdefault(pk, e)

    def summarise(d):
        return {
            "count": len(d),
            "people": sorted(
                [{"person_key": pk,
                  "name": (people.get(pk) or {}).get("full_name"),
                  "signal_class": (people.get(pk) or {}).get("signal_class"),
                  "relationship_type": e["relationship_type"],
                  "overlap_class": e["overlap_class"],
                  "investment_date": e["investment_date"],
                  "first_public_source_date": e["first_pub"]}
                 for pk, e in d.items()],
                key=lambda x: (x["investment_date"] or "", x["name"] or "")),
            "weighted": round(sum((people.get(pk, {}).get("person_weight") or 0.0)
                                  * (e["edge_weight"] or 0.0) for pk, e in d.items()), 4),
        }

    val = None
    for r in con.execute(
            "SELECT valuation_usd, valuation_date, valuation_type FROM valuations"
            " WHERE company_id=? ORDER BY valuation_date DESC", (company_id,)):
        if parse_partial_date(r["valuation_date"]) <= cut:
            val = {"valuation_usd": r["valuation_usd"], "valuation_date": r["valuation_date"],
                   "valuation_type": r["valuation_type"]}
            break

    as_inv, as_know = summarise(invested), summarise(knowable)
    undated_n = len({k for k in undated_source if k not in knowable})
    return {
        "company_id": company_id, "as_of_date": as_of,
        "as_invested": as_inv, "as_knowable": as_know,
        "knowable_upper_bound": as_know["count"] + undated_n,
        "excluded_source_undated": undated_n,
        "hindsight_gap": as_inv["count"] - as_know["count"],
        "valuation_at_date": val,
        "undated_edges_excluded": len(undated),
        "total_confirmed_edges_now": len(mine),
        "temporal_coverage": (round(len(dated) / len(mine), 3) if mine else None),
    }


def run_cohort(con, cohort: list[dict], dates: list[str]) -> list[dict]:
    """cohort: [{company_id, outcome_label, note}]. Writes backtest_observations."""
    edges = _edge_rows(con)
    people = {r["person_key"]: dict(r) for r in con.execute(
        "SELECT p.person_key, p.full_name, p.signal_class, s.person_weight"
        " FROM people p LEFT JOIN people_scores s ON s.person_key=p.person_key")}
    con.execute("DELETE FROM backtest_observations")
    out = []
    for c in cohort:
        for d in dates:
            snap = snapshot(con, c["company_id"], d, edges=edges, people=people)
            snap["outcome_label"] = c.get("outcome_label", "UNRESOLVED")
            snap["note"] = c.get("note")
            con.execute(
                "INSERT OR REPLACE INTO backtest_observations (obs_id, company_id, as_of_date,"
                " valuation_usd, elite_people_count, people_list, outcome_label, notes)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (f"{c['company_id']}__{d}", c["company_id"], d,
                 (snap["valuation_at_date"] or {}).get("valuation_usd"),
                 snap["as_knowable"]["count"], json.dumps(snap["as_knowable"]["people"]),
                 c.get("outcome_label", "UNRESOLVED"),
                 f"as_invested={snap['as_invested']['count']}; "
                 f"hindsight_gap={snap['hindsight_gap']}; "
                 f"temporal_coverage={snap['temporal_coverage']}"))
            out.append(snap)
    con.commit()
    return out


def discrimination(snapshots: list[dict]) -> dict:
    """Does elite overlap actually separate winners from failures?

    Compares AS_KNOWABLE overlap between outcome groups at each date. With small
    cohorts this is descriptive, NOT a significance test, and is reported as such.
    """
    by_date: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for s in snapshots:
        by_date[s["as_of_date"]][s["outcome_label"]].append(s["as_knowable"]["count"])

    res = {}
    for d, groups in sorted(by_date.items()):
        row = {}
        for label, vals in sorted(groups.items()):
            vals_sorted = sorted(vals)
            row[label] = {
                "n": len(vals),
                "mean": round(sum(vals) / len(vals), 2) if vals else None,
                "median": vals_sorted[len(vals_sorted) // 2] if vals else None,
                "max": max(vals) if vals else None,
                "zero_overlap": sum(1 for v in vals if v == 0),
            }
        w = row.get("WINNER", {}).get("mean")
        f = row.get("FAILURE", {}).get("mean")
        row["_separation_winner_minus_failure"] = (round(w - f, 2)
                                                   if (w is not None and f is not None) else None)
        res[d] = row
    return res
