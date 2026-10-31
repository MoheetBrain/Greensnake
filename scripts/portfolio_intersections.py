#!/usr/bin/env python3
"""PORTFOLIO INTERSECTION RANKING — which companies appear in the most elite portfolios?

    python3 scripts/portfolio_intersections.py

One metric, deliberately simple:

    PORTFOLIO_INTERSECTION_COUNT =
        distinct tracked people with a CONFIRMED relationship to the company
        that represents real economic ownership exposure

A person counts once per company no matter how many rounds or sources.
Weighted and network-adjusted scores are carried as secondary columns only;
they never affect the ordering.

Writes  data/exports/portfolio_intersections.csv   (every company, ranked)
        reports/PORTFOLIO_INTERSECTIONS.md         (the readable report)
"""
from __future__ import annotations

import csv
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from greensnake.graph.correlation import person_primary_cluster  # noqa: E402
from greensnake.scoring.people import is_technical_elite         # noqa: E402

# --- what counts as economic ownership exposure ---------------------------
DIRECT = {"PERSONAL_ANGEL_INVESTMENT", "PERSONAL_EQUITY_INVESTMENT",
          "SPV_INVESTMENT", "FOUNDER_EQUITY"}
CONTROLLED = {"FAMILY_OFFICE_INVESTMENT", "CONTROLLED_FUND_INVESTMENT"}
ECONOMIC = DIRECT | CONTROLLED
VC_PARTNER = {"VC_FUND_PARTNER_INVESTMENT"}
# Everything else — BOARD_ONLY, ADVISOR_ONLY, GRANT_FUNDING,
# PHILANTHROPIC_FUNDING, LP_INDIRECT, DEBT_FINANCING,
# CORPORATE_STRATEGIC_INVESTMENT, OTHER_VERIFIED — is excluded from the count.

TIER_LABEL = {
    "TIER_A_UNDER_500M": "Under $500M",
    "TIER_B_500M_TO_1B": "$500M – $1B",
    "TIER_C_1B_TO_5B": "$1B – $5B",
    "TIER_D_5B_PLUS": "$5B and above",
    "TIER_U_UNKNOWN": "Valuation unknown",
}
TIER_ORDER = ["TIER_A_UNDER_500M", "TIER_B_500M_TO_1B", "TIER_C_1B_TO_5B",
              "TIER_D_5B_PLUS", "TIER_U_UNKNOWN"]
TIER_RANK = {"TIER_1_PRIMARY": 3, "TIER_2_SECONDARY": 2, "TIER_3_DATABASE": 1}

# "Obscure" is a judgement, not a field in the data. A company can sit in
# TIER_U simply because nobody sourced a market cap for it -- Alphabet did.
# So household names are excluded by an explicit, auditable list rather than
# by a proxy that pretends to measure notability.
NOT_OBSCURE = {
    "alphabet", "meta platforms", "amazon", "x (formerly twitter)", "spacex", "stripe",
    "uber", "airbnb", "openai", "anthropic", "palantir technologies", "tesla", "coinbase",
    "reddit", "dropbox", "spotify", "zoom", "shopify", "figma", "databricks", "scale ai",
    "perplexity", "cognition", "anduril industries", "neuralink", "the boring company",
    "xai", "whatsapp", "instagram", "youtube", "waymo", "google deepmind", "grail, inc.",
    "nvidia", "microsoft", "apple", "netflix", "linkedin", "paypal", "square", "block",
    "twitter", "23andme", "moderna", "illumina", "rocket lab", "planet labs", "canva",
    "revolut", "nubank", "mercadolibre", "atlassian", "box", "asana", "vercel", "replit",
    "hugging face", "mistral ai", "cohere", "safe superintelligence", "thinking machines lab",
}

FRONTIER = {"AI_SOFTWARE", "SEMICONDUCTORS", "ROBOTICS", "BIOTECH_LIFESCIENCES",
            "MATERIALS", "ENERGY_CLIMATE", "SPACE", "DEFENCE", "QUANTUM",
            "INDUSTRIAL_DEEPTECH"}


def usd(v):
    if v is None:
        return ""
    v = float(v)
    for d, s in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(v) >= d:
            return f"${v/d:,.2f}{s}"
    return f"${v:,.0f}"


def build():
    con = sqlite3.connect(ROOT / "database" / "elite_graph.sqlite")
    con.row_factory = sqlite3.Row

    people = {r["person_key"]: dict(r) for r in con.execute(
        "SELECT p.person_key, p.full_name, p.signal_class, p.archetypes, p.domains,"
        " s.technical_intelligence_score tech, s.capital_flexibility cap,"
        " s.person_weight FROM people p LEFT JOIN people_scores s USING(person_key)")}
    primary = person_primary_cluster(con)
    for pk, p in people.items():
        arch = json.loads(p["archetypes"] or "[]")
        p["arch"] = arch
        p["is_tech_elite"] = is_technical_elite(p["tech"], arch)
        # PROXY for "billionaire founder": a founder-operator whose capital
        # flexibility band is 5 (effectively unconstrained personal capital).
        # Not a sourced net-worth claim.
        p["is_big_founder"] = "FOUNDER_OPERATOR" in arch and (p["cap"] or 0) >= 5
        p["cluster"] = primary.get(pk, "OTHER")
        p["is_frontier_ai"] = p["cluster"] == "AI"

    # --- collapse to one row per (company, person) -------------------------
    slots: dict[str, dict[str, dict]] = defaultdict(dict)
    for r in con.execute(
            "SELECT e.company_id, e.person_key, e.relationship_type, e.verification_status,"
            " e.edge_id, e.investment_date FROM person_company_edges e WHERE e.is_confirmed=1"):
        rt = r["relationship_type"]
        if rt not in ECONOMIC and rt not in VC_PARTNER:
            continue
        s = slots[r["company_id"]].setdefault(r["person_key"], {
            "types": set(), "edges": [], "statuses": set(), "dates": []})
        s["types"].add(rt)
        s["edges"].append(r["edge_id"])
        s["statuses"].add(r["verification_status"])
        if r["investment_date"]:
            s["dates"].append(r["investment_date"])

    best_tier: dict[str, str] = {}
    for r in con.execute(
            "SELECT e.company_id, s.tier FROM person_company_edges e"
            " JOIN sources s ON s.parent_kind='edge' AND s.parent_id=e.edge_id"
            " WHERE e.is_confirmed=1"):
        cur = best_tier.get(r["company_id"])
        if cur is None or TIER_RANK.get(r["tier"], 0) > TIER_RANK.get(cur, 0):
            best_tier[r["company_id"]] = r["tier"]

    comp = {r["company_id"]: dict(r) for r in con.execute(
        "SELECT c.company_id, c.canonical_name, c.public_or_private, c.ticker, c.country,"
        " c.industry_primary, c.current_status, cs.best_valuation_usd v,"
        " cs.best_valuation_date vd, cs.best_valuation_type vt, cs.staleness_band sb,"
        " cs.best_valuation_confidence vc, cs.valuation_tier tier,"
        " cs.weighted_person_score w, cs.independence_adjusted_score ia,"
        " cs.distinct_information_clusters clusters"
        " FROM companies c LEFT JOIN company_scores cs USING(company_id)")}

    rows = []
    for cid, members in slots.items():
        econ = {pk: s for pk, s in members.items() if s["types"] & ECONOMIC}
        if not econ:
            continue                      # VC-partner-only: not an ownership intersection
        vcp = {pk for pk, s in members.items() if s["types"] & VC_PARTNER}
        direct = sum(1 for s in econ.values() if s["types"] & DIRECT)
        ctrl = sum(1 for s in econ.values() if (s["types"] & CONTROLLED)
                   and not (s["types"] & DIRECT))
        c = comp.get(cid, {})
        ppl = sorted(econ, key=lambda pk: (people.get(pk, {}).get("full_name") or pk))
        names = [people.get(pk, {}).get("full_name") or pk for pk in ppl]

        multi = sum(1 for s in econ.values()
                    if "CONFIRMED_MULTI_SOURCE" in s["statuses"]
                    or "CONFIRMED_PRIMARY" in s["statuses"])
        conf = (f"{best_tier.get(cid, '—')}; {multi}/{len(econ)} people on "
                f"primary or multi-source evidence")

        rows.append({
            "company_id": cid,
            "company": c.get("canonical_name", cid),
            "number_of_elite_people": len(econ),
            "direct_personal_or_founder_count": direct,
            "controlled_family_office_or_fund_count": ctrl,
            "vc_partner_exposure_count": len(vcp),
            "total_incl_vc_partner": len(set(econ) | vcp),
            "names_of_every_person": "; ".join(names),
            "public_or_private": c.get("public_or_private") or "UNKNOWN",
            "current_valuation_if_known": usd(c.get("v")),
            "current_valuation_usd": c.get("v"),
            "valuation_date": c.get("vd") or "",
            "valuation_type": c.get("vt") or "",
            "valuation_staleness": c.get("sb") or "",
            "valuation_confidence": c.get("vc") or "",
            "valuation_tier": c.get("tier") or "TIER_U_UNKNOWN",
            "sector": c.get("industry_primary") or "",
            "country": c.get("country") or "",
            "ticker": c.get("ticker") or "",
            "status": c.get("current_status") or "UNKNOWN",
            "source_confidence": conf,
            # secondary, never used for ordering
            "weighted_score_secondary": c.get("w"),
            "independence_adjusted_secondary": c.get("ia"),
            "distinct_networks_secondary": c.get("clusters"),
            "technical_elite_count": sum(1 for pk in ppl
                                         if people.get(pk, {}).get("is_tech_elite")),
            "billionaire_founder_count": sum(1 for pk in ppl
                                             if people.get(pk, {}).get("is_big_founder")),
            "frontier_ai_count": sum(1 for pk in ppl
                                     if people.get(pk, {}).get("is_frontier_ai")),
            "distinct_primary_domains": len({people.get(pk, {}).get("cluster")
                                             for pk in ppl}),
            "technical_elite_names": "; ".join(
                people[pk]["full_name"] for pk in ppl if people.get(pk, {}).get("is_tech_elite")),
            "_people": ppl,
            "_members": econ,
            "_vcp": sorted(vcp),
        })

    # MAIN SORT: raw count, descending. Nothing weighted touches this.
    rows.sort(key=lambda r: (-r["number_of_elite_people"],
                             -r["direct_personal_or_founder_count"],
                             r["company"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return con, people, rows


CSV_COLS = ["rank", "company", "number_of_elite_people", "direct_personal_or_founder_count",
            "controlled_family_office_or_fund_count", "vc_partner_exposure_count",
            "total_incl_vc_partner", "names_of_every_person", "public_or_private", "ticker",
            "current_valuation_if_known", "current_valuation_usd", "valuation_date",
            "valuation_type", "valuation_staleness", "valuation_confidence", "valuation_tier",
            "sector", "country", "status", "source_confidence", "technical_elite_count",
            "billionaire_founder_count", "frontier_ai_count", "distinct_primary_domains",
            "technical_elite_names", "weighted_score_secondary",
            "independence_adjusted_secondary", "distinct_networks_secondary", "company_id"]


def table(rows, n=30, start=1):
    out = ["| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows[:n], start):
        out.append(
            f"| {i} | **{r['company']}** | **{r['number_of_elite_people']}** "
            f"| {r['direct_personal_or_founder_count']} "
            f"| {r['controlled_family_office_or_fund_count']} "
            f"| {r['vc_partner_exposure_count']} "
            f"| {r['current_valuation_if_known'] or '—'} | {r['valuation_tier'][5:6]} "
            f"| {r['sector'] or '—'} | {r['status']} |")
    return "\n".join(out) + "\n"


def report(con, people, rows):
    total_people = con.execute("SELECT COUNT(*) FROM people").fetchone()[0]
    L = [
        "# PORTFOLIO INTERSECTIONS — which companies show up in the most elite portfolios?", "",
        f"_{len(rows)} companies have at least one tracked person with confirmed economic "
        f"ownership exposure, out of {total_people} people tracked._", "",
        "## The metric", "",
        "```",
        "PORTFOLIO_INTERSECTION_COUNT =",
        "    distinct tracked people with a CONFIRMED relationship to the company",
        "    representing real economic ownership exposure",
        "```", "",
        "**Counted** — `PERSONAL_ANGEL_INVESTMENT`, `PERSONAL_EQUITY_INVESTMENT`, "
        "`SPV_INVESTMENT`, `FOUNDER_EQUITY` (the *direct* column) and "
        "`FAMILY_OFFICE_INVESTMENT`, `CONTROLLED_FUND_INVESTMENT` (the *controlled* column).", "",
        "**Shown but NOT counted in the ranking** — `VC_FUND_PARTNER_INVESTMENT`, in its own "
        "column. A partner at a firm they do not control has exposure to the deal, not "
        "necessarily to the company.", "",
        "**Excluded entirely** — `BOARD_ONLY`, `ADVISOR_ONLY`, `GRANT_FUNDING`, "
        "`PHILANTHROPIC_FUNDING`, `LP_INDIRECT`, `DEBT_FINANCING`, "
        "`CORPORATE_STRATEGIC_INVESTMENT`, `OTHER_VERIFIED`. None of these is ownership.", "",
        "**One person counts once per company**, regardless of how many rounds they joined or "
        "how many sources confirm it. Only `CONFIRMED_*` edges count; anything uncertain is "
        "left out.", "",
        "The ranking is the **raw count**. Weighted and independence-adjusted scores appear as "
        "secondary columns in the CSV and never affect the ordering.", "",
        "---", "",
        "# OUTPUT 1 — TOP 30 PORTFOLIO INTERSECTIONS", "",
        table(rows, 30),
        "",
        "_Tier key: A = under $500M · B = $500M–$1B · C = $1B–$5B · D = $5B+ · U = unknown._",
        "Full ranked list of all "
        f"{len(rows)} companies: `data/exports/portfolio_intersections.csv`.", "",
        "---", "",
        "# OUTPUT 2 — THE ACTUAL INTERSECTIONS", "",
        "Every tracked person behind each of the top 30, with the relationship that counted "
        "them. `(VC)` marks people with fund-partner exposure only — they are listed for "
        "completeness and are **not** in the headline count.", "",
    ]
    for r in rows[:30]:
        L += [f"### {r['rank']}. {r['company']} — {r['number_of_elite_people']} people",
              "",
              f"_{r['current_valuation_if_known'] or 'valuation unknown'}"
              f"{' · ' + r['valuation_date'] if r['valuation_date'] else ''}"
              f" · {r['public_or_private']} · {r['sector'] or 'sector unlabelled'}"
              f" · {r['status']}_", ""]
        for pk in r["_people"]:
            m = r["_members"][pk]
            p = people.get(pk, {})
            tags = []
            if p.get("is_tech_elite"):
                tags.append("technical elite")
            if p.get("is_big_founder"):
                tags.append("founder w/ large personal capital")
            d = min(m["dates"]) if m["dates"] else None
            L.append(f"- **{p.get('full_name') or pk}** — {', '.join(sorted(m['types']))}"
                     f"{' · ' + d if d else ''}"
                     f"{'  _(' + '; '.join(tags) + ')_' if tags else ''}")
        if r["_vcp"]:
            L.append(f"- _(VC) fund-partner exposure only: "
                     f"{', '.join(people.get(pk, {}).get('full_name') or pk for pk in r['_vcp'])}_")
        L += ["", f"**{r['number_of_elite_people']} total**", ""]

    L += ["---", "", "# OUTPUT 3 — THE SAME METRIC, BY VALUATION BUCKET", "",
          "Identical raw count, partitioned by the best sourced current valuation. "
          "**The unknown bucket is not a leftover pile** — most of the graph is in it, because "
          "portfolio pages name companies without valuing them, and several of the most "
          "interesting names are there.", ""]
    under1b = [r for r in rows if r["valuation_tier"] in
               ("TIER_A_UNDER_500M", "TIER_B_500M_TO_1B")]
    L += [f"## Combined: everything under $1B — {len(under1b)} companies", "",
          "**There are not 30 companies here, and the reason matters.** Only "
          f"{len(under1b)} companies in the whole graph carry a *sourced* valuation below "
          "$1B. That is a statement about valuation coverage, not about how many small "
          "companies elite people back: "
          f"{sum(1 for r in rows if r['valuation_tier'] == 'TIER_U_UNKNOWN')} companies have "
          "no sourced valuation at all, and that is where the genuinely early, genuinely "
          "obscure companies live. Portfolio pages name companies without valuing them.", "",
          "Several rows below are also acquired, bankrupt or shut down — kept because they "
          "are factually in the bucket, but they are history, not opportunities.", ""]
    L.append(table(under1b, 40))
    L += ["", "### The sub-$1B universe the valuations cannot see", "",
          "Unvalued companies with **3 or more** elite backers, which is where most "
          "genuinely small companies in this graph actually sit. Size is unknown, so these "
          "are **not** confirmed to be under $1B — but the early-stage ones are the closest "
          "thing to an answer to 'small company, many elite backers'.", ""]
    unk3 = sorted([r for r in rows if r["valuation_tier"] == "TIER_U_UNKNOWN"
                   and r["number_of_elite_people"] >= 3],
                  key=lambda r: (-r["number_of_elite_people"], -r["technical_elite_count"],
                                 r["company"]))
    L += ["| # | company | backers | technical elite | sector | who |",
          "|---|---|---|---|---|---|"]
    for i, r in enumerate(unk3[:30], 1):
        L.append(f"| {i} | **{r['company']}** | **{r['number_of_elite_people']}** "
                 f"| {r['technical_elite_count']} | {r['sector'] or '—'} "
                 f"| {r['names_of_every_person'][:120]} |")
    L.append("")

    for t in TIER_ORDER:
        sub = [r for r in rows if r["valuation_tier"] == t]
        L += [f"## {TIER_LABEL[t]} — {len(sub)} companies", ""]
        L.append(table(sub, 20) if sub else "_None._\n")
        L.append("")

    L += ["---", "", "# OUTPUT 4 — INTERESTING OBSCURE INTERSECTIONS", "",
          "`ANALYTICAL INTERPRETATION`, kept deliberately separate from the factual ranking "
          "above. Filter: **private or unvalued**, **not** above $5B, **≥2** elite backers, "
          "and either a frontier sector or **≥2 technically elite** backers. Ranked by "
          "technically elite backers, then raw count.", "",
          "Household names are removed by an explicit list in the script, because obscurity "
          "is a judgement and not a field in the data — a company can sit in the unknown "
          "bucket simply because nobody sourced a market cap for it, which is how Alphabet "
          "first appeared here.", ""]
    obscure = [r for r in rows
               if r["valuation_tier"] != "TIER_D_5B_PLUS"
               and r["public_or_private"] != "PUBLIC"
               and not r["ticker"]
               and r["company"].strip().lower() not in NOT_OBSCURE
               and r["status"] not in ("ACQUIRED", "MERGED", "SHUT_DOWN", "BANKRUPT",
                                       "OPERATING_PUBLIC")
               and r["number_of_elite_people"] >= 2
               and (r["technical_elite_count"] >= 2 or r["sector"] in FRONTIER)]
    obscure.sort(key=lambda r: (-r["technical_elite_count"], -r["number_of_elite_people"],
                                r["company"]))
    if obscure:
        L += ["| company | backers | technical elite | valuation | sector | who |",
              "|---|---|---|---|---|---|"]
        for r in obscure[:30]:
            L.append(f"| **{r['company']}** | {r['number_of_elite_people']} "
                     f"| {r['technical_elite_count']} "
                     f"| {r['current_valuation_if_known'] or 'unknown'} "
                     f"| {r['sector'] or '—'} | {r['names_of_every_person'][:120]} |")
    else:
        L.append("_No company passes this filter._")

    L += ["", "---", "", "# OUTPUT 5 — HIGHEST INTERSECTION BY PERSON TYPE", "",
          "Secondary views. The main answer above is still company → how many tracked people "
          "own or backed it.", ""]
    views = [
        ("Most technically elite backers", "technical_elite_count",
         "Technical band ≥4 with a research or academic archetype, or band 5 with a "
         "founder-operator archetype. Celebrity is never evidence of technical capability."),
        ("Most founder-operators with large personal capital", "billionaire_founder_count",
         "**PROXY, not a sourced net-worth claim**: founder-operators at capital-flexibility "
         "band 5."),
        ("Most frontier-AI people", "frontier_ai_count",
         "People whose primary information lens is AI."),
        ("Most distinct primary domains represented", "distinct_primary_domains",
         "One primary lens per person, so a few multi-domain people cannot manufacture "
         "apparent breadth."),
    ]
    for title, key, note in views:
        sub = sorted([r for r in rows if r[key] > 0],
                     key=lambda r: (-r[key], -r["number_of_elite_people"], r["company"]))[:12]
        L += [f"## {title}", "", f"_{note}_", "",
              f"| company | {key.replace('_', ' ')} | total backers | valuation | who |",
              "|---|---|---|---|---|"]
        for r in sub:
            who = (r["technical_elite_names"] if key == "technical_elite_count"
                   else r["names_of_every_person"])
            L.append(f"| **{r['company']}** | **{r[key]}** | {r['number_of_elite_people']} "
                     f"| {r['current_valuation_if_known'] or 'unknown'} | {who[:110]} |")
        L.append("")

    L += ["---", "", "## What this does and does not say", "",
          "`FACT` — every count above is distinct people with sourced, confirmed economic "
          "exposure. Each is traceable: `company_id` → `people_list` → `edge_ids` → `sources` "
          "→ original URL.", "",
          "`NOT ESTABLISHED` — that a high intersection predicts anything. The backtest in "
          "`reports/BACKTEST.md` cannot yet discriminate winners from failures, because the "
          "failure arm is under-collected. Several companies in the tables above had heavy "
          "elite backing and failed.", "",
          "`COVERAGE` — a company appears here only because someone published something. An "
          "equally backed company whose investors publish nothing is absent entirely, and "
          "large fund portfolios (ARCH, Breakthrough Energy, Khosla, Lowercarbon) contribute "
          "many controlled-fund rows while quiet personal cheques contribute none.", ""]
    return "\n".join(L) + "\n"


def main():
    con, people, rows = build()
    out_csv = ROOT / "data" / "exports" / "portfolio_intersections.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    md = ROOT / "reports" / "PORTFOLIO_INTERSECTIONS.md"
    md.write_text(report(con, people, rows))

    # reconciliation: the stored count must equal the edges underneath it
    bad = 0
    for r in rows[:200]:
        n = con.execute(
            "SELECT COUNT(DISTINCT person_key) FROM person_company_edges"
            " WHERE company_id=? AND is_confirmed=1 AND relationship_type IN "
            f"({','.join('?' * len(ECONOMIC))})",
            (r["company_id"], *sorted(ECONOMIC))).fetchone()[0]
        if n != r["number_of_elite_people"]:
            bad += 1
            print(f"  MISMATCH {r['company']}: stored {r['number_of_elite_people']} vs {n}")
    print(f"{len(rows)} companies ranked -> {out_csv}")
    print(f"report -> {md}")
    print(f"reconciliation over top 200: {'OK' if bad == 0 else str(bad) + ' MISMATCHES'}")
    print("\nTop 15:")
    for r in rows[:15]:
        print(f"  {r['rank']:2d}. {r['company'][:36]:38s} {r['number_of_elite_people']:2d} people "
              f"(direct {r['direct_personal_or_founder_count']}, "
              f"ctrl {r['controlled_family_office_or_fund_count']}, "
              f"vc {r['vc_partner_exposure_count']})  "
              f"{r['current_valuation_if_known'] or 'unknown':>10s}  {r['valuation_tier'][5:6]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
