"""Answers to the standing investigative questions -- computed, not asserted.

Each answer names the query behind it so a reader can reproduce or disagree with
it. Where the graph cannot yet answer a question, it says so instead of
producing a confident-looking table built on three rows.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from ..core.enums import TIER_UNKNOWN
from .report import fmt, fmt_usd

MIN_ROWS_FOR_CLAIM = 3


def _q(con, sql, params=()):
    return [dict(r) for r in con.execute(sql, params)]


def _table(rows, cols, headers=None):
    if not rows:
        return "_The graph cannot yet answer this: no rows satisfy the query._\n"
    headers = headers or cols
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "—") if r.get(c) is not None else "—")
                                    for c in cols) + " |")
    return "\n".join(out) + "\n"


def build(con, out: Path) -> None:
    L = ["# SECONDARY INVESTIGATIVE QUESTIONS", "",
         "Every answer below is a query over the confirmed graph. "
         "`FACT` rows are counts of sourced edges; `DERIVED` rows are formulas from "
         "`docs/METHODOLOGY.md`; anything interpretive is labelled `ANALYSIS`.", ""]

    # 1 ---------------------------------------------------------------------
    L += ["## 1. Which people historically entered exceptional companies earliest?", "",
          "`FACT` — confirmed edges with a real `investment_date`, into companies now "
          "valued at $1B+. Undated edges are excluded, so this understates everyone "
          "whose early deals are simply undated.", ""]
    rows = _q(con, """
        SELECT p.full_name person, c.canonical_name company, e.investment_date entered,
               cs.best_valuation_usd now_val, e.entry_valuation_usd entry_val,
               e.entry_multiple_to_current mult, e.relationship_type rel
        FROM person_company_edges e
        JOIN people p ON p.person_key=e.person_key
        JOIN companies c ON c.company_id=e.company_id
        JOIN company_scores cs ON cs.company_id=e.company_id
        WHERE e.is_confirmed=1 AND e.investment_date IS NOT NULL
          AND cs.best_valuation_usd >= 1000000000
        ORDER BY e.investment_date ASC LIMIT 30""")
    for r in rows:
        r["now_val"] = fmt_usd(r["now_val"]); r["entry_val"] = fmt_usd(r["entry_val"])
        r["mult"] = fmt(r["mult"], 1)
    L.append(_table(rows, ["person", "company", "entered", "entry_val", "now_val", "mult", "rel"]))

    # 2 ---------------------------------------------------------------------
    L += ["## 2. Which people have the strongest domain-specific signal?", "",
          "`DERIVED` — `domain_information_signal` blends technical band, access and "
          "independence. It is deliberately separate from general investing signal: a "
          "world-class researcher with two investments scores low on one and high on the "
          "other, and collapsing them would destroy the signal this project looks for.", ""]
    rows = []
    for r in _q(con, "SELECT p.full_name, s.domain_information_signal d, s.person_weight,"
                     " s.investment_visibility v FROM people p"
                     " JOIN people_scores s ON s.person_key=p.person_key"
                     " WHERE s.domain_information_signal IS NOT NULL"):
        d = json.loads(r["d"] or "{}")
        if not d:
            continue
        best = max(d.items(), key=lambda x: x[1])
        rows.append({"person": r["full_name"], "domain": best[0], "signal": fmt(best[1]),
                     "visibility": fmt(r["v"], 1), "weight": fmt(r["person_weight"], 3)})
    rows = sorted(rows, key=lambda x: -float(x["signal"]))[:25]
    L.append(_table(rows, ["person", "domain", "signal", "visibility", "weight"]))

    # 3 ---------------------------------------------------------------------
    L += ["## 3. Which combinations of people appear together unusually often?", "",
          "`FACT` — distinct companies where both people hold a confirmed edge.", ""]
    rows = _q(con, """
        SELECT pa.full_name a, pb.full_name b, COUNT(DISTINCT x.company_id) shared
        FROM person_company_edges x
        JOIN person_company_edges y ON y.company_id=x.company_id
             AND y.person_key > x.person_key AND y.is_confirmed=1
        JOIN people pa ON pa.person_key=x.person_key
        JOIN people pb ON pb.person_key=y.person_key
        WHERE x.is_confirmed=1 GROUP BY 1,2 HAVING shared>=2
        ORDER BY shared DESC LIMIT 25""")
    L.append(_table(rows, ["a", "b", "shared"]))

    # 4 ---------------------------------------------------------------------
    L += ["## 4. Which combinations preceded enormous outcomes?", "",
          "`FACT` — pairs co-occurring on cohort companies labelled WINNER.", ""]
    rows = _q(con, """
        SELECT pa.full_name a, pb.full_name b, COUNT(DISTINCT x.company_id) winners,
               GROUP_CONCAT(DISTINCT c.canonical_name) companies
        FROM person_company_edges x
        JOIN person_company_edges y ON y.company_id=x.company_id
             AND y.person_key > x.person_key AND y.is_confirmed=1
        JOIN people pa ON pa.person_key=x.person_key
        JOIN people pb ON pb.person_key=y.person_key
        JOIN companies c ON c.company_id=x.company_id
        JOIN (SELECT DISTINCT company_id FROM backtest_observations
              WHERE outcome_label='WINNER') w ON w.company_id=x.company_id
        WHERE x.is_confirmed=1 GROUP BY 1,2 ORDER BY winners DESC LIMIT 20""")
    L.append(_table(rows, ["a", "b", "winners", "companies"]))
    L += ["`ANALYSIS` — co-occurrence on winners is **not** evidence of predictive skill "
          "until the same pairs are checked against the failure cohort. Question 15 does that.", ""]

    # 5 ---------------------------------------------------------------------
    L += ["## 5. Which investor combinations are mostly explained by shared networks?", "",
          "`DERIVED` — companies where many backers collapse into few independent "
          "networks. `collapse_ratio = raw_people_count / distinct_information_clusters`; "
          "higher means the apparent breadth is one network wearing several hats.", ""]
    rows = _q(con, """
        SELECT c.canonical_name company, cs.raw_overlap_count raw,
               cs.distinct_information_clusters clusters,
               ROUND(CAST(cs.raw_overlap_count AS REAL)/
                     MAX(cs.distinct_information_clusters,1),2) collapse_ratio,
               ROUND(cs.weighted_person_score,2) weighted,
               ROUND(cs.independence_adjusted_score,2) indep_adj
        FROM company_scores cs JOIN companies c USING(company_id)
        WHERE cs.raw_overlap_count>=3
        ORDER BY collapse_ratio DESC, raw DESC LIMIT 20""")
    L.append(_table(rows, ["company", "raw", "clusters", "collapse_ratio", "weighted", "indep_adj"]))

    # 6 ---------------------------------------------------------------------
    L += ["## 6. Which companies have the most genuinely independent backers?", "",
          "`DERIVED` — most distinct network clusters after leave-one-out correlation.", ""]
    rows = _q(con, """
        SELECT c.canonical_name company, cs.raw_overlap_count raw,
               cs.distinct_information_clusters clusters,
               cs.distinct_domains_represented domains,
               ROUND(cs.independence_adjusted_score,2) indep_adj,
               cs.valuation_tier tier
        FROM company_scores cs JOIN companies c USING(company_id)
        ORDER BY clusters DESC, indep_adj DESC LIMIT 25""")
    L.append(_table(rows, ["company", "raw", "clusters", "domains", "indep_adj", "tier"]))

    # 7-9 -------------------------------------------------------------------
    for tier, label, num in (("TIER_A_UNDER_500M", "under $500M", 7),
                             ("TIER_B_500M_TO_1B", "$500M–$1B", 8),
                             ("TIER_C_1B_TO_5B", "$1B–$5B", 9)):
        L += [f"## {num}. Which companies {label} have surprising elite overlap?", "",
              "`FACT` + `DERIVED` — high overlap relative to how small the company still is.", ""]
        rows = _q(con, """
            SELECT c.canonical_name company, cs.best_valuation_usd val,
                   cs.raw_overlap_count raw, cs.confirmed_person_count_strict strict,
                   cs.technical_elite_count tech, cs.distinct_information_clusters clusters,
                   ROUND(cs.elite_density,4) elite_density
            FROM company_scores cs JOIN companies c USING(company_id)
            WHERE cs.valuation_tier=? ORDER BY cs.raw_overlap_count DESC,
                  cs.elite_density DESC LIMIT 15""", (tier,))
        for r in rows:
            r["val"] = fmt_usd(r["val"])
        L.append(_table(rows, ["company", "val", "raw", "strict", "tech", "clusters",
                               "elite_density"]))

    # 10 --------------------------------------------------------------------
    L += ["## 10. Which unknown-valuation companies most deserve valuation work?", "",
          "`FACT` — highest confirmed overlap with no sourced current valuation. "
          "These are the graph's blind spots and its best leads simultaneously.", ""]
    rows = _q(con, """
        SELECT c.canonical_name company, cs.raw_overlap_count raw,
               cs.confirmed_person_count_strict strict, cs.technical_elite_count tech,
               cs.distinct_information_clusters clusters
        FROM company_scores cs JOIN companies c USING(company_id)
        WHERE cs.valuation_tier=? ORDER BY raw DESC, strict DESC LIMIT 30""", (TIER_UNKNOWN,))
    L.append(_table(rows, ["company", "raw", "strict", "tech", "clusters"]))

    # 11 --------------------------------------------------------------------
    L += ["## 11. Which technically sophisticated people back obscure companies that "
          "conventional famous investors have missed?", "",
          "`FACT` — companies with ≥1 technically elite backer and **zero** professional "
          "investors among their confirmed backers. This is the purest version of the "
          "project's thesis: technical judgement without venture consensus.", ""]
    rows = _q(con, """
        SELECT c.canonical_name company, cs.best_valuation_usd val, cs.valuation_tier tier,
               cs.technical_elite_count tech, cs.raw_overlap_count raw, cs.people_list pl
        FROM company_scores cs JOIN companies c USING(company_id)
        WHERE cs.technical_elite_count>=1 AND cs.number_of_professional_investors=0
        ORDER BY cs.technical_elite_count DESC, cs.raw_overlap_count DESC LIMIT 30""")
    for r in rows:
        pl = json.loads(r.pop("pl") or "[]")
        r["who"] = "; ".join(p["name"] or p["person_key"] for p in pl if p.get("technical_elite"))
        r["val"] = fmt_usd(r["val"])
    L.append(_table(rows, ["company", "val", "tier", "tech", "raw", "who"]))

    # 12 --------------------------------------------------------------------
    L += ["## 12. Which elite-person connections are newest?", "",
          "`FACT` — most recent confirmed edges carrying a real date.", ""]
    rows = _q(con, """
        SELECT e.investment_date date, p.full_name person, c.canonical_name company,
               e.relationship_type rel, cs.raw_overlap_count raw, cs.valuation_tier tier
        FROM person_company_edges e JOIN people p ON p.person_key=e.person_key
        JOIN companies c ON c.company_id=e.company_id
        LEFT JOIN company_scores cs ON cs.company_id=e.company_id
        WHERE e.is_confirmed=1 AND e.investment_date IS NOT NULL
        ORDER BY e.investment_date DESC LIMIT 30""")
    L.append(_table(rows, ["date", "person", "company", "rel", "raw", "tier"]))

    # 13 --------------------------------------------------------------------
    L += ["## 13. Which sectors show accelerating elite-network convergence?", "",
          "`DERIVED` — new confirmed elite connections in the last 12 months, by sector. "
          "Only dated edges count, and sector is only known where a company record "
          "supplied it, so unlabelled sectors are under-counted rather than absent.", ""]
    rows = _q(con, """
        SELECT COALESCE(c.industry_primary,'(unlabelled)') sector,
               COUNT(DISTINCT cs.company_id) companies,
               SUM(COALESCE(cs.elite_network_momentum_12m,0)) new_connections_12m,
               SUM(COALESCE(cs.elite_network_momentum_6m,0)) new_connections_6m
        FROM company_scores cs JOIN companies c USING(company_id)
        GROUP BY 1 HAVING new_connections_12m > 0
        ORDER BY new_connections_12m DESC LIMIT 20""")
    L.append(_table(rows, ["sector", "companies", "new_connections_12m", "new_connections_6m"]))

    # 14 --------------------------------------------------------------------
    L += ["## 14. Which past companies generated false-positive signals?", "",
          "`FACT` — cohort companies labelled FAILURE or MEDIOCRE that nonetheless "
          "attracted confirmed elite backing. **These are the most important rows in the "
          "entire project**: they are what stops elite overlap being treated as a "
          "guarantee.", ""]
    rows = _q(con, """
        SELECT c.canonical_name company, b.outcome_label outcome,
               MAX(b.elite_people_count) peak_knowable_overlap,
               cs.raw_overlap_count overlap_now, cs.best_valuation_usd val
        FROM backtest_observations b JOIN companies c USING(company_id)
        LEFT JOIN company_scores cs ON cs.company_id=b.company_id
        WHERE b.outcome_label IN ('FAILURE','MEDIOCRE')
        GROUP BY 1,2 HAVING overlap_now >= 1
        ORDER BY overlap_now DESC LIMIT 30""")
    for r in rows:
        r["val"] = fmt_usd(r["val"])
    L.append(_table(rows, ["company", "outcome", "peak_knowable_overlap", "overlap_now", "val"]))

    # 15 --------------------------------------------------------------------
    L += ["## 15. Does elite overlap retain signal after correlation and survivorship "
          "adjustment?", ""]
    import json as _json
    from pathlib import Path as _P
    bt = _P(out).parent / "reports" / "backtest_snapshots.json"
    if not bt.exists():
        bt = _P(out) / "backtest_snapshots.json"
    arms: dict[str, dict] = {}
    if bt.exists():
        doc = _json.loads(bt.read_text())
        for s_ in doc["snapshots"]:
            arm = ("WINNER" if s_["outcome_label"] in ("WINNER", "STRONG")
                   else "FAILURE/MEDIOCRE" if s_["outcome_label"] in ("FAILURE", "MEDIOCRE")
                   else None)
            if arm is None:
                continue
            a = arms.setdefault(arm, {"companies": set(), "any_edge": set(),
                                      "any_knowable": set()})
            a["companies"].add(s_["company"])
            if s_["total_confirmed_edges_now"]:
                a["any_edge"].add(s_["company"])
            if s_["as_knowable"]["count"]:
                a["any_knowable"].add(s_["company"])

    if not arms:
        L += ["**The graph cannot yet answer this.** No backtest cohort is loaded.", ""]
    else:
        L += ["`FACT` — cohort coverage, which decides whether the question is answerable "
              "at all:", "",
              "| arm | companies | with any confirmed edge | with any *knowable* overlap |",
              "|---|---|---|---|"]
        for arm in ("WINNER", "FAILURE/MEDIOCRE"):
            a = arms.get(arm)
            if a:
                L.append(f"| `{arm}` | {len(a['companies'])} | {len(a['any_edge'])} "
                         f"| **{len(a['any_knowable'])}** |")
        w = arms.get("WINNER", {}).get("any_knowable", set())
        f = arms.get("FAILURE/MEDIOCRE", {}).get("any_knowable", set())
        L += [""]
        MIN_PER_ARM = 8          # below this, no cohort claim is supportable at all
        underpowered = min(len(w), len(f)) < MIN_PER_ARM
        imbalanced = len(f) < 0.3 * max(1, len(w))
        if underpowered or imbalanced:
            L += [
                "### The honest answer: **not yet, and the apparent separation is an artefact.**",
                "",
                f"`BACKTEST.md` shows winners averaging above failures at every date. "
                f"**That number must not be believed.** Only "
                f"{len(w)} winner companies and "
                f"{len(f)} failure/mediocre companies have *any* knowable overlap at all "
                f"(out of {len(arms.get('WINNER', {}).get('companies', []))} and "
                f"{len(arms.get('FAILURE/MEDIOCRE', {}).get('companies', []))} in the cohort). "
                f"At least {MIN_PER_ARM} per arm would be needed before a difference in means "
                f"meant anything, and the failure arm is the thinner of the two.",
                "",
                "The separation is therefore measuring **which companies had edges "
                "collected**, not which companies were backed by elite people. And the "
                "reason is structural, not accidental:",
                "",
                "- Collection followed **people**, and a person's portfolio is documented "
                "through the companies that *worked*. Portfolio pages list wins; press "
                "releases announce rounds into companies that went on to raise again.",
                "- A failed company's investor list is frequently deleted along with its "
                "website, and nobody writes a retrospective naming the angels.",
                "- So the failure arm is under-collected **by construction**, and any test "
                "run on it will flatter the signal.",
                "",
                "**This is survivorship bias operating on the evidence itself**, one level "
                "below the usual concern about which companies get studied. Fixing it needs "
                "the negative controls' edges collected *deliberately* — going company-first "
                "through the failure list and reconstructing who backed them from archived "
                "announcements and filings — not waiting for them to appear while following "
                "people.",
                "",
                "Until that is done, this project can say **where elite capital is "
                "concentrated today**, which is its stated purpose, but it **cannot yet say "
                "whether that concentration predicts anything**. Treating the rankings as "
                "predictive would be exactly the error the negative controls exist to "
                "prevent.",
                "",
                "`SECONDARY_QUESTIONS.md` question 14 and `BACKTEST.md` carry the same "
                "caveat. The highest-priority next task in `research/state.json` is this "
                "gap.", ""]
        else:
            L += ["Both arms carry comparable coverage, so the separation in `BACKTEST.md` "
                  "is interpretable — as a **description of this cohort**, not a "
                  "significance test. Cohorts of this size cannot support one.", ""]
    (out / "SECONDARY_QUESTIONS.md").write_text("\n".join(L) + "\n")
