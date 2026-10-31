#!/usr/bin/env python3
"""Rebuild elite_graph.sqlite from the raw research batches, end to end.

    python3 scripts/build_graph.py                # full rebuild
    python3 scripts/build_graph.py --check-urls   # also verify source liveness
    python3 scripts/build_graph.py --delta 0.5    # different independence discount

Idempotent and deterministic: the database is a DERIVED artefact. The durable
assets are research/batches/ (evidence) and research/people/ (universe design).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from greensnake.core.db import init_db                      # noqa: E402
from greensnake.ingestion.loader import Ingestor            # noqa: E402
from greensnake.valuation.current import (                  # noqa: E402
    entry_multiples, resolve_current_valuations)
from greensnake.graph.correlation import derive_co_investment  # noqa: E402
from greensnake.scoring.people import person_outcomes, score_people  # noqa: E402
from greensnake.scoring.company import score_companies      # noqa: E402
from greensnake.verification import quality, url_check      # noqa: E402
from greensnake.verification.validate import run_all        # noqa: E402
from greensnake.reporting.exports import export_all         # noqa: E402
from greensnake.reporting.report import generate_all        # noqa: E402
from greensnake.backtest.cohort import run_default_backtest # noqa: E402

DB = ROOT / "database" / "elite_graph.sqlite"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--delta", type=float, default=0.35,
                    help="independence discount for same-network co-investors (default 0.35)")
    ap.add_argument("--check-urls", action="store_true",
                    help="HTTP-check every source URL (slow; run before publishing)")
    ap.add_argument("--url-limit", type=int, default=None)
    ap.add_argument("--as-of", default=date.today().isoformat())
    args = ap.parse_args()
    as_of = date.fromisoformat(args.as_of)

    print(f"[1/9] init database -> {DB}")
    con = init_db(DB, fresh=True)

    print("[2/9] load people universe")
    ing = Ingestor(con, ROOT / "data" / "company_aliases.yaml",
                   ROOT / "data" / "processed" / "ingest_rejects.jsonl")
    ing.load_people_universe(ROOT / "research" / "people" / "people_universe.yaml")

    print("[3/9] ingest research batches")
    batches = sorted(p for p in (ROOT / "research" / "batches").iterdir() if p.is_dir())
    for b in batches:
        ing.load_batch(b)
        print(f"        {b.name}")
    ing.finalise_companies()
    ing.write_reject_log()
    print(f"        stats: {json.dumps(ing.stats, sort_keys=True)}")
    if ing.rejects:
        print(f"        {len(ing.rejects)} record(s) REJECTED at ingest -> "
              f"data/processed/ingest_rejects.jsonl")

    print("[4/9] resolve current valuations and tiers")
    vals = resolve_current_valuations(con, as_of=as_of)
    n_mult = entry_multiples(con)
    print(f"        {len(vals)} companies with a current valuation; "
          f"{n_mult} edges with an entry multiple")

    print("[5/9] derive person<->person co-investment links")
    derived = derive_co_investment(con)
    print(f"        {len(derived)} derived co-investment links")

    print("[6/9] score people")
    ps = score_people(con)
    person_outcomes(con)
    print(f"        {len(ps)} people scored")

    print(f"[7/9] score companies (independence delta={args.delta})")
    n = score_companies(con, as_of=as_of, delta=args.delta)
    print(f"        {n} companies scored")

    cached = url_check.load_cache(con, ROOT / "data" / "processed" / "url_liveness_cache.json")
    if cached:
        print(f"[7c] re-applied {cached} cached source-liveness results")

    if args.check_urls:
        print("[7b] checking source URL liveness")
        res = url_check.check_all(con, limit=args.url_limit)
        print(f"        checked {res['checked']}, resolving {res['resolving']}, "
              f"failing {res['failing']}")
        url_check.save_cache(con, ROOT / "data" / "processed" / "url_liveness_cache.json")

    print("[8/9] run integrity tests")
    results = run_all(con)
    for r in results:
        mark = {"PASS": "  ok ", "WARN": " WARN", "FAIL": " FAIL"}[r["status"]]
        print(f"      {mark} {r['test_id']} {r['name']}: {r['detail']}")
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "validation_results.json").write_text(json.dumps(results, indent=2))

    q = quality.build(con)
    grade, reasons = quality.completeness_assessment(q)
    q["data_completeness_assessment"] = grade
    q["data_completeness_reasons"] = reasons
    (ROOT / "reports" / "data_quality.json").write_text(json.dumps(q, indent=2))

    print("[8b] historical backtest and negative controls")
    bt = run_default_backtest(con, ROOT)
    print(f"        {bt['n_companies']} cohort companies x {bt['n_dates']} dates "
          f"= {bt['n_snapshots']} snapshots")

    print("[9/9] export CSVs")
    counts = export_all(con, ROOT / "data" / "exports")
    for k, v in sorted(counts.items()):
        print(f"        {k:34s} {v:6d} rows")

    names = generate_all(con, q, results, ROOT / "reports", root=ROOT)
    print(f"        reports: {', '.join(names)}")

    con.execute("INSERT OR REPLACE INTO run_metadata (key,value) VALUES (?,?)",
                ("built_at", date.today().isoformat()))
    con.execute("INSERT OR REPLACE INTO run_metadata (key,value) VALUES (?,?)",
                ("independence_delta", str(args.delta)))
    con.execute("INSERT OR REPLACE INTO run_metadata (key,value) VALUES (?,?)",
                ("data_completeness", grade))
    con.commit()

    failures = [r for r in results if r["status"] == "FAIL"]
    print(f"\nDATA COMPLETENESS: {grade}")
    print(f"integrity: {len(results) - len(failures)}/{len(results)} passing")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
