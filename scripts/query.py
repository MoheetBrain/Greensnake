#!/usr/bin/env python3
"""Ask the graph a question from the command line.

    python3 scripts/query.py screen --tier A --min-people 3
    python3 scripts/query.py screen --max-valuation 500e6 --min-technical 2
    python3 scripts/query.py company "Granola"
    python3 scripts/query.py person "Elad Gil"
    python3 scripts/query.py edge <edge_id>          # walk back to the sources
    python3 scripts/query.py sql "SELECT ..."        # read-only escape hatch

Every screen prints the RAW factual count next to the derived scores, and every
row carries the ids needed to walk back to the evidence.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "elite_graph.sqlite"
TIERS = {"A": "TIER_A_UNDER_500M", "B": "TIER_B_500M_TO_1B", "C": "TIER_C_1B_TO_5B",
         "D": "TIER_D_5B_PLUS", "U": "TIER_U_UNKNOWN"}


def con():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def usd(v):
    if v is None:
        return "—"
    v = float(v)
    for d, s in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(v) >= d:
            return f"${v/d:,.2f}{s}"
    return f"${v:,.0f}"


def cmd_screen(a):
    where, params = ["1=1"], []
    if a.tier:
        where.append("cs.valuation_tier = ?"); params.append(TIERS[a.tier.upper()])
    if a.max_valuation is not None:
        where.append("cs.best_valuation_usd < ?"); params.append(float(a.max_valuation))
    if a.min_valuation is not None:
        where.append("cs.best_valuation_usd >= ?"); params.append(float(a.min_valuation))
    if a.min_people:
        where.append("cs.raw_overlap_count >= ?"); params.append(a.min_people)
    if a.min_strict:
        where.append("cs.confirmed_person_count_strict >= ?"); params.append(a.min_strict)
    if a.min_technical:
        where.append("cs.technical_elite_count >= ?"); params.append(a.min_technical)
    if a.min_clusters:
        where.append("cs.distinct_information_clusters >= ?"); params.append(a.min_clusters)
    if a.public_only:
        where.append("c.public_or_private = 'PUBLIC'")
    if a.sector:
        where.append("LOWER(COALESCE(c.industry_primary,'')) LIKE ?")
        params.append(f"%{a.sector.lower()}%")
    order = {"raw": "cs.raw_overlap_count", "strict": "cs.confirmed_person_count_strict",
             "weighted": "cs.weighted_person_score", "independence": "cs.independence_adjusted_score",
             "technical": "cs.technical_elite_score", "density": "cs.elite_density",
             "momentum": "cs.elite_network_momentum_12m"}[a.sort]
    rows = con().execute(
        f"SELECT c.canonical_name nm, c.company_id, cs.best_valuation_usd v, cs.valuation_tier t,"
        f" cs.raw_overlap_count raw, cs.confirmed_person_count_strict st, cs.technical_elite_count te,"
        f" cs.distinct_information_clusters cl, cs.weighted_person_score w,"
        f" cs.independence_adjusted_score ia, cs.people_list pl"
        f" FROM company_scores cs JOIN companies c USING(company_id)"
        f" WHERE {' AND '.join(where)} ORDER BY {order} DESC, cs.raw_overlap_count DESC"
        f" LIMIT {int(a.limit)}", params).fetchall()
    if not rows:
        print("no companies match that screen"); return
    print(f"{'company':34s} {'valuation':>11s} {'tier':5s} {'raw':>4s}{'strict':>7s}"
          f"{'tech':>5s}{'clust':>6s}{'weight':>8s}{'indep':>7s}  people")
    for r in rows:
        who = "; ".join(p["name"] or p["person_key"] for p in json.loads(r["pl"] or "[]")[:4])
        print(f"{r['nm'][:33]:34s} {usd(r['v']):>11s} {r['t'][5:6]:5s} {r['raw']:4d}{r['st']:7d}"
              f"{r['te']:5d}{r['cl']:6d}{r['w']:8.2f}{r['ia']:7.2f}  {who[:60]}")
    print(f"\n{len(rows)} row(s). Full data: data/exports/company_discovery.csv")


def cmd_company(a):
    c = con()
    r = c.execute("SELECT * FROM companies WHERE canonical_name = ? COLLATE NOCASE"
                  " OR company_id = ?", (a.name, a.name)).fetchone()
    if not r:
        like = c.execute("SELECT canonical_name FROM companies WHERE canonical_name LIKE ?"
                         " LIMIT 10", (f"%{a.name}%",)).fetchall()
        print(f"no exact match for {a.name!r}." +
              (" did you mean: " + ", ".join(x[0] for x in like) if like else ""))
        return
    cid = r["company_id"]
    s = c.execute("SELECT * FROM company_scores WHERE company_id=?", (cid,)).fetchone()
    print(f"\n{r['canonical_name']}  [{cid}]")
    print(f"  {r['public_or_private']}  {r['ticker'] or ''}  {r['industry_primary'] or '—'}"
          f"  {r['country'] or '—'}  status={r['current_status']}")
    if s:
        print(f"  valuation {usd(s['best_valuation_usd'])} ({s['best_valuation_type'] or '—'},"
              f" {s['best_valuation_date'] or '—'}, {s['staleness_band'] or '—'}) -> {s['valuation_tier']}")
        print(f"  FACT     raw={s['raw_overlap_count']} strict={s['confirmed_person_count_strict']}"
              f" broad={s['confirmed_person_count_broad']}")
        print(f"  DERIVED  weighted={s['weighted_person_score']:.2f}"
              f" independence_adjusted={s['independence_adjusted_score']:.2f}"
              f" clusters={s['distinct_information_clusters']}"
              f" domains={s['distinct_domains_represented']}"
              f" technical_elite={s['technical_elite_count']}")
        print("\n  connected people:")
        for p in json.loads(s["people_list"] or "[]"):
            print(f"    {p['name'] or p['person_key']:28s} {','.join(p['relationship_types']):34s}"
                  f" {p['strongest_overlap_class']:12s} {p.get('earliest_investment_date') or '—':10s}"
                  f" {'TECH' if p.get('technical_elite') else '    '}")
    print("\n  sources:")
    for x in c.execute("SELECT DISTINCT s.tier, s.url FROM sources s"
                       " JOIN person_company_edges e ON e.edge_id=s.parent_id"
                       " WHERE s.parent_kind='edge' AND e.company_id=? ORDER BY s.tier", (cid,)):
        print(f"    [{x['tier']}] {x['url']}")


def cmd_person(a):
    c = con()
    r = c.execute("SELECT p.*, s.* FROM people p LEFT JOIN people_scores s USING(person_key)"
                  " WHERE p.full_name = ? COLLATE NOCASE OR p.person_key = ?",
                  (a.name, a.name)).fetchone()
    if not r:
        like = c.execute("SELECT full_name FROM people WHERE full_name LIKE ? LIMIT 10",
                         (f"%{a.name}%",)).fetchall()
        print(f"no match for {a.name!r}." +
              (" did you mean: " + ", ".join(x[0] for x in like) if like else ""))
        return
    print(f"\n{r['full_name']}  [{r['person_key']}]  {r['signal_class']}")
    print(f"  {r['primary_affiliation']}")
    print(f"  ASSERTED  access={r['access_score']} technical={r['technical_intelligence_score']}"
          f" early_stage={r['early_stage_track_record']} network={r['founder_network_score']}"
          f" capital={r['capital_flexibility']} independence={r['independence_score']}")
    print(f"  DERIVED   visibility={r['investment_visibility']} herding={r['herding_risk']}"
          f" weight={r['person_weight']}")
    print(f"\n  {r['rationale']}\n")
    print("  confirmed relationships:")
    for x in c.execute(
            "SELECT c.canonical_name nm, e.relationship_type rt, e.overlap_class oc,"
            " e.investment_date d, cs.best_valuation_usd v, cs.valuation_tier t"
            " FROM person_company_edges e JOIN companies c USING(company_id)"
            " LEFT JOIN company_scores cs ON cs.company_id=e.company_id"
            " WHERE e.person_key=? AND e.is_confirmed=1 ORDER BY c.canonical_name",
            (r["person_key"],)):
        print(f"    {x['nm'][:34]:36s} {x['rt']:32s} {x['oc']:12s} {x['d'] or '—':10s}"
              f" {usd(x['v']):>10s}")


def cmd_edge(a):
    c = con()
    e = c.execute("SELECT e.*, p.full_name, co.canonical_name FROM person_company_edges e"
                  " JOIN people p USING(person_key) JOIN companies co USING(company_id)"
                  " WHERE e.edge_id=?", (a.edge_id,)).fetchone()
    if not e:
        print("no such edge"); return
    print(f"\n{e['full_name']} -> {e['canonical_name']}")
    print(f"  {e['relationship_type']}  via {e['investment_vehicle'] or '—'}"
          f"  {e['investment_date'] or 'undated'}  round={e['round_name'] or '—'}")
    print(f"  {e['verification_status']}  verified {e['date_verified']}  by {e['collected_by']}")
    if e["verification_notes"]:
        print(f"  note: {e['verification_notes']}")
    print("\n  evidence:")
    for s in c.execute("SELECT * FROM sources WHERE parent_kind='edge' AND parent_id=?",
                       (a.edge_id,)):
        live = ("resolves" if s["url_http_status"] and s["url_http_status"] < 400
                else f"HTTP {s['url_http_status']}" if s["url_http_status"] else "unchecked")
        print(f"    [{s['tier']}] {s['publisher'] or s['source_type']}  ({live})")
        print(f"      {s['url']}")
        print(f"      {s['evidence_summary']}")


def cmd_sql(a):
    q = a.query.strip()
    if not q.lower().startswith(("select", "with")):
        print("read-only: only SELECT / WITH queries are allowed"); return
    rows = con().execute(q).fetchall()
    if not rows:
        print("(no rows)"); return
    print(" | ".join(rows[0].keys()))
    for r in rows[:200]:
        print(" | ".join("" if v is None else str(v)[:60] for v in r))
    print(f"\n{len(rows)} row(s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("screen", help="filter companies")
    s.add_argument("--tier", choices=list(TIERS) + [t.lower() for t in TIERS])
    s.add_argument("--min-valuation", type=float); s.add_argument("--max-valuation", type=float)
    s.add_argument("--min-people", type=int); s.add_argument("--min-strict", type=int)
    s.add_argument("--min-technical", type=int); s.add_argument("--min-clusters", type=int)
    s.add_argument("--public-only", action="store_true"); s.add_argument("--sector")
    s.add_argument("--sort", default="raw",
                   choices=["raw", "strict", "weighted", "independence", "technical",
                            "density", "momentum"])
    s.add_argument("--limit", default=25); s.set_defaults(func=cmd_screen)
    p = sub.add_parser("company"); p.add_argument("name"); p.set_defaults(func=cmd_company)
    p = sub.add_parser("person"); p.add_argument("name"); p.set_defaults(func=cmd_person)
    p = sub.add_parser("edge"); p.add_argument("edge_id"); p.set_defaults(func=cmd_edge)
    p = sub.add_parser("sql"); p.add_argument("query"); p.set_defaults(func=cmd_sql)
    a = ap.parse_args()
    if not DB.exists():
        print(f"{DB} not found -- run scripts/build_graph.py first"); return 1
    a.func(a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
