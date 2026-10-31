"""Markdown report generation.

Every table shows RAW FACTUAL COUNTS beside any derived score. Sections that
have no data say so explicitly rather than being omitted, because a missing
section reads as an oversight while an empty one reads as a finding.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from ..core.enums import TIER_UNKNOWN

TIER_LABEL = {
    "TIER_A_UNDER_500M": "Below $500M",
    "TIER_B_500M_TO_1B": "$500M – $1B",
    "TIER_C_1B_TO_5B": "$1B – $5B",
    "TIER_D_5B_PLUS": "$5B and above (calibration)",
    TIER_UNKNOWN: "Valuation unknown",
}
RANKINGS = [
    ("raw_people_count", "RAW verified overlap"),
    ("strict_people_count", "STRICT economic-exposure overlap"),
    ("weighted_score", "WEIGHTED overlap"),
    ("independence_adjusted_score", "INDEPENDENCE-ADJUSTED overlap"),
]


def fmt_usd(v) -> str:
    if v is None:
        return "—"
    v = float(v)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(v) >= div:
            return f"${v / div:,.2f}{suf}"
    return f"${v:,.0f}"


def fmt(v, nd=2) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def _q(con, sql, params=()) -> list[dict]:
    return [dict(r) for r in con.execute(sql, params)]


def _companies(con, tier=None, limit=None):
    from .exports import company_rows
    rows = company_rows(con, tier)
    return rows[:limit] if limit else rows


def _rank_table(rows: list[dict], key: str, n: int = 10) -> str:
    ranked = sorted(rows, key=lambda r: (-(r.get(key) or 0), -(r.get("raw_people_count") or 0),
                                         r["company"]))[:n]
    if not ranked:
        return "_No companies in this tier._\n"
    out = ["| # | company | valuation | raw | strict | weighted | indep-adj | clusters | tech | people |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(ranked, 1):
        out.append(
            f"| {i} | **{r['company']}** | {fmt_usd(r['valuation_usd'])} "
            f"| {r['raw_people_count']} | {r['strict_people_count']} "
            f"| {fmt(r['weighted_score'])} | {fmt(r['independence_adjusted_score'])} "
            f"| {r['distinct_information_clusters']} | {r['technical_elite_count']} "
            f"| {r['names_of_people'][:120]} |")
    return "\n".join(out) + "\n"


def _company_dossier(con, r: dict) -> str:
    """Full evidence-exposed profile. Never '7 elite investors' without the edges."""
    pl = json.loads(con.execute("SELECT people_list FROM company_scores WHERE company_id=?",
                                (r["company_id"],)).fetchone()["people_list"] or "[]")
    src = _q(con,
        "SELECT DISTINCT s.url, s.source_type, s.tier, s.publisher, s.published_date"
        " FROM sources s JOIN person_company_edges e ON e.edge_id = s.parent_id"
        " WHERE s.parent_kind='edge' AND e.company_id=? AND e.is_confirmed=1"
        " ORDER BY s.tier, s.published_date DESC", (r["company_id"],))
    vsrc = _q(con,
        "SELECT s.url, s.publisher, s.evidence_summary FROM sources s"
        " JOIN valuations v ON v.valuation_id=s.parent_id"
        " WHERE s.parent_kind='valuation' AND v.company_id=? AND v.is_current_best=1",
        (r["company_id"],))

    L = [f"### {r['company']}", "",
         "**FACT — identity and valuation**", "",
         f"- company_id: `{r['company_id']}`",
         f"- current valuation: **{fmt_usd(r['valuation_usd'])}** "
         f"({r['valuation_type'] or '—'}, dated {r['valuation_date'] or '—'}, "
         f"confidence {r['valuation_confidence'] or '—'}, staleness {r['staleness_band'] or '—'})",
         f"- valuation source: " + (", ".join(f"[{v['publisher'] or 'source'}]({v['url']})"
                                              for v in vsrc) or "**none — TIER_U_UNKNOWN**"),
         f"- tier: `{r['valuation_tier']}` · {r['public_or_private'] or 'UNKNOWN'}"
         f"{' · ' + r['ticker'] if r.get('ticker') else ''}"
         f" · sector {r['sector'] or '—'} · {r['country'] or '—'}",
         "",
         "**FACT — verified elite connections**", "",
         f"- raw people count: **{r['raw_people_count']}**"
         f" · strict (direct personal economic exposure): **{r['strict_people_count']}**"
         f" · broad (incl. controlled vehicles): **{r['broad_people_count']}**",
         f"- best source tier: `{r['source_quality'] or '—'}`",
         "",
         "| person | relationship | overlap class | date | verification | technical elite | domains |",
         "|---|---|---|---|---|---|---|"]
    for p in pl:
        L.append(f"| **{p['name'] or p['person_key']}** ({p['signal_class']}) "
                 f"| {', '.join(p['relationship_types'])} | {p['strongest_overlap_class']} "
                 f"| {p.get('earliest_investment_date') or '—'} "
                 f"| {', '.join(p['verification_statuses'])} "
                 f"| {'yes' if p.get('technical_elite') else 'no'} "
                 f"| {', '.join(p['domain_clusters'])} |")
    L += ["",
          "**DERIVED**", "",
          f"- weighted overlap: `{fmt(r['weighted_score'])}`",
          f"- independence-adjusted: `{fmt(r['independence_adjusted_score'])}` "
          f"(δ=0.35) · `{fmt(r['independence_adjusted_delta0'])}` (δ=0, one voice per network) "
          f"· `{fmt(r['independence_adjusted_delta1'])}` (δ=1, = raw weighted)",
          f"- distinct information clusters (network): **{r['distinct_information_clusters']}** "
          f"· distinct domains: **{r['distinct_domains_represented']}** "
          f"· cross-domain score: `{fmt(r['cross_domain_score'])}`",
          f"- technical-elite count: **{r['technical_elite_count']}** "
          f"({r['technical_elite_names'] or '—'})",
          f"- earliest elite entry: {r['earliest_elite_entry_date'] or '—'}"
          f" · entry valuation {fmt_usd(r['valuation_at_earliest_elite_entry'])}"
          f" · current/entry multiple {fmt(r['current_to_entry_multiple'])}",
          f"- elite-network momentum: +{r['elite_network_momentum_12m'] or 0} in 12m, "
          f"+{r['elite_network_momentum_6m'] or 0} in 6m "
          f"(from {r['dated_edge_person_count']} of {r['raw_people_count']} dated edges)",
          "", f"**PROVENANCE** — {len(src)} distinct sources behind these edges:", ""]
    for s in src[:25]:
        L.append(f"- `{s['tier']}` [{s['publisher'] or s['source_type']}]({s['url']})"
                 f"{' · ' + s['published_date'] if s['published_date'] else ''}")
    if len(src) > 25:
        L.append(f"- _…and {len(src) - 25} more; full list in `data/exports/sources.csv`_")
    L += ["", f"_Walk back any figure above: `edge_ids` = `{r['edge_ids'][:200]}`_", ""]
    return "\n".join(L)


def executive_report(con, q: dict, validation: list[dict], out: Path) -> None:
    built = date.today().isoformat()
    all_rows = _companies(con)
    L = [
        "# GREENSNAKE — EXECUTIVE RESULTS", "",
        f"_Built {built} · {q['edges_confirmed']} confirmed edges · "
        f"{q['companies_canonical_total']} canonical companies · "
        f"{q['people_total_in_universe']} people tracked_", "",
        f"**DATA COMPLETENESS: `{q['data_completeness_assessment']}`** — "
        "this is a partial reconstruction, not a census. See "
        "[Data quality](DATA_QUALITY.md) before acting on anything here.", "",
        "> **This is a discovery instrument, not a recommendation engine.** Elite overlap "
        "is an information signal about where unusually well-informed people are looking. "
        "It says nothing on its own about valuation, dilution, access, liquidity, unit "
        "economics, burn, competition, technical feasibility, regulation or downside. "
        "Anything surfaced here still requires independent diligence.", "",
        "> **The backtest does NOT yet show that elite overlap predicts outcomes, and the "
        "separation it reports must not be believed.** Only a handful of cohort companies "
        "on either arm have overlap that was *knowable* at the historical date, and the "
        "failure arm is the thinner of the two — because collection followed people, and "
        "people's portfolios are documented through the companies that worked. That is "
        "survivorship bias operating on the evidence itself. This graph can say where "
        "elite capital is concentrated today; it cannot yet say whether that concentration "
        "predicts anything. See [question 15](SECONDARY_QUESTIONS.md).", "",
        "---", "",
    ]

    # ---- THE CENTRAL QUESTION -------------------------------------------
    DEAD = {"ACQUIRED", "MERGED", "SHUT_DOWN", "BANKRUPT"}
    status = {r["company_id"]: (r["current_status"] or "UNKNOWN") for r in
              con.execute("SELECT company_id, current_status FROM companies")}

    def _row(r, n):
        stale = " ⚠stale" if r["staleness_band"] == "GT_36M" else ""
        return (f"| {n} | **{r['company']}** | {fmt_usd(r['valuation_usd'])}{stale} "
                f"| {r['valuation_tier'][5:6]} | {r['raw_people_count']} "
                f"| {r['strict_people_count']} | {r['technical_elite_count']} "
                f"| {r['distinct_information_clusters']} "
                f"| {fmt(r['independence_adjusted_score'])} | {r['names_of_people'][:110]} |")

    HDR = ["| # | company | valuation | tier | raw | strict | tech-elite | networks "
           "| indep-adj | who |", "|---|---|---|---|---|---|---|---|---|---|"]
    live = [r for r in all_rows if r["raw_people_count"] >= 2
            and status.get(r["company_id"]) not in DEAD]
    valued = sorted([r for r in live if r["valuation_tier"] in
                     ("TIER_A_UNDER_500M", "TIER_B_500M_TO_1B", "TIER_C_1B_TO_5B")],
                    key=lambda r: (-(r["independence_adjusted_score"] or 0),
                                   -r["technical_elite_count"], -r["raw_people_count"]))
    unvalued = sorted([r for r in live if r["valuation_tier"] == TIER_UNKNOWN],
                      key=lambda r: (-(r["independence_adjusted_score"] or 0),
                                     -r["technical_elite_count"], -r["raw_people_count"]))
    L += [
        "## THE CENTRAL QUESTION",
        "",
        "> *Which still-small companies are already quietly attracting capital or direct "
        "involvement from multiple exceptionally high-access, high-intelligence people who "
        "historically encounter technological outliers before the general market?*",
        "",
        "Answered in two parts, because **an unvalued company is not a small one** — it is a "
        "company whose valuation this project could not source. Merging the two would let "
        "large, well-known names masquerade as quiet discoveries, which is the opposite of "
        "what is being asked. Acquired, merged and shut-down companies are excluded here "
        "(they remain in the tier tables for calibration).",
        "",
        "Both lists are ranked by **independence-adjusted overlap**, so three backers from "
        "three different information networks outrank four from one firm.",
        "",
        f"### Part 1 — confirmed under $5B ({len(valued)} companies with ≥2 elite connections)",
        "",
        "These have a **sourced, dated valuation** placing them below $5B. This is the "
        "direct answer to the question.",
        "",
    ] + HDR + [_row(r, i) for i, r in enumerate(valued[:25], 1)] + [
        "",
        f"### Part 2 — valuation unknown ({len(unvalued)} companies with ≥2 elite connections)",
        "",
        "**No sourced current valuation, so size is genuinely unknown** — some of these are "
        "early and obscure, others are large companies whose valuation simply was not "
        "reached. They are shown because several of the most interesting names in the graph "
        "are here, and they are the priority targets for valuation work. Do not read this "
        "list as small companies.",
        "",
    ] + HDR + [_row(r, i) for i, r in enumerate(unvalued[:25], 1)] + [
        "",
        "`ANALYSIS` — read both as a **prioritised research list, not a ranking of "
        "quality**. Three cautions apply to every row:",
        "",
        "1. **A company is here because it was found, and it was found because someone "
        "published something.** A company with equally strong backing whose investors "
        "publish nothing does not appear at all.",
        "2. **Elite overlap has preceded expensive failures.** `SECONDARY_QUESTIONS.md` "
        "question 14 lists the ones in this very cohort.",
        "3. **⚠stale marks a valuation over three years old.** It is the best sourced figure "
        "available, not a current one.",
        "", "---", ""]

    for tier in ("TIER_A_UNDER_500M", "TIER_B_500M_TO_1B", "TIER_C_1B_TO_5B"):
        letter = {"TIER_A_UNDER_500M": "A", "TIER_B_500M_TO_1B": "B", "TIER_C_1B_TO_5B": "C"}[tier]
        all_tier = _companies(con, tier)
        # An acquired, merged or dead company has no CURRENT valuation -- what it
        # carries is a terminal one. Google DeepMind's 2014 acquisition price
        # would otherwise win the $500M-$1B tier twelve years after the fact.
        rows = [r for r in all_tier
                if (r.get("current_status") or "UNKNOWN")
                not in ("ACQUIRED", "MERGED", "SHUT_DOWN", "BANKRUPT")]
        excluded = [r for r in all_tier if r not in rows]
        L.append(f"## {letter}. HIGHEST-OVERLAP COMPANY — {TIER_LABEL[tier]}\n")
        if excluded:
            L.append(f"_{len(excluded)} company/companies in this tier are acquired, merged or "
                     f"shut down and are excluded from the headline — an acquisition price or a "
                     f"shut-down zero is a **terminal** valuation, not a current one. They remain "
                     f"in the tier table below: "
                     f"{', '.join(r['company'] + ' (' + (r.get('current_status') or '?') + ')' for r in excluded[:6])}._\n")
        if not rows:
            L.append(f"**No company currently qualifies for this tier.** "
                     f"{q['companies_by_tier'].get(tier, 0)} companies are bucketed here. "
                     f"This is a valuation-coverage gap, not an absence of candidates: "
                     f"{q['companies_valuation_unknown']} companies in the graph have no "
                     f"sourced current valuation and sit in `TIER_U_UNKNOWN`. "
                     f"See the unknown-valuation table — the highest-overlap companies there "
                     f"are the priority valuation targets.\n")
        else:
            top = max(rows, key=lambda r: (r["raw_people_count"], r["weighted_score"]))
            alts = {
                "STRICT economic exposure": max(
                    rows, key=lambda r: (r["strict_people_count"], r["weighted_score"])),
                "INDEPENDENCE-ADJUSTED overlap": max(
                    rows, key=lambda r: (r["independence_adjusted_score"] or 0,
                                         r["raw_people_count"])),
                "TECHNICAL-ELITE density": max(
                    rows, key=lambda r: (r["technical_elite_count"],
                                         r["technical_elite_score"] or 0)),
            }
            disagree = {k: v for k, v in alts.items()
                        if v["company_id"] != top["company_id"]}
            L.append(f"**By RAW verified overlap the answer is {top['company']}** "
                     f"({top['raw_people_count']} confirmed elite people).\n")
            if disagree:
                L.append("The ranking methods **disagree**, and that disagreement is "
                         "information rather than noise:\n")
                L.append("| ranked by | winner | why it differs |")
                L.append("|---|---|---|")
                for label, r in disagree.items():
                    L.append(f"| {label} | **{r['company']}** | raw {r['raw_people_count']}, "
                             f"strict {r['strict_people_count']}, "
                             f"indep-adj {fmt(r['independence_adjusted_score'])}, "
                             f"tech-elite {r['technical_elite_count']}, "
                             f"{r['distinct_information_clusters']} network cluster(s) |")
                L.append("")
                L.append("_Raw overlap rewards breadth; independence adjustment rewards "
                         "backers who are not reading the same sources; technical density "
                         "rewards people who can evaluate the science. A company that wins "
                         "on all of them is a stronger signal than one that wins on any._\n")
            else:
                L.append("_Raw, strict, independence-adjusted and technical-elite rankings "
                         "all pick the same company here._\n")
            L.append(_company_dossier(con, top))
            for label, r in disagree.items():
                L.append(f"#### Also shown: leader by {label}\n")
                L.append(_company_dossier(con, r))
        L.append("---\n")

    L.append("## TIER RANKINGS\n")
    L.append("Ranking methods disagree by design — raw counts favour breadth, "
             "independence-adjusted favours genuinely distinct sources. "
             "**Disagreements are shown, not resolved.**\n")
    for tier in ("TIER_A_UNDER_500M", "TIER_B_500M_TO_1B", "TIER_C_1B_TO_5B",
                 "TIER_D_5B_PLUS", TIER_UNKNOWN):
        rows = _companies(con, tier)
        L.append(f"### {TIER_LABEL[tier]} — {len(rows)} companies\n")
        if not rows:
            L.append("_No companies in this tier._\n")
            continue
        for key, label in RANKINGS:
            L.append(f"**Top 10 by {label}**\n")
            L.append(_rank_table(rows, key))
            L.append("")
    L.append("---\n")

    L.append("## INTEGRITY\n")
    L.append("| test | status | detail |\n|---|---|---|")
    for v in validation:
        L.append(f"| {v['test_id']} {v['name']} | `{v['status']}` | {v['detail']} |")
    L.append("")
    (out / "EXECUTIVE_REPORT.md").write_text("\n".join(L) + "\n")


def technical_and_crossdomain(con, out: Path) -> None:
    rows = _companies(con)
    tech = sorted([r for r in rows if r["technical_elite_count"] >= 2],
                  key=lambda r: (-r["technical_elite_count"], -(r["technical_elite_score"] or 0)))
    cross = sorted([r for r in rows if r["distinct_domains_represented"] >= 3],
                   key=lambda r: (-r["distinct_domains_represented"], -(r["cross_domain_score"] or 0)))
    L = ["# TECHNICAL-ELITE AND CROSS-DOMAIN OVERLAP", "",
         "## Technical-elite overlap", "",
         "**Qualification is documented capability, never celebrity.** A person counts as "
         "technical elite at technical band ≥4 *and* a research/academic archetype, or band 5 "
         "with a founder-operator archetype — an engineer who built the thing.", "",
         f"{len(tech)} companies have **2 or more** technically elite backers.", ""]
    if tech:
        L += ["| company | valuation | tier | tech-elite | tech score | who | why they qualify |",
              "|---|---|---|---|---|---|---|"]
        for r in tech[:40]:
            pl = json.loads(con.execute(
                "SELECT people_list FROM company_scores WHERE company_id=?",
                (r["company_id"],)).fetchone()["people_list"] or "[]")
            tp = [p for p in pl if p.get("technical_elite")]
            why = "; ".join(
                (con.execute("SELECT primary_affiliation FROM people WHERE person_key=?",
                             (p["person_key"],)).fetchone() or [""])[0] or "" for p in tp[:3])
            L.append(f"| **{r['company']}** | {fmt_usd(r['valuation_usd'])} | {r['valuation_tier']} "
                     f"| {r['technical_elite_count']} | {fmt(r['technical_elite_score'])} "
                     f"| {r['technical_elite_names']} | {why[:180]} |")
    else:
        L.append("_No company yet has two or more technically elite backers in the confirmed set._")
    L += ["", "---", "", "## Cross-domain overlap", "",
          "Backers who read the world from **genuinely different domains** carry more "
          "independent information than several adjacent venture partners. "
          "`distinct_domains_represented` counts domain clusters among a company's backers; "
          "`cross_domain_score` sums the strongest contribution within each domain.", "",
          f"{len(cross)} companies draw backers from **3 or more** distinct domains.", ""]
    if cross:
        L += ["| company | valuation | tier | domains | raw | indep-adj | cross-domain | who |",
              "|---|---|---|---|---|---|---|---|"]
        for r in cross[:40]:
            pl = json.loads(con.execute(
                "SELECT people_list FROM company_scores WHERE company_id=?",
                (r["company_id"],)).fetchone()["people_list"] or "[]")
            doms = sorted({d for p in pl for d in p["domain_clusters"]})
            L.append(f"| **{r['company']}** | {fmt_usd(r['valuation_usd'])} | {r['valuation_tier']} "
                     f"| {', '.join(doms)} | {r['raw_people_count']} "
                     f"| {fmt(r['independence_adjusted_score'])} | {fmt(r['cross_domain_score'])} "
                     f"| {r['names_of_people'][:110]} |")
    else:
        L.append("_No company yet draws confirmed backers from three or more distinct domains._")
    (out / "TECHNICAL_AND_CROSSDOMAIN.md").write_text("\n".join(L) + "\n")


def network_report(con, out: Path) -> None:
    asserted = _q(con, "SELECT r.correlation_type, COUNT(*) n FROM investor_relationships r"
                       " WHERE derived=0 GROUP BY 1 ORDER BY n DESC")
    derived = _q(con, "SELECT a.full_name na, b.full_name nb, r.strength, r.evidence"
                      " FROM investor_relationships r JOIN people a ON a.person_key=r.person_key_a"
                      " JOIN people b ON b.person_key=r.person_key_b WHERE r.derived=1"
                      " ORDER BY r.strength DESC LIMIT 40")
    pairs = _q(con, "SELECT a.person_key ka, b.person_key kb, pa.full_name na, pb.full_name nb,"
                    " COUNT(DISTINCT a.company_id) shared FROM person_company_edges a"
                    " JOIN person_company_edges b ON b.company_id=a.company_id"
                    " AND b.person_key > a.person_key AND b.is_confirmed=1"
                    " JOIN people pa ON pa.person_key=a.person_key"
                    " JOIN people pb ON pb.person_key=b.person_key"
                    " WHERE a.is_confirmed=1 GROUP BY 1,2 HAVING shared >= 2"
                    " ORDER BY shared DESC LIMIT 40")
    L = ["# PERSON ↔ PERSON NETWORK", "",
         "The purpose is **not** social mapping. It is to test whether apparently "
         "independent investment signals actually come from one information network. "
         "Personal friendship is never inferred without evidence.", "",
         "## Asserted correlation links (evidence-backed)", ""]
    if asserted:
        L += ["| type | count |", "|---|---|"] + [
            f"| `{a['correlation_type']}` | {a['n']} |" for a in asserted]
    else:
        L.append("_None recorded yet._")
    L += ["", "## Derived co-investment links",
          "",
          "Two people are linked when they share **≥3** companies with confirmed edges. "
          "Derived links are stored separately (`derived=1`) and are recomputed with the "
          "scored company removed, so a company can never inflate its own backers' "
          "apparent correlation.", ""]
    if derived:
        L += ["| A | B | strength | evidence |", "|---|---|---|---|"] + [
            f"| {d['na']} | {d['nb']} | {fmt(d['strength'])} | {d['evidence']} |" for d in derived]
    else:
        L.append("_No pair yet shares three or more confirmed companies._")
    L += ["", "## Which combinations appear together most often", ""]
    if pairs:
        L += ["| A | B | shared companies |", "|---|---|---|"] + [
            f"| {p['na']} | {p['nb']} | {p['shared']} |" for p in pairs]
    else:
        L.append("_No pair yet shares two or more confirmed companies._")
    (out / "NETWORK_ANALYSIS.md").write_text("\n".join(L) + "\n")


def data_quality_report(con, q: dict, out: Path) -> None:
    L = ["# DATA QUALITY AND COVERAGE", "",
         f"**DATA COMPLETENESS ASSESSMENT: `{q['data_completeness_assessment']}`**", ""]
    for r in q["data_completeness_reasons"]:
        L.append(f"- {r}")
    L += ["", "## People", "", "| metric | value |", "|---|---|",
          f"| total candidates researched | {q['people_total_in_universe']} |",
          f"| CORE_HIGH_SIGNAL | {q['people_core_high_signal']} |",
          f"| EXTENDED_SIGNAL | {q['people_extended_signal']} |",
          f"| DOMAIN_SPECIALIST | {q['people_domain_specialist']} |",
          f"| WATCHLIST | {q['people_watchlist']} |",
          f"| LOW_SIGNAL_OR_POOR_VISIBILITY | {q['people_low_signal']} |",
          f"| with ≥1 confirmed edge | {q['people_with_at_least_one_confirmed_edge']} |",
          f"| with no edge at all | {q['people_with_zero_edges']} |",
          "", "## Companies and relationships", "", "| metric | value |", "|---|---|",
          f"| raw company name strings seen | {q['company_raw_name_strings_seen']} |",
          f"| canonical companies after dedup | {q['companies_canonical_total']} |",
          f"| name strings merged by dedup | {q['companies_merged_by_dedup']} |",
          f"| relationships investigated (edges + rejected + queued) | {q['edges_total_investigated']} |",
          f"| CONFIRMED_PRIMARY | {q['edges_CONFIRMED_PRIMARY']} |",
          f"| CONFIRMED_MULTI_SOURCE | {q['edges_CONFIRMED_MULTI_SOURCE']} |",
          f"| CONFIRMED_REPUTABLE_SECONDARY | {q['edges_CONFIRMED_REPUTABLE_SECONDARY']} |",
          f"| PROBABLE_BUT_NOT_CONFIRMED | {q['edges_PROBABLE_BUT_NOT_CONFIRMED']} |",
          f"| CONFLICTING_EVIDENCE | {q['edges_CONFLICTING_EVIDENCE']} |",
          f"| UNVERIFIED | {q['edges_UNVERIFIED']} |",
          f"| REJECTED (investigated and not supported) | {q['edges_rejected_table']} |",
          f"| unresolved claims in research queue | {q['edges_in_research_queue']} |",
          f"| **% of confirmed edges with Tier-1 primary evidence** | **{q['pct_confirmed_with_primary_evidence']}%** |",
          f"| % of confirmed edges resting only on reputable secondary | {q['pct_confirmed_secondary_only']}% |",
          f"| distinct source domains cited | {q['distinct_source_domains']} |",
          f"| % of edges carrying an investment date | {q['pct_edges_dated']}% |",
          "", "### Confirmed edges by relationship type", "",
          "| relationship | n |", "|---|---|"]
    for k, v in q["confirmed_edges_by_relationship_type"].items():
        L.append(f"| `{k}` | {v} |")
    L += ["", "## Valuation coverage", "", "| metric | value |", "|---|---|",
          f"| companies with a sourced current valuation | {q['companies_with_current_valuation']} ({q['pct_companies_with_valuation']}%) |",
          f"| **companies with UNKNOWN valuation** | **{q['companies_valuation_unknown']}** |",
          f"| companies with entry-valuation information | {q['companies_with_entry_valuation']} |",
          f"| public companies | {q['companies_public']} |",
          f"| private companies | {q['companies_private']} |",
          f"| public/private unknown | {q['companies_public_private_unknown']} |", ""]
    L += ["### Valuation age (share of valued companies)", "", "| band | n | % |", "|---|---|---|"]
    for b, n in q["valuation_staleness_counts"].items():
        L.append(f"| {b} | {n} | {q['valuation_staleness_pct_of_valued'][b]}% |")
    L += ["", "### Companies per tier", "", "| tier | n |", "|---|---|"]
    for t, n in q["companies_by_tier"].items():
        L.append(f"| `{t}` | {n} |")
    L += ["", "## Sector and geography coverage", "",
          f"`{q['companies_sector_unlabelled']}` of {q['companies_canonical_total']} companies "
          f"carry no sector label and `{q['companies_country_unstated']}` no country. Both are "
          f"collection gaps: most edges came from portfolio pages and filings that name a "
          f"company without describing it. **An unlabelled company is invisible to any "
          f"sector-level analysis**, so the sector table below understates every category.", "",
          "| sector | companies |", "|---|---|"]
    for k, v in list(q["companies_by_sector"].items())[:22]:
        L.append(f"| {k} | {v} |")
    L += ["", "| country | companies |", "|---|---|"]
    for k, v in list(q["companies_by_country"].items())[:22]:
        L.append(f"| {k} | {v} |")
    L += ["", "### Confirmed edges by workstream", "", "| workstream | confirmed edges |", "|---|---|"]
    for k, v in q["edges_by_workstream"].items():
        L.append(f"| `{k}` | {v} |")
    L += ["", "See `docs/COVERAGE_GAPS.md` for the named, specific gaps each workstream "
          "reported — paywalled sources, image-only portfolio pages and people whose "
          "vehicles publish nothing.", ""]

    if q.get("source_urls_checked"):
        L += ["", "## Source liveness", "",
              f"- URLs checked: {q['source_urls_checked']}",
              f"- resolving: {q['pct_source_urls_resolving']}%",
              f"- failing: {q['source_urls_failing']} "
              f"(401/403/405/429 count as resolving — a paywalled page is a real page)"]
    L += ["", "## People whose portfolios could not be reconstructed", "",
          f"{q['n_people_without_reconstructable_portfolio']} of "
          f"{q['people_total_in_universe']} tracked people have **no confirmed edge**. ",
          "",
          "This is a coverage statement, not a statement about those people. Several were "
          "included precisely to measure the visibility floor. **Absence of an edge is never "
          "evidence of absence of an investment.**", "",
          "| person | class |", "|---|---|"]
    for p in q["people_without_reconstructable_portfolio"][:200]:
        L.append(f"| {p['full_name']} | {p['signal_class']} |")
    (out / "DATA_QUALITY.md").write_text("\n".join(L) + "\n")


def discovery_report(con, out: Path) -> None:
    rows = [r for r in _companies(con)
            if r["valuation_tier"] != "TIER_D_5B_PLUS"]
    def sel(pred, key, n=20):
        return sorted([r for r in rows if pred(r)], key=key)[:n]
    qs = [
        ("Sub-$500M companies with ≥3 elite backers",
         lambda r: r["valuation_tier"] == "TIER_A_UNDER_500M" and r["raw_people_count"] >= 3,
         lambda r: -r["raw_people_count"]),
        ("Sub-$1B companies with ≥2 technically elite backers",
         lambda r: r["valuation_tier"] in ("TIER_A_UNDER_500M", "TIER_B_500M_TO_1B")
                   and r["technical_elite_count"] >= 2,
         lambda r: -r["technical_elite_count"]),
        ("Companies with backers from ≥3 independent information clusters",
         lambda r: r["distinct_information_clusters"] >= 3,
         lambda r: -r["distinct_information_clusters"]),
        ("Companies first backed when worth under $100M",
         lambda r: (r["valuation_at_earliest_elite_entry"] or 1e18) < 100_000_000,
         lambda r: r["valuation_at_earliest_elite_entry"] or 0),
        ("Highest overlap at the lowest valuation (elite density)",
         lambda r: r["elite_density"] is not None and r["raw_people_count"] >= 2,
         lambda r: -(r["elite_density"] or 0)),
        ("Highest technical-elite density",
         lambda r: r["technical_elite_density"] is not None and r["technical_elite_count"] >= 1,
         lambda r: -(r["technical_elite_density"] or 0)),
        ("Newest elite convergence (most new backers in last 12 months)",
         lambda r: (r["elite_network_momentum_12m"] or 0) >= 1,
         lambda r: -(r["elite_network_momentum_12m"] or 0)),
        ("UNKNOWN-valuation companies with the highest overlap — priority valuation targets",
         lambda r: r["valuation_tier"] == TIER_UNKNOWN and r["raw_people_count"] >= 2,
         lambda r: -r["raw_people_count"]),
        ("Public companies appearing unexpectedly in elite portfolios",
         lambda r: r["public_or_private"] == "PUBLIC",
         lambda r: -r["raw_people_count"]),
    ]
    L = ["# COMPANY DISCOVERY VIEW", "",
         "Answers to the standing screening questions, computed from the graph. "
         "Full filterable data: `data/exports/company_discovery.csv`.", "",
         "_Every row keeps the raw factual count next to the derived scores._", ""]
    for title, pred, key in qs:
        sub = sel(pred, key)
        L += [f"## {title}", ""]
        if not sub:
            L += ["_No company currently satisfies this filter._", ""]
            continue
        L += ["| company | valuation | tier | raw | strict | tech | clusters | indep-adj | people |",
              "|---|---|---|---|---|---|---|---|---|"]
        for r in sub:
            L.append(f"| **{r['company']}** | {fmt_usd(r['valuation_usd'])} | {r['valuation_tier']} "
                     f"| {r['raw_people_count']} | {r['strict_people_count']} "
                     f"| {r['technical_elite_count']} | {r['distinct_information_clusters']} "
                     f"| {fmt(r['independence_adjusted_score'])} | {r['names_of_people'][:100]} |")
        L.append("")
    (out / "COMPANY_DISCOVERY.md").write_text("\n".join(L) + "\n")


def generate_all(con, q: dict, validation: list[dict], out_dir: str | Path,
                 root: Path | None = None) -> list[str]:
    from . import backtest_report, openwork, questions
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    executive_report(con, q, validation, out)
    technical_and_crossdomain(con, out)
    network_report(con, out)
    data_quality_report(con, q, out)
    discovery_report(con, out)
    questions.build(con, out)
    openwork.build(con, out)
    backtest_report.build(con, root or out.parent, out)
    return sorted(p.name for p in out.glob("*.md"))
