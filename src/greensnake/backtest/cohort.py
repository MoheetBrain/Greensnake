"""The backtest cohort: winners AND a matched set of failures/mediocre outcomes.

SURVIVORSHIP DISCIPLINE. Studying only OpenAI/SpaceX/Stripe proves nothing --
famous winners have famous investors by definition. The cohort therefore pairs
every winner class with companies that had comparable elite backing and did NOT
become enormous: shutdowns, fire-sale acquisitions, down rounds and stagnation.

Outcome labels are FACTS about what happened and must be sourced in the company
record (`current_status`) or in the cohort note. A company whose fate the graph
cannot establish is labelled UNRESOLVED rather than guessed.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from .historical import discrimination, run_cohort

DEFAULT_DATES = ["2016-01", "2018-01", "2020-01", "2022-01", "2024-01", "2026-01"]


def load_cohort(con, path: Path) -> list[dict]:
    """Resolve cohort company names to company_ids already in the graph."""
    if not path.exists():
        return []
    doc = yaml.safe_load(path.read_text()) or {}
    from ..entity_resolution.dedupe import tight_key
    by_key = {tight_key(r["canonical_name"]): r["company_id"]
              for r in con.execute("SELECT company_id, canonical_name FROM companies")}
    for r in con.execute("SELECT alias_raw, company_id FROM company_aliases"):
        by_key.setdefault(tight_key(r["alias_raw"]), r["company_id"])

    out, missing = [], []
    for c in doc.get("cohort", []):
        cid = by_key.get(tight_key(c["name"]))
        if cid is None:
            missing.append(c["name"])
            continue
        out.append({"company_id": cid, "name": c["name"],
                    "outcome_label": c.get("outcome", "UNRESOLVED"),
                    "note": c.get("note")})
    return out, missing


def run_default_backtest(con, root: Path) -> dict:
    path = root / "research" / "companies" / "backtest_cohort.yaml"
    loaded = load_cohort(con, path)
    if not loaded:
        return {"n_companies": 0, "n_dates": 0, "n_snapshots": 0, "missing": []}
    cohort, missing = loaded
    dates = DEFAULT_DATES
    snaps = run_cohort(con, cohort, dates)
    disc = discrimination(snaps)
    name_by_id = {c["company_id"]: c["name"] for c in cohort}
    for s in snaps:
        s["company"] = name_by_id.get(s["company_id"], s["company_id"])
    (root / "reports").mkdir(exist_ok=True)
    (root / "reports" / "backtest_snapshots.json").write_text(
        json.dumps({"dates": dates, "snapshots": snaps, "discrimination": disc,
                    "cohort_not_in_graph": missing}, indent=2))
    return {"n_companies": len(cohort), "n_dates": len(dates),
            "n_snapshots": len(snaps), "missing": missing, "discrimination": disc}
