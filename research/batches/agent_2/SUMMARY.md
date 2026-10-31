# agent_2 — Energy / Climate / Industrial / Deep Tech

Collected 2026-09-16. `python3 scripts/validate_batch.py research/batches/agent_2` → **OK**.

| file | records |
|---|---|
| edges.jsonl | 868 |
| companies.jsonl | 67 |
| valuations.jsonl | 5 |
| correlations.jsonl | 12 |
| rejected.jsonl | 7 |
| queue.jsonl | 11 |
| people.jsonl | 0 (no person outside the assigned 24 earned an edge) |

**505 distinct companies. 64 distinct source URLs, every one of which I opened.**
1,438 Tier-1 source attachments, 126 Tier-2. No Tier-3 database was used to confirm anything.

## Edges by verification status

| status | n |
|---|---|
| CONFIRMED_PRIMARY | 742 |
| CONFIRMED_MULTI_SOURCE | 104 |
| CONFIRMED_REPUTABLE_SECONDARY | 19 |
| PROBABLE_BUT_NOT_CONFIRMED | 3 |

## Edges by relationship type

| type | n |
|---|---|
| CONTROLLED_FUND_INVESTMENT | 488 |
| VC_FUND_PARTNER_INVESTMENT | 255 |
| FAMILY_OFFICE_INVESTMENT | 41 |
| FOUNDER_EQUITY | 31 |
| PERSONAL_EQUITY_INVESTMENT | 22 |
| BOARD_ONLY | 11 |
| PHILANTHROPIC_FUNDING | 9 |
| ADVISOR_ONLY | 8 |
| OTHER_VERIFIED | 2 |
| CORPORATE_STRATEGIC_INVESTMENT | 1 |

**There is not one `PERSONAL_ANGEL_INVESTMENT` edge in this batch.** In this domain the money
moves through funds and family offices, and I refused to upgrade a fund position into a
personal cheque. The 22 `PERSONAL_EQUITY_INVESTMENT` edges are all Michael Liebreich, who
publishes his own register of direct holdings.

## People covered (24/24 attempted, 24/24 produced at least one edge)

| person | edges | basis |
|---|---|---|
| carmichael_roberts | 130 | Material Impact (co-founded → controlled fund) + BEV investment-committee co-lead (partner) |
| bill_gates | 124 | BEV portfolio (controlled fund), Cascade Investment + Gates Frontier SEC filings, TerraPower founder |
| vinod_khosla | 120 | Khosla Ventures portfolio (controlled fund), Sun/Daisy founder equity, KPCB-era partner deals |
| chris_sacca | 112 | Lowercarbon portfolio (controlled fund), Lowercase Capital |
| crystal_sacca | 105 | Lowercarbon portfolio (controlled fund), Lowercase Capital |
| eric_toone | 105 | BEV managing partner / required deal sign-off (partner), two pharma scientific-founder roles |
| michael_liebreich | 29 | his own published register of interests — the cleanest personal-holding disclosure of anyone on my list |
| john_doerr | 26 | Kleiner Perkins' own page tags each company "Partners: John Doerr" plus a "Partnered Since" year |
| josh_wolfe | 19 | Lux Capital companies page partner tags + his own Lux bio |
| andrew_forrest | 16 | Fortescue/Tattarang founder; Tattarang portfolio (family office) |
| robert_friedland | 15 | Ivanhoe Electric board bio is an unusually complete, dated career record |
| ion_yadigaroglu | 10 | Capricorn / Technology Impact Fund (partner) |
| matt_rogers | 11 | Nest/Mill/Incite founder; Incite case studies split into Investments vs Philanthropy |
| steve_jurvetson | 8 | Future Ventures home page (only 8 companies are named in text) |
| maryanna_saenko | 8 | same |
| rachel_slaybaugh | 7 | DCVC partner page — her "Why We Invested" posts |
| shayle_kann | 6 | EIP team page names four of his deals; Ceibo board seat |
| jigar_shah | 5 | SunEdison / Generate Capital / Multiplier founder roles |
| gina_rinehart | 4 | Hancock Prospecting SEC 13G + Reuters |
| lukas_walton | 3 | Builders Vision / S2G founder roles only |
| bilal_zuberi | 2 | Lux companies page partner tags |
| bob_mumgaard | 1 | CFS co-founder |
| dennis_whyte | 1 | CFS co-founder |
| david_kirtley | 1 | Helion founder |

## Whose portfolio could NOT be reconstructed, and why

- **lukas_walton (WATCHLIST).** Builders Vision manages >$15bn and is explicitly an investment
  platform, but **it publishes no portfolio list at all** — home, "Who We Are" and the Lukas
  Walton bio page name no portfolio company. S2G was spun out as an independent RIA in 2024,
  further detaching deal names from him. Every company name I could find for Builders Vision
  came from Tier-3 databases, so none became an edge. *Documented absence is the finding here.*
  Next: S2G Investments' own portfolio page; company releases naming Builders Vision.
- **gina_rinehart (WATCHLIST).** Hancock Prospecting is private and files almost nothing in the
  US: exactly two SEC schedules exist (MP Materials). The Australian positions (Liontown, Azure,
  Delta Lithium, Vulcan, St George, and exact Lynas/Arafura/Brazilian Rare Earths percentages)
  live in ASX Form 604 substantial-holder notices, which I did not open — the ASX announcements
  platform was not reachable inside my time budget. Four edges is a floor, not her real
  exposure. Queued HIGH.
- **bob_mumgaard, dennis_whyte, david_kirtley (operators).** One founder edge each is correct
  and complete: these are fusion CEOs/scientists, not allocators. I found no evidence any of
  them invests outside their own company, and I will not invent any.
- **steve_jurvetson / maryanna_saenko.** `future.ventures/investments` renders its entire
  portfolio as image logos with no machine-readable names — the page body says "Each logo below
  links to a founding story" and then contains no text. I used only the eight companies named in
  prose on the home page. Their real portfolio is ~60 companies. This is the single biggest
  recoverable gap in the batch.
- **carmichael_roberts' own founded companies.** Material Impact's bio says he "co-founded
  several ventures" without naming them. The named list (MC10, 1366 Technologies, Arsenal
  Medical, Diagnostics For All, Surface Logix, Foro Energy, Lyra Therapeutics) exists only in
  scraped LinkedIn data, which I refused to use. Queued HIGH — pre-2015 deep-tech founder edges.
- **bilal_zuberi.** Lux's public companies page tags him on only two entries, and his new fund
  (Red Glass Ventures, 2025) has no reachable website or Form D. His known Lux portfolio
  (Saildrone, Desktop Metal, Evolv, Nozomi, OpenSpace, Ironclad…) is attested only on LinkedIn.

## Paywalled / inaccessible

- **Bloomberg** — paywalled throughout. I removed the one edge that would have rested on it (Ion
  Yadigaroglu / Form Energy) and queued it instead. The Sacca fusion-fund piece and the Rinehart
  rare-earths feature are also behind the wall and were not bypassed.
- **Forbes** — the $800m Rinehart rare-earths portfolio piece is behind a wall; not used.
- **Parallel Search MCP** hit its free-tier rate limit mid-run; the rest was done on Exa,
  WebFetch/WebSearch and direct `curl` to SEC EDGAR.
- `breakthroughenergy.org/people` and `cfs.energy/*` returned crawl errors repeatedly; worked
  round them with congress.gov and MIT primary sources.
- `future.ventures/investments`, `terrapower.com/people/`, `capricorninvestmentgroup.com`:
  crawl failures or logo-only rendering.

## Source-type mapping I used (so an auditor can check me)

The controlled vocabulary has no generic "company website" type. I mapped consistently:
a fund's own portfolio listing → `investor_portfolio_page`; a fund's or a person's own bio page
→ `personal_website`; a company's own About/Board/Team/press page → `company_press_release`;
an official institutional biography (DOE, congress.gov) → `official_interview_or_statement`.
**Every `evidence_summary` states in words exactly what kind of page it is**, so the mapping is
recoverable even if the orchestrator disagrees with it.

## Name normalisation the orchestrator must resolve

Company names are written exactly as each source writes them, per the contract. These pairs are
the same company seen through two different funds' portfolio pages:

`Antora` / `Antora Energy` · `Brimstone` / `Brimstone Energy` · `Commonwealth Fusion` /
`Commonwealth Fusion Systems` / `Commonwealth Fusion Systems (CFS)` · `Heart` /
`Heart Aerospace` · `Heirloom` / `Heirloom Carbon` · `Lilac` / `Lilac Solutions` ·
`MagLev Aero` / `Maglev Aero` · `Physical Intelligence` / `Physical intelligence` ·
`RedoxBlox` / `Redoxblox` · `Sublime` / `Sublime Systems` · `Zap` / `Zap Energy`

## The interesting part: small, obscure companies with several elite backers

Excluding the obvious (Commonwealth Fusion, QuantumScape, Redwood), these pre-unicorn
climate-industrial names carry three or more of my 24:

- **Airloom Energy** — wind on a "clothesline". Lowercarbon *and* BEV. Tiny, weird, twice-backed.
- **Xcimer Energy** — laser inertial fusion. Lowercarbon *and* BEV.
- **Electra** — electrified iron for green steel. Lowercarbon *and* BEV.
- **Dioxycle** — low-temperature CO2 electrolysis. Lowercarbon *and* BEV.
- **Yard Stick** — soil-carbon measurement. Lowercarbon *and* BEV.
- **Verdox** — electroswing carbon capture. Lowercarbon *and* BEV.
- **Mariana Minerals** — software-first minerals developer. BEV *and* Khosla Ventures.
- **RedoxBlox** — thermochemical industrial heat storage. BEV *and* Khosla Ventures.
- **Fourth Power** — thermal ("sun in a box") storage. BEV *and* DCVC/Slaybaugh.
- **Equilibrium Energy** — BEV *and* DCVC/Slaybaugh.
- **Mill** — the rare one where a backer is also the founder: Matt Rogers founded it, and both
  Lowercarbon and BEV are in.
- **Koloma**, **GALY**, **MagLev Aero** — each sits in *both* BEV and Carmichael Roberts' own
  Material Impact portfolio, i.e. he backed them twice through two different vehicles.
- **Ceibo** (copper from primary sulphides) — its own team page carries both Shayle Kann of EIP
  and Samir Kaul of Khosla Ventures. A genuinely obscure company with two elite funds seated
  around it.

Single-backer but unusually obscure and worth watching: **I-ROX** (pulsed-power rock
fragmentation — note Robert Friedland's I-Pulse is the pulsed-power incumbent, so BEV has funded
a company in his exact technical lane), **Mantle8** and **Koloma** (geologic hydrogen, two
separate BEV bets), **Still Bright** (copper), **Molten Industries**, **Heron Power**,
**Zanskar**, **Lithios**, **Novalith**, **Milvus Advanced**, **Arca**, **Genomines**, **Aepnus**,
**Foundation Alloy**, **Amperesand**, **Hertha Metals**, **Mazama**, **Magrathea** (magnesium
from seawater — Liebreich's personal money).

## Deliberate non-findings

`rejected.jsonl` records seven claims chased and killed, the most important being: DOE Loan
Programs Office borrowers are **not** Jigar Shah edges (US federal money, not his); BEV portfolio
companies are **not** personal Bill Gates angel investments; BEV holdings are **not**
controlled-fund edges for Carmichael Roberts (it is Gates' fund, not his); and Capricorn is
recorded as a partner fund for Ion Yadigaroglu, not a controlled one, because Capricorn's own
team page calls him only "Partner | Investments", while the co-founder description appears
only in secondary profiles I did not open in full — conflicting evidence resolved downward.
