#!/usr/bin/env python3
"""Compare each person's PRIOR signal_class against what the graph actually shows.

signal_class was set before any research, from public reputation. Now that the
edges exist, two derived quantities can test it:

  investment_visibility  can this person's portfolio actually be reconstructed?
  herding_risk           is their book crowded with the rest of the pool?

This script does NOT edit the universe. It proposes revisions with reasons, for
a human to accept or reject -- a scoring layer that silently rewrites its own
inputs is not auditable.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from greensnake.core.db import connect  # noqa: E402

ORDER = ["LOW_SIGNAL_OR_POOR_VISIBILITY", "WATCHLIST", "DOMAIN_SPECIALIST",
         "EXTENDED_SIGNAL", "CORE_HIGH_SIGNAL"]


def main() -> int:
    con = connect(ROOT / "database" / "elite_graph.sqlite")
    rows = [dict(r) for r in con.execute(
        "SELECT p.person_key, p.full_name, p.signal_class, p.archetypes,"
        " s.investment_visibility v, s.herding_risk h, s.person_weight w,"
        " s.technical_intelligence_score tech, s.early_stage_track_record esr,"
        " o.number_verified_investments n, o.disclosure_completeness dc"
        " FROM people p LEFT JOIN people_scores s ON s.person_key=p.person_key"
        " LEFT JOIN person_outcomes o ON o.person_key=p.person_key")]

    proposals = []
    for r in rows:
        cls, v, n = r["signal_class"], r["v"] or 0.0, r["n"] or 0
        arch = json.loads(r["archetypes"] or "[]")
        tech = r["tech"] or 0
        why = None
        new = cls
        if cls == "CORE_HIGH_SIGNAL" and v <= 1.0:
            new, why = "WATCHLIST", (
                f"prior says core, but only {n} confirmed companies could be reconstructed "
                f"(visibility {v}). Their real activity is invisible to this method, so "
                f"weighting them as a core signal over-weights the little we can see.")
        elif cls == "CORE_HIGH_SIGNAL" and v <= 2.0 and n < 5:
            new, why = "EXTENDED_SIGNAL", (
                f"reconstructable book is thin ({n} companies, visibility {v}); the prior "
                f"outruns the evidence.")
        elif cls in ("WATCHLIST", "LOW_SIGNAL_OR_POOR_VISIBILITY") and v >= 3.0 and n >= 8:
            new, why = "EXTENDED_SIGNAL", (
                f"prior assumed poor visibility, but {n} confirmed companies were "
                f"reconstructed (visibility {v}). The pessimism was wrong.")
        elif (cls == "EXTENDED_SIGNAL" and tech >= 4
              and {"RESEARCH_SCIENTIST", "ACADEMIC"} & set(arch) and n and n <= 4):
            new, why = "DOMAIN_SPECIALIST", (
                f"technical band {tech} with a small book ({n}); the value here is domain "
                f"signal, not general investing signal, and the classes should say so.")
        if why:
            proposals.append({"person_key": r["person_key"], "name": r["full_name"],
                              "from": cls, "to": new, "reason": why,
                              "visibility": v, "confirmed_companies": n,
                              "herding_risk": r["h"]})

    out = [
        "# PEOPLE CLASSIFICATION REVIEW", "",
        "`signal_class` in `research/people/people_universe.yaml` is a **prior**, set from "
        "public reputation before any edge was collected. This file tests those priors "
        "against what the graph actually produced.", "",
        "Two derived quantities do the testing, and neither is hand-set:", "",
        "- **`investment_visibility` (0–5)** — how much of this person's portfolio could "
        "actually be reconstructed, from confirmed company count and the Tier-1 share of "
        "their evidence.",
        "- **`herding_risk` (0–1)** — how crowded their book is with the rest of the pool.",
        "",
        "**Nothing here is applied automatically.** A scoring layer that rewrites its own "
        "inputs is not auditable. These are proposals for a human.", "",
        "> An important asymmetry: low visibility is a statement about **the evidence**, not "
        "about the person. Several people were included precisely to measure how much this "
        "method cannot see. Demoting them is the method admitting its blind spot, not a "
        "judgement that they are unimportant.", "",
        f"## Proposed revisions ({len(proposals)})", "",
    ]
    if proposals:
        out += ["| person | from | to | visibility | confirmed cos | reason |",
                "|---|---|---|---|---|---|"]
        for p in sorted(proposals, key=lambda x: (ORDER.index(x["to"]), x["name"])):
            out.append(f"| **{p['name']}** | `{p['from']}` | `{p['to']}` | {p['visibility']} "
                       f"| {p['confirmed_companies']} | {p['reason']} |")
    else:
        out.append("_No prior was contradicted strongly enough to propose a change._")

    out += ["", "## Visibility distribution by prior class", "",
            "| prior class | n | median visibility | median confirmed companies | n with zero edges |",
            "|---|---|---|---|---|"]
    for cls in reversed(ORDER):
        grp = [r for r in rows if r["signal_class"] == cls]
        if not grp:
            continue
        vs = sorted((r["v"] or 0) for r in grp)
        ns = sorted((r["n"] or 0) for r in grp)
        zero = sum(1 for r in grp if not r["n"])
        out.append(f"| `{cls}` | {len(grp)} | {vs[len(vs)//2]} | {ns[len(ns)//2]} | {zero} |")

    out += ["", "## Most crowded books (highest herding risk)", "",
            "`ANALYSIS` — a crowded book is not a bad book. It means this person's "
            "positions carry less *independent* information, because the rest of the pool "
            "is already in them. The independence adjustment already discounts this at the "
            "company level; the column exists so the effect is visible at the person level "
            "too.", "",
            "| person | herding risk | visibility | confirmed companies |", "|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: -(x["h"] or 0))[:15]:
        out.append(f"| {r['full_name']} | {r['h']} | {r['v']} | {r['n'] or 0} |")

    out += ["", "## People the graph could not see at all", "",
            "`FACT` — tracked people with **no confirmed edge**. For the WATCHLIST and "
            "LOW_SIGNAL entries this was the expected result and is the finding: it "
            "calibrates the method's floor. For anyone else it is a coverage gap.", "",
            "| person | prior class | interpretation |", "|---|---|---|"]
    for r in sorted((r for r in rows if not r["n"]), key=lambda x: x["full_name"]):
        interp = ("expected — included to measure the visibility floor"
                  if r["signal_class"] in ("WATCHLIST", "LOW_SIGNAL_OR_POOR_VISIBILITY")
                  else "coverage gap — worth another pass")
        out.append(f"| {r['full_name']} | `{r['signal_class']}` | {interp} |")

    (ROOT / "docs" / "PEOPLE_CLASSIFICATION.md").write_text("\n".join(out) + "\n")
    print(f"{len(proposals)} revision(s) proposed -> docs/PEOPLE_CLASSIFICATION.md")
    for p in proposals:
        print(f"  {p['name']:26s} {p['from']:30s} -> {p['to']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
