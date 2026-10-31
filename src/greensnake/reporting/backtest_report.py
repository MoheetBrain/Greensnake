"""BACKTEST.md -- did the graph see these companies before the market did?"""
from __future__ import annotations

import json
from pathlib import Path

from .report import fmt, fmt_usd

ORDER = {"WINNER": 0, "STRONG": 1, "MEDIOCRE": 2, "FAILURE": 3, "UNRESOLVED": 4}


def build(con, root: Path, out: Path) -> None:
    snap_path = root / "reports" / "backtest_snapshots.json"
    L = ["# HISTORICAL BACKTEST AND NEGATIVE CONTROLS", ""]
    if not snap_path.exists():
        (out / "BACKTEST.md").write_text("\n".join(L + ["_Not yet run._"]) + "\n")
        return
    doc = json.loads(snap_path.read_text())
    snaps, dates, disc = doc["snapshots"], doc["dates"], doc["discrimination"]
    missing = doc.get("cohort_not_in_graph", [])

    L += [
        "## How this test is constructed", "",
        "Every snapshot is computed **two ways**, because an edge can be true in 2016 and "
        "only become public in a 2021 filing. Counting the latter as visible in 2016 would "
        "be cheating.", "",
        "| view | definition | use |",
        "|---|---|---|",
        "| `AS_INVESTED` | `investment_date ≤ T` | what was **true** at T. Upper bound, contaminated by hindsight. |",
        "| `AS_KNOWABLE` | `investment_date ≤ T` **and** earliest source publication `≤ T` | what a researcher running this system at T could actually have **seen**. |",
        "| `upper bound` | AS_KNOWABLE + edges whose source carries no publication date | the most it could have been. |",
        "",
        "**Only `AS_KNOWABLE` is a legitimate backtest number**, and it is a **strict lower "
        "bound**: many sources (portfolio pages, personal investment lists, SEC filing "
        "indexes) carry no publication date at all, so an edge that was genuinely public "
        "at T is excluded from it. Those edges are counted separately, and the true value "
        "lies between AS_KNOWABLE and the upper bound. Where the two are far apart the "
        "test is uninformative and says so rather than pretending otherwise.", "",
        "Edges with no `investment_date` are excluded from both rather than imputed; "
        "`temporal coverage` below shows what fraction of each company's confirmed edges "
        "the test could actually use.", "",
        "## Cohort coverage", "",
    ]
    by_outcome: dict[str, set] = {}
    for s in snaps:
        by_outcome.setdefault(s["outcome_label"], set()).add(s["company"])
    L += ["| outcome | companies in graph |", "|---|---|"]
    for lab in sorted(by_outcome, key=lambda x: ORDER.get(x, 9)):
        L.append(f"| `{lab}` | {len(by_outcome[lab])} |")
    if missing:
        L += ["", f"**{len(missing)} cohort companies carry no confirmed edge in the graph "
                  f"and are therefore absent from this test**: " + ", ".join(sorted(missing)),
              "", "This is a collection gap, not a finding about those companies. It biases "
                  "the test toward whichever arm happens to be better covered, which is why "
                  "the discrimination result below is reported with that caveat attached."]
    L += ["", "---", "", "## Snapshots", ""]

    by_company: dict[str, list] = {}
    for s in snaps:
        by_company.setdefault(s["company"], []).append(s)
    for company in sorted(by_company, key=lambda c: (ORDER.get(by_company[c][0]["outcome_label"], 9),
                                                     c)):
        rows = sorted(by_company[company], key=lambda s: s["as_of_date"])
        lab = rows[0]["outcome_label"]
        cov = rows[0]["temporal_coverage"]
        L += [f"### {company} — `{lab}`", "",
              f"_{rows[0]['total_confirmed_edges_now']} confirmed edges now; "
              f"temporal coverage {fmt(cov, 2) if cov is not None else '—'} "
              f"({rows[0]['undated_edges_excluded']} undated edges excluded)_", "",
              "| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |",
              "|---|---|---|---|---|---|---|"]
        for s in rows:
            v = s["valuation_at_date"]
            who = ", ".join(p["name"] or p["person_key"] for p in s["as_knowable"]["people"])
            L.append(f"| {s['as_of_date']} | **{s['as_knowable']['count']}** "
                     f"| {s.get('knowable_upper_bound', s['as_knowable']['count'])} "
                     f"| {s['as_invested']['count']} | {s['hindsight_gap']} "
                     f"| {fmt_usd(v['valuation_usd']) if v else '—'} | {who or '—'} |")
        L.append("")

    L += ["---", "", "## Discrimination: do winners separate from failures?", "",
          "`AS_KNOWABLE` overlap by outcome group at each date.", ""]
    for d in dates:
        row = disc.get(d, {})
        groups = {k: v for k, v in row.items() if not k.startswith("_")}
        if not groups:
            continue
        L += [f"**{d}**", "", "| outcome | n | mean | median | max | with zero overlap |",
              "|---|---|---|---|---|---|"]
        for lab in sorted(groups, key=lambda x: ORDER.get(x, 9)):
            g = groups[lab]
            L.append(f"| `{lab}` | {g['n']} | {fmt(g['mean'])} | {g['median']} | {g['max']} "
                     f"| {g['zero_overlap']} |")
        sep = row.get("_separation_winner_minus_failure")
        L += ["", f"_winner mean − failure mean: **{fmt(sep) if sep is not None else '—'}**_", ""]

    L += ["---", "", "## How to read this", "",
          "`ANALYSIS` — with cohorts this size the separation figures are **descriptive, "
          "not a significance test**. Three things must hold before elite overlap can be "
          "called predictive, and they are not yet all satisfied here:", "",
          "1. **Both arms need comparable edge coverage.** The research workstreams were "
          "pointed at people, and people's portfolios are documented through their *wins*. "
          "Failures are systematically under-collected, which inflates any measured "
          "separation. Fixing this requires collecting failure edges deliberately, not "
          "waiting for them to appear.",
          "2. **The `AS_KNOWABLE` view must carry the result.** If separation exists only "
          "in `AS_INVESTED`, the signal is retrospective and untradeable.",
          "3. **Correlation adjustment must not erase it.** If independence-adjusted "
          "overlap separates the arms no better than raw overlap does, what looked like "
          "many independent signals was one network.", "",
          "The negative controls in `SECONDARY_QUESTIONS.md` question 14 list the companies "
          "that had elite backing and still failed. Those are the rows that keep this "
          "honest.", ""]
    (out / "BACKTEST.md").write_text("\n".join(L) + "\n")
