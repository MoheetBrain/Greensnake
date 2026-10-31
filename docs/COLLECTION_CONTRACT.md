# Greensnake Collection Contract (v1)

**Every research worker writes into this format. No schema variants.**
A batch that fails `scripts/validate_batch.py` does not enter the database.

## The one rule that outranks everything

> **A PERSON–COMPANY edge may not carry a `CONFIRMED_*` status unless a source
> you actually opened explicitly supports that specific person having that
> specific relationship with that specific company.**

If you are uncertain: set `verification_status` to `PROBABLE_BUT_NOT_CONFIRMED`
or `UNVERIFIED`, and add a `research_queue` row saying what evidence is missing.
`NULL IS SUPERIOR TO FICTION.`

### Never infer an investment from
- their VC firm invested → `VC_FUND_PARTNER_INVESTMENT` (not personal)
- their employer invested → `CORPORATE_STRATEGIC_INVESTMENT` at most
- a board seat → `BOARD_ONLY`
- praise, friendship, an event, a podcast → **not an edge at all**
- "family office rumoured to have participated" → `research_queue`, not an edge
- an article that copied an unsourced claim → find the original or reject
- a Crunchbase-style listing on its own → Tier 3 can *lead*, never *confirm*
- an LP position in a fund that invested → `LP_INDIRECT`
- a commercial/partnership relationship → **not an edge at all**

A search-engine snippet is **not** evidence. You must open the page.
AI-generated text is **never** evidence.

## Output files

Write JSONL (one JSON object per line) to `research/batches/<your_agent_id>/`:

| file | record kind |
|---|---|
| `edges.jsonl` | person→company relationships |
| `companies.jsonl` | canonical company records |
| `valuations.jsonl` | valuation observations |
| `people.jsonl` | people you added beyond your assigned list |
| `correlations.jsonl` | person↔person network links |
| `rejected.jsonl` | investigated and **not** supported |
| `queue.jsonl` | unresolved claims |

Append-only. Never edit another agent's directory.

## `edges.jsonl` record

```json
{
  "person_key": "elad_gil",
  "company_name": "Example Labs",
  "relationship_type": "PERSONAL_ANGEL_INVESTMENT",
  "investment_vehicle": "personal",
  "investment_date": "2023-06",
  "round_name": "Series A",
  "amount_personally_invested_usd": null,
  "round_total_usd": 25000000,
  "entry_valuation_usd": null,
  "entry_valuation_type": null,
  "ownership_percentage": null,
  "verification_status": "CONFIRMED_PRIMARY",
  "verification_notes": "Company's own release names him among individual investors.",
  "date_verified": "2026-09-16",
  "collected_by": "agent_1",
  "sources": [
    {
      "url": "https://example.com/series-a",
      "source_type": "company_press_release",
      "tier": "TIER_1_PRIMARY",
      "publisher": "Example Labs",
      "title": "Example Labs raises $25M Series A",
      "author": null,
      "published_date": "2023-06-14",
      "accessed_date": "2026-09-16",
      "evidence_summary": "Release lists participating individual investors and names Elad Gil among them, separately from the institutional leads."
    }
  ]
}
```

### Field rules
- `person_key` — the slug from `research/people/people_universe.yaml`. If the
  person is not there yet, add them to your `people.jsonl` too.
- `company_name` — the name **as the source writes it**. Canonicalisation is the
  orchestrator's job; do not invent a canonical form.
- `investment_date` — `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. **Unknown → `null`.**
  A guessed date silently corrupts every temporal metric. Never guess.
- `*_usd` fields — plain numbers in **US dollars**. Convert and note the rate in
  `verification_notes` if the source is in another currency. Unknown → `null`.
- `evidence_summary` — 40–700 chars, in your own words, stating *why* this page
  proves *this* relationship. Another researcher must be able to check you from
  it. Do not paste long passages of copyrighted text.

### `verification_status` ladder
| status | requirement (enforced by the validator) |
|---|---|
| `CONFIRMED_PRIMARY` | ≥1 Tier-1 source |
| `CONFIRMED_MULTI_SOURCE` | ≥2 distinct URLs, ≥2 non-database sources |
| `CONFIRMED_REPUTABLE_SECONDARY` | ≥1 Tier-2 source |
| `PROBABLE_BUT_NOT_CONFIRMED` | you believe it, evidence falls short — say why |
| `CONFLICTING_EVIDENCE` | two reputable sources disagree — **preserve both** |
| `UNVERIFIED` | lead only |
| `REJECTED` | put it in `rejected.jsonl` instead |

Only the first three enter the confirmed-overlap calculations.

## Highest-yield search strategy (use in this order)

1. **Official personal portfolio pages.** Many of these people publish their own
   investment lists. One page can yield 30+ Tier-1 edges. Search
   `"<name>" investments site:<their personal domain>`, `"<name>" portfolio`.
2. **Company funding announcements that name individuals.** Search
   `"<company>" "raises" "<name>"`, and read the *investor list paragraph*.
   TechCrunch/Axios/FT funding stories routinely name angels.
3. **Company "investors"/"backers" pages and press releases.**
4. **SEC / Companies House filings** — Form D, S-1 "principal stockholders",
   13D/G, UK PSC and confirmation statements.
5. **Official interviews / first-person statements** ("I invested in X").
6. Tier-3 databases **only to generate leads you then verify elsewhere**.

Work company-by-company as well as person-by-person; funding announcements are
the densest source of individually-named angels.

## `companies.jsonl`
```json
{"canonical_name":"Example Labs","aliases":["Example Labs Inc."],"former_names":[],
 "website":"https://example.com","country":"US","city":"San Francisco",
 "industry_primary":"AI_SOFTWARE","industry_secondary":null,
 "company_description":"<=300 chars, factual","public_or_private":"PRIVATE",
 "ticker":null,"exchange":null,"founding_year":2021,"founders":["A B"],
 "current_status":"OPERATING_PRIVATE","acquired_status":null,"parent_company":null,
 "total_funding_usd":31000000,"notes":null,"collected_by":"agent_1"}
```

## `valuations.jsonl`
```json
{"company_name":"Example Labs","valuation_usd":300000000,
 "valuation_type":"primary_round_post_money","valuation_date":"2023-06",
 "valuation_confidence":"HIGH","share_price":null,"shares_outstanding":null,
 "notes":"Post-money stated in the company release.","collected_by":"agent_1",
 "sources":[{...same shape as edge sources...}]}
```
**Never manufacture a valuation.** No source → no record → the company lands in
`TIER_U_UNKNOWN`, which is a legitimate and interesting outcome, not a failure.
For public companies use a recent market cap and record the date.

## `rejected.jsonl`
```json
{"person_key":"x_y","company_name":"Z","suspected_relationship":"PERSONAL_ANGEL_INVESTMENT",
 "reason_rejected":"Widely repeated, but every source traces to one unsourced blog post; the firm invested, not the individual.",
 "source_url":"https://...","date_checked":"2026-09-16","rejected_by":"agent_1"}
```
This table is as valuable as the confirmed one — it stops bad claims being
rediscovered and promoted later. **Record every claim you chased and killed.**

## `queue.jsonl`
```json
{"claim":"<person> may have angel-invested in <company>","person_key":"x_y",
 "company_name":"Z","reason_unresolved":"Only a paywalled FT piece appears to cover it",
 "sources_checked":"google, company site, SEC full-text","next_source_to_check":"FT archive / Companies House",
 "priority":"HIGH","raised_by":"agent_1","date_raised":"2026-09-16"}
```

## `correlations.jsonl`
```json
{"person_key_a":"a_b","person_key_b":"c_d","correlation_type":"SAME_FIRM",
 "strength":0.9,"evidence":"Both are general partners at the same firm.",
 "source_url":"https://firm.com/team","collected_by":"agent_1"}
```

## Before you finish — mandatory

```bash
cd Greensnake
python3 scripts/validate_batch.py research/batches/<your_agent_id>
```
Fix every error it reports. A batch with errors is not accepted.
Then write a short `SUMMARY.md` in your batch directory: what you covered, what
you could not verify, which people had unreconstructable portfolios, and which
sources were paywalled.
