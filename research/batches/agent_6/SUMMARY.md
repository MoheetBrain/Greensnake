# Agent 6 — Billionaire Founders / Family Offices / Crossover

Collected 2026-09-16. Validates clean against `scripts/validate_batch.py`.

| file | records |
|---|---|
| `edges.jsonl` | 471 |
| `companies.jsonl` | 132 |
| `valuations.jsonl` | 2 |
| `correlations.jsonl` | 16 |
| `rejected.jsonl` | 9 |
| `queue.jsonl` | 13 |
| `people.jsonl` | 0 (all 33 assignees already in `people_universe.yaml`) |

**471 edges across 448 distinct companies. All 33 assigned people have at least one edge.**

## Verification mix

| status | n |
|---|---|
| `CONFIRMED_PRIMARY` | 275 |
| `CONFIRMED_MULTI_SOURCE` | 178 |
| `CONFIRMED_REPUTABLE_SECONDARY` | 17 |
| `PROBABLE_BUT_NOT_CONFIRMED` | 1 |

453 of 471 edges (96%) carry at least one Tier-1 source. The single non-confirmed edge
(Bezos -> Altos Labs) is deliberate and explained below.

By relationship type: `FAMILY_OFFICE_INVESTMENT` 358, `CONTROLLED_FUND_INVESTMENT` 64,
`FOUNDER_EQUITY` 33, `PERSONAL_EQUITY_INVESTMENT` 7, `PHILANTHROPIC_FUNDING` 6,
`BOARD_ONLY` 1, `CORPORATE_STRATEGIC_INVESTMENT` 1, `OTHER_VERIFIED` 1.

## How vehicles were classified

The brief listed named vehicles to record as `FAMILY_OFFICE_INVESTMENT`. I followed that for
vehicles deploying one person's own capital (Bezos Expeditions, Grok Ventures, Skip Capital,
Horizons Ventures, Kima Ventures, Aglae Ventures, MSD Capital, Duquesne Family Office,
Emerson Collective, Prima Materia). I used `CONTROLLED_FUND_INVESTMENT` for three vehicles
that demonstrably raised outside LP capital — **Point72 Ventures**, **QuantumLight** and
**Social Capital** — because the enum defines that type as "fund they founded / control", and
calling third-party-LP money a family office would overstate personal economic exposure.
Each such edge says so in `verification_notes`.

Philanthropy was never recorded as equity: Parker Institute, Griffin Catalyst, Good Ventures,
USAFacts, Signal Foundation and the Canva founders' GiveDirectly commitment are
`PHILANTHROPIC_FUNDING`.

## Where the volume came from

Nine vehicle-owned portfolio pages / filings did most of the work. All were opened and parsed,
never read from a search snippet:

| vehicle | person | edges | source |
|---|---|---|---|
| Horizons Ventures | Li Ka-shing | 102 | own portfolio page (per-company date + country) |
| Duquesne Family Office | Druckenmiller | 84 | 13F-HR infotable, period 2026-06-30 |
| Kima Ventures | Xavier Niel | 52 | own portfolio page (984 listed; 52 frontier-tech selected) |
| QuantumLight | Storonsky | 41 | own portfolio table (sector + geography) |
| Skip Capital | Scott Farquhar | 39 | own `/technology` page, logo-to-caption pairs |
| Bezos Expeditions | Jeff Bezos | 31 | own "Selected Investments" list |
| Grok Ventures | Cannon-Brookes | 28 | own portfolio page (first-invested year) |
| Point72 Ventures | Steve Cohen | 22 | own portfolio page (non-US subset only) |
| Aglae Ventures | Bernard Arnault | 10 | own companies list |

Public-company founder stakes came from SEC proxies and filings with exact share counts
(Alphabet, Airbnb, Block, Zoom, Atlassian, Dell, Amazon, Nu Holdings, Twitter, MercadoLibre
13D/A, MSD Capital 13F).

## Geographic independence

Of the 132 company records: France 25, UK 14, Australia 9, Canada 8, Indonesia 6, India 5,
Israel 5, Germany 4, Hong Kong 4, Sweden 3, Brazil 3, Turkiye 3, Belgium 2, Mexico 2,
Philippines 2, Denmark / Colombia / Bermuda / Switzerland / Netherlands / Argentina 1 each,
US 6, plus 23 with country unstated (Grok's page does not publish it — queued).

## Small / obscure companies with more than one elite backer

18 companies in this batch have >=2 distinct backers. The interesting ones are the small,
mostly non-US names:

- **Spore.Bio** (Paris, instant AI microbiology) — Point72 Ventures *and* Kima Ventures.
  The most striking overlap in the batch: a US hedge-fund venture arm and a French angel
  vehicle in the same seed/Series-A company.
- **Kimia** (AI for chemists) — Horizons Ventures *and* Skip Capital.
- **Loam Bio** (Australian soil-carbon) — Grok Ventures (first invested 2019) *and*
  Horizons Ventures (2019). Two family offices, same company, same year.
- **Neara** (3D models for electric-utility infrastructure) — Grok *and* Skip.
- **Harrison.ai** (Australian clinical AI) — Horizons *and* Skip.
- **Brighte** and **Zoomo** (Australian home-electrification finance / e-bikes) — Grok *and* Skip.
- **Arena** (enterprise AI) — QuantumLight *and* Skip Capital.
- **Airwallex** — Horizons *and* Skip.

Single-backer but unusually obscure and worth surfacing: Isentroniq and Viqthor (wiring and RF
control for superconducting quantum computers, FR), Vertical Compute (BE semiconductor),
SKYNOPY / ThrustMe / Gama (FR space), Alta Ares (FR air defence), Beyond Aero (FR hydrogen
aviation), Apollo Atomics (US micro-reactors), Cure 51 (FR cancer-outlier database), Endolith
(copper mining with microbes), Rhizocore, MAKO (shark-skin film for aviation), Cortical Labs
(AU biological computers), Micro Connect (HK), Alva Auto / Bank Jasa Jakarta / SATU Dental (ID),
Enter (BR legaltech), Midas and Sipay (TR), Yuno (CO), Tsuga (FR).

## People whose portfolios could NOT be reconstructed

This is the important negative result for this workstream.

- **Sergey Brin** — 1 edge (Alphabet founder stake). **Bayshore Global Management does not
  appear as a filer in EDGAR at all** — no 13F, no 13D/G — and publishes no website or
  portfolio page. A family office reported to manage a very large book is invisible to every
  disclosure route I could reach. Queued HIGH (Singapore ACRA, Form D).
- **Larry Page** — 1 investment edge (Kittyhawk, since wound down) plus his Alphabet stake.
  Opener, Wisk and Planetary Resources could not be verified; Wisk is a Boeing JV spun out of
  Kittyhawk's Cora programme, a corporate transaction rather than evidence of a Page cheque.
- **Jan Koum** — 1 edge (WhatsApp founder equity, from Facebook's own acquisition release).
  **Genuine near-total absence.** Snapchat / Uber / Airbnb / Pinterest / Sacramento Kings
  claims circulate only on net-worth aggregator sites with no round, date or filing; the three
  checkable ones are in `rejected.jsonl`. He is in neither Airbnb's nor Uber's proxy.
- **Brian Acton** — 2 edges (WhatsApp founding; the $50m that created the Signal Foundation,
  from Signal's own launch post). Nothing else verified. The larger $105m loan figure and the
  Trak N Tell / DuckDuckGo investments are queued, not written.
- **Eric Yuan** — 1 edge (Zoom founder stake from Zoom's proxy). No personal vehicle, no
  portfolio page, no funding announcement naming him.
- **Travis Kalanick** — 2 edges (City Storage Solutions controlling stake, $150m, March 2018;
  CloudKitchens). The 10100 Fund names no portfolio company anywhere public. He has also
  **disappeared entirely from Uber's current proxy** — not in the ownership table, not a
  director — so a present-tense Uber equity edge is unsupported and was rejected.
- **Chamath Palihapitiya** — 3 edges. Social Capital has no portfolio page; holdings live in
  annual letters and the 2025 letter's portfolio deep dive is members-only. Only Groq (from his
  own first-person "I made the decision to invest ten years ago") and 8090 survived.
- **Laurene Powell Jobs** — 5 edges. Emerson Collective publishes no portfolio page; the named
  rounds come from CNBC's reporting on Fintrx data.
- **Marcos Galperin, David Velez, Melanie Perkins, Mark Cuban, Anne Wojcicki, Steve Ballmer,
  Masayoshi Son, Michael Dell, Ken Griffin, Dustin Moskovitz, Brian Chesky** — covered, but
  mostly via founder/controlling stakes rather than reconstructable outbound portfolios.

## Claims investigated and killed (`rejected.jsonl`)

1-3. Jan Koum -> Snapchat / Uber / Airbnb — aggregator-only, no original source to chase.

4. **Ken Griffin -> Citadel's 13F portfolio.** I pulled it: **16,127 positions**, dominated by
S&P 500 and Nasdaq ETFs held in multiple lots. That is market-making and hedging inventory, not
investment selection. Writing it would have injected ~16,000 meaningless rows and inflated every
overlap metric in the graph. Deliberately not collected — Griffin has 3 edges instead.

5. Jeff Bezos -> Altos Labs — kept at `PROBABLE_BUT_NOT_CONFIRMED`; see below.

6. **Michael Dell -> MSD Partners' 13F.** MSD Partners L.P. (CIK 1514334) is a different filer
from MSD Capital L.P. (CIK 1105497) and manages outside client capital as part of BDT & MSD. Its
nine positions (Oddity Tech, ReNew Energy Global, Azul, Xponential, Lindblad, Safehold,
ServiceTitan, Office Properties, TriSalus) were **not** written as Dell family-office edges; only
MSD Capital's three were.

7. Melanie Perkins' "~18% of Canva" — founder role confirmed from Canva's own newsroom, but the
percentage traces only to secondary blogs, so `ownership_percentage` is null.

8. Steve Ballmer's "4% of Microsoft" — the holding is confirmed in his own words to GeekWire, but
4% is his 2014 departure figure which he has never updated; left null.

### The Altos Labs case
Every Bezos-Altos trail leads back to one MIT Technology Review sentence: *"some people briefed
by the company have been told that its investors include Jeff Bezos."* The same article says of
Milner, in contrast, that *"Technology Review confirmed"* the investment. Altos is also absent
from Bezos Expeditions' own Selected Investments list. So Milner -> Altos is
`CONFIRMED_REPUTABLE_SECONDARY` and Bezos -> Altos is `PROBABLE_BUT_NOT_CONFIRMED`, with a
HIGH-priority queue row pointing at Altos Labs' UK Companies House filings.

## Sources that failed or were gated

- **startsmall.llc** looks like Jack Dorsey's official grant tracker and carries a full
  machine-readable record of 386 grants with amounts and dates. It prints *"Currently not
  affiliated with Jack/Twitter/Square. Data is pulled from a copy of his Google sheet."*
  **It is an unofficial mirror and cannot carry Tier-1 status.** No Start Small grant edges were
  written; queued HIGH with a pointer to Dorsey's own published sheet. This is the single biggest
  trap in this workstream.
- `chamath.substack.com` 2025 annual letter — portfolio deep dive behind a members wall.
- `helsing.ai` Series E press release — URL returned no content, so the US$1.8bn Series E and the
  reported EUR12bn Series D valuation were **not** recorded.
- `emersoncollective.com`, `socialcapital.com`, `grok.ventures`, `skipcapital.com`,
  `primamateria.com` have no portfolio page at all, or none listing companies.
- FMP's `form13F` and `insiderTrades` tools are gated on this account's plan; **all 13F/13D/proxy
  data here was pulled directly from SEC EDGAR instead**, which is better provenance anyway.
- MercadoLibre's and Asana's proxy ownership rows for Galperin and Moskovitz did not parse
  cleanly; Galperin was recovered from the Galperin Trust's Schedule 13D/A (7.00%), Moskovitz's
  percentage was left null.

## Deliberate omissions

- **Kima Ventures publishes 984 portfolio companies.** I wrote 52 — the frontier-tech,
  non-consumer subset — so Xavier Niel does not swamp the graph with ~1,000 EUR150k seed tickets.
  The full parsed list is reproducible from the same page.
- **Point72 Ventures publishes 161 companies.** I wrote the 22 non-US ones, since the research
  question favours geographic independence and small companies.
- Horizons Ventures dates ending `-01-01` are page placeholders and were normalised to year-only;
  `-MM-01` to `YYYY-MM`. No date was ever guessed.
- 13F `value` is quarter-end market value, not cost, so no 13F edge carries an
  `amount_personally_invested_usd`; the position value is stated in `verification_notes`.
- `ownership_percentage` is null wherever a proxy reports only class-level ownership and voting
  power (e.g. "35.6% of Class B, 31.9% of voting power") rather than a whole-company figure.

## Next steps, in priority order

1. Dorsey's own #startsmall Google Sheet -> ~386 Tier-1 philanthropic edges currently blocked.
2. Bayshore Global (Singapore ACRA, Form D) -> the largest single visibility hole in this batch.
3. Social Capital Hedosophia SPAC S-1/S-4 sponsor share disclosures -> Chamath's SPAC holdings.
4. Altos Labs UK Companies House filings -> settle the Bezos question either way.
5. Form D filings naming Emerson Collective LLC as a purchaser.
6. The remaining ~930 Kima and ~139 Point72 Ventures companies, if breadth beats selectivity.
