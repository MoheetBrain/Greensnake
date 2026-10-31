"""OPEN_WORK.md -- what is unresolved, and what was investigated and killed.

These two tables are as much a deliverable as the rankings. The research queue
stops uncertainty silently becoming fact; the rejected table stops a bad claim
being rediscovered and promoted months later by someone who does not know it was
already checked.
"""
from __future__ import annotations

from pathlib import Path


def _q(con, sql, params=()):
    return [dict(r) for r in con.execute(sql, params)]


def build(con, out: Path) -> None:
    q = _q(con, "SELECT * FROM research_queue ORDER BY CASE priority WHEN 'HIGH' THEN 0"
                " WHEN 'MEDIUM' THEN 1 ELSE 2 END, raised_by")
    rej = _q(con, "SELECT * FROM rejected_edges ORDER BY rejected_by, person_key")
    by_pri: dict[str, int] = {}
    for r in q:
        by_pri[r["priority"] or "UNSET"] = by_pri.get(r["priority"] or "UNSET", 0) + 1

    L = ["# OPEN WORK — UNRESOLVED CLAIMS AND REJECTED CLAIMS", "",
         f"**{len(q)} unresolved claims · {len(rej)} claims investigated and rejected**", "",
         "Neither table is an appendix. The queue is what stops uncertainty silently "
         "becoming fact; the rejected table is what stops a killed claim being "
         "rediscovered and promoted by someone who does not know it was already checked.", "",
         "Full data: `data/exports/research_queue.csv`, `data/exports/rejected_edges.csv`.", "",
         "## Unresolved claims by priority", "", "| priority | n |", "|---|---|"]
    for p in ("HIGH", "MEDIUM", "LOW", "UNSET"):
        if by_pri.get(p):
            L.append(f"| `{p}` | {by_pri[p]} |")

    L += ["", "## HIGH-priority unresolved claims", "",
          "These are the highest-value next research actions: each is a specific claim "
          "with a named next source to check.", "",
          "| claim | why unresolved | next source | raised by |", "|---|---|---|---|"]
    for r in [x for x in q if x["priority"] == "HIGH"]:
        L.append(f"| {(r['claim'] or '')[:150]} | {(r['reason_unresolved'] or '')[:190]} "
                 f"| {(r['next_source_to_check'] or '—')[:110]} | `{r['raised_by']}` |")

    L += ["", "## MEDIUM-priority unresolved claims", "",
          "| claim | why unresolved | next source |", "|---|---|---|"]
    for r in [x for x in q if x["priority"] == "MEDIUM"][:60]:
        L.append(f"| {(r['claim'] or '')[:130]} | {(r['reason_unresolved'] or '')[:150]} "
                 f"| {(r['next_source_to_check'] or '—')[:90]} |")

    L += ["", "---", "", "## Rejected claims", "",
          "Relationships that were investigated and turned out **not** to be supported. "
          "The commonest failure mode by far is the one this project was built to catch: "
          "a firm invested, and the individual got the credit.", "",
          "| person | company | suspected | why rejected | checked by |", "|---|---|---|---|---|"]
    for r in rej:
        L.append(f"| `{r['person_key'] or '—'}` | {r['company_name'] or '—'} "
                 f"| `{r['suspected_relationship'] or '—'}` "
                 f"| {(r['reason_rejected'] or '')[:230]} | `{r['rejected_by']}` |")
    (out / "OPEN_WORK.md").write_text("\n".join(L) + "\n")
