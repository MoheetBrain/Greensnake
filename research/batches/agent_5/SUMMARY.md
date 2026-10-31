# agent_5 — Major Venture Investors / Super-Angels

Collected 2026-09-16. Validator: `python3 scripts/validate_batch.py research/batches/agent_5` → **OK**.

## Headline counts

| file | records |
|---|---|
| `edges.jsonl` | 1,054 |
| `companies.jsonl` | 71 |
| `valuations.jsonl` | 1 |
| `correlations.jsonl` | 88 |
| `rejected.jsonl` | 28 |
| `queue.jsonl` | 23 |
| `people.jsonl` | 0 (no people added beyond the assigned universe) |

**827 distinct companies. 35 of the 40 assigned people covered. 39 distinct source URLs, every one
of which I opened myself.**

### Edges by verification status
| status | n |
|---|---|
| CONFIRMED_PRIMARY | 1,037 |
| CONFIRMED_REPUTABLE_SECONDARY | 8 |
| CONFIRMED_MULTI_SOURCE | 3 |
| PROBABLE_BUT_NOT_CONFIRMED | 6 |

Source-object tier mix: **1,047 Tier-1 primary, 10 Tier-2 secondary, 0 Tier-3.** No edge in this
batch rests on a private-market database.

### Edges by relationship type
| type | n | what it means here |
|---|---|---|
| CONTROLLED_FUND_INVESTMENT | 496 | their own firm (Gil & Co, Zeev Ventures, Floodgate, 776, SV Angel, Conviction, Felicis, Neo, LAUNCH, Thrive, Hit Forge, YC) |
| VC_FUND_PARTNER_INVESTMENT | 241 | partner at a firm they do **not** control (Sequoia, Greylock, Khosla, General Catalyst, Sutter Hill, Benchmark, USV) |
| PERSONAL_ANGEL_INVESTMENT | 229 | a source shows the **individual** wrote the cheque |
| BOARD_ONLY | 49 | source establishes a board seat and nothing more |
| FOUNDER_EQUITY | 23 | founded / co-founded |
| OTHER_VERIFIED | 14 | crypto protocols, fund entities, employment links |
| PHILANTHROPIC_FUNDING | 2 | Code.org (non-profit) |

The 229 personal-angel edges come from six genuinely personal sources: partovi.org's joint
investments page, gokulrajaram.com, Immad Akhund's own AngelList syndicate page, balajis.com/about,
Cyan Banister's published Tim Ferriss interview transcript, and nav.al.

## Edges per person

alexis_ohanian 115 · mike_maples 113 · hadi_partovi 79 · ron_conway 76 · ali_partovi 70 ·
oren_zeev 50 · fred_wilson 47 · albert_wenger 47 · aydin_senkut 42 · shaun_maguire 40 ·
elad_gil 39 · alfred_lin 38 · balaji_srinivasan 34 · gokul_rajaram 31 · immad_akhund 28 ·
martin_casado 25 · sarah_guo 18 · reid_hoffman 17 · doug_leone 16 · hemant_taneja 14 ·
marc_andreessen 14 · roelof_botha 14 · keith_rabois 12 · josh_kushner 12 · mike_speiser 9 ·
cyan_banister 9 · bill_gurley 9 · ben_horowitz 7 · jason_calacanis 6 · paul_graham 6 ·
naval_ravikant 5 · jessica_livingston 5 · chris_dixon 3 · garry_tan 3 · lachy_groom 1

## Whose portfolios could NOT be reconstructed

Five of the forty produced **zero** edges and one produced only one. Each is a documented absence,
not an omission — all are in `queue.jsonl` with the exact next source to try.

1. **`lee_fixel` (Addition) — hard blocker.** `additionvc.com` is a **parked domain**: `/lander`
   returns a parking script (`window.LANDER_SYSTEM="PW"`, `ap:"parking"`) and `/portfolio`
   redirects into it. The firm has no reachable public site. Next: SEC Form D / Form ADV.
2. **`brad_gerstner` (Altimeter).** `altimeter.com` renders only a firm description and two office
   addresses; `/portfolio` 404s. Next: Altimeter 13F-HR filings on EDGAR.
3. **`philippe_laffont` (Coatue)** and **`chase_coleman` (Tiger Global).** Not reached in this pass.
   Both are public-market-heavy; the right instrument is 13F-HR and 13D/G, not portfolio pages. Any
   firm position would in any case be fund capital, so the interesting question is whether either
   discloses a personal or family-office vehicle.
4. **`michael_moritz`.** He no longer appears on Sequoia's current team page (I checked
   `sequoiacap.com/people/` — the roster is Balkansky, Bek, Buhler, Chen, Corrigan, Goetz, Leone,
   Lin, Lixandru, Maguire, Meyer, Reeder, Robson, Zhan). `sequoiacap.com/people/michael-moritz/`
   redirects to the team index. `crankstart.org` describes the foundation's grant-making but names
   neither Moritz nor a single grantee. His only evidenced link is second-hand, via Alfred Lin's
   Sequoia page recounting Moritz as their partner at LinkExchange and again at Zappos.
   Next: Crankstart Form 990s.
5. **`lachy_groom` — 1 edge only.** He publishes no portfolio page; `lachy.com` timed out and no
   personal domain resolved. Every one of the 100+ attributions I found is Tier-3 (PitchBook,
   CB Insights, Dealroom, Tracxn, Seedtable, EquityFlow), so none could be promoted. The single
   confirmed edge is FOUNDER_EQUITY in **Physical Intelligence**, taken from Sequoia's Alfred Lin
   page, which names him first in that company's founder list. Next: Form D filings naming Lachy
   Groom Fund as promoter.
6. **`josh_kushner` — partial (12 edges).** `thrivecap.com` is a single video page; `/about`,
   `/companies` and `/portfolio` all 404. `jobs.thrivecap.com/companies` is a real Thrive-domain
   portfolio page but lazy-loads: only 12 of a reported ~200 names rendered.
7. **`garry_tan` (3), `chris_dixon` (3), `naval_ravikant` (5), `jessica_livingston` (5)** are thin
   for a different reason: `initialized.com/portfolio` 404s, a16z's page for Dixon says he "made a
   number of personal angel investments" without naming one, and Naval's 300+ angel positions are
   nowhere published by him — his own site names only Twitter and Uber, and AngelList's Q&A adds
   Postmates via Hit Forge.

## Paywalled, parked or unrenderable sources

- `additionvc.com` — domain parked (see above).
- `thrivecap.com` — video-only landing page, all portfolio paths 404.
- `altimeter.com/portfolio`, `initialized.com/portfolio`, `conviction.com/portfolio`,
  `floodgate.com/portfolio`, `neo.com/investments`, `neo.com/companies`, `suttershill.com` —
  404 or returned no content. (Working equivalents were found for Conviction, Floodgate and Neo.)
- `immad.com` and `lachy.com` — did not resolve / timed out.
- `medium.com/@rabois/...` — 403 to WebFetch, retrieved successfully via the Exa fetch tool.
- `businessinsider.com` — blocked to WebFetch; the Exa fetch returned only article chrome, not the
  slideshow body, so Keith Rabois's 2010 personal angel portfolio remains unread.
- `benchmark.com` — deliberately publishes no portfolio; Bill Gurley's edges come from his own blog
  and from Zillow's governance page instead.
- No hard paywall (FT / WSJ / The Information) was hit, because I stayed on primary sources.

## The category error this workstream exists to prevent

`rejected.jsonl` holds 28 kills, most of exactly this shape:

- **roelof_botha → YouTube / Instagram**, **michael_moritz → Google**, **bill_gurley → Uber**,
  **keith_rabois → Faire**: the *firm* invested. Gurley's $11m Uber cheque was Benchmark's; Rabois
  says of Faire "we are the largest shareholder", meaning Khosla Ventures.
- **keith_rabois → Opendoor**: he co-founded it, so it is founder equity, not an angel investment.
- **hemant_taneja → Livongo**: his own page says he co-founded it — recorded as FOUNDER_EQUITY.
- **mike_speiser → Grail / Wavefront**: CNBC names both as *Lacework customers*. A commercial
  relationship is not an edge.
- **jason_calacanis → Uber**: universally described as his personal angel win, but the only source
  I opened (launch.co) says "**we've** backed Uber" — LAUNCH's capital. Left as a controlled-fund
  edge until a primary source shows the personal cheque.
- **elad_gil → Helsing / Shield AI / Saronic / Pacific Fusion / Periodic Labs / Cambridge
  Aerospace**, **lachy_groom → Deel / Zepto / Anduril**, **naval_ravikant → Perplexity / OpenSea**,
  **immad_akhund → Ramp / Vanta**, **bill_gurley → Glassdoor / HackerOne**,
  **martin_casado → Thinking Machines**: Tier-3 database or unopened-profile attribution only.

Every rejection whose URL I saw only as a search-result extract rather than a full page open says
so explicitly in `reason_rejected`.

## Deliberate typing decisions an auditor should check

- **Elad Gil → CONTROLLED_FUND_INVESTMENT, not personal angel.** eladgil.com frames the entire list
  under "I run Gil&Co a multi-stage investment firm. Past investments include:". Several positions
  (Airbnb, Coinbase, Stripe, Square, Pinterest, Instacart) plainly predate that firm and were almost
  certainly personal cheques, so this deliberately under-weights him. Flagged HIGH in `queue.jsonl`.
- **Martin Casado and Ben Horowitz → BOARD_ONLY.** Their a16z pages say only "serves on the board".
  Marc Andreessen's page, by contrast, says "serves on the board of the following **Andreessen
  Horowitz portfolio companies**", which is why his 11 are CONTROLLED_FUND_INVESTMENT (he co-founded
  and controls a16z) while Casado's 25 are not.
- **Fred Wilson and Albert Wenger carry identical USV edges.** usv.com/companies gives no
  per-partner attribution, so the two nodes look far more correlated than they really are. Flagged
  HIGH — the fix is to read the bylines on USV's individual "Read the Post" announcements.
- **Paul Graham and Jessica Livingston → CONTROLLED_FUND_INVESTMENT via Y Combinator** for Airbnb,
  Dropbox, Stripe and Reddit: they co-founded YC and ran it when those were funded. Not personal.
- **Partovi brothers.** partovi.org annotates which entries were joint, which only Hadi made after
  Ali started Neo, and which only Ali made (Panna) — unusually honest provenance, and I preserved
  the distinction rather than duplicating everything.

## Correlations (88 records, 51 distinct people)

SAME_FOUNDER_ECOSYSTEM 26 · SAME_FIRM 20 · SAME_FORMER_EMPLOYER 18 · FREQUENT_CO_INVESTMENT 16 ·
CO_FOUNDED_COMPANY 3 · SAME_BOARD 2 · FAMILY_RELATIONSHIP 1 · SAME_SYNDICATE 1 ·
SAME_INSTITUTIONAL_SOURCE 1.

The ones that most damage an independence assumption:

- **ali_partovi ↔ hadi_partovi — identical twins (0.95) who publish a single joint investments page
  (0.90).** Roughly sixty of their positions are literally the same cheque; treating them as two
  independent signals would double-count ~60 companies.
- **fred_wilson ↔ albert_wenger — SAME_FIRM (0.90)**, and in this batch their edge sets are
  identical by construction.
- **elad_gil ↔ sarah_guo — SAME_INSTITUTIONAL_SOURCE (0.60):** they co-run the *No Priors* podcast
  (his site claims it; Conviction's site lists it as a Conviction project). Their early AI deal flow
  shares an interview pipeline, and their portfolios overlap on Cognition, Harvey and Mistral.
- **Sequoia bloc** (doug_leone, alfred_lin, shaun_maguire, roelof_botha, michael_moritz) and the
  **a16z bloc** (marc_andreessen, ben_horowitz, chris_dixon, martin_casado, plus balaji_srinivasan
  as alumnus) — 20 SAME_FIRM links in total.
- **shaun_maguire ↔ elon_musk — SAME_FOUNDER_ECOSYSTEM (0.70):** five of the ~40 companies on his
  Sequoia page are Musk entities (SpaceX, The Boring Company, Neuralink, X, xAI). His "independent"
  frontier signal is heavily one-founder-weighted.
- **ron_conway ↔ sam_altman (0.65):** SV Angel's own homepage publishes Altman saying OpenAI "would
  have fallen apart without his help".
- 16 FREQUENT_CO_INVESTMENT records are **derived from this batch's own edges** and are labelled as
  such — they aggregate sourced edges and are explicitly *not* independent evidence.

Reach beyond the 40: correlations touch 51 people, including sam_altman, greg_brockman,
ilya_sutskever, dario_amodei, daniela_amodei, jared_kaplan, elon_musk, brian_armstrong,
brian_chesky, jack_dorsey, peter_thiel, joe_lonsdale, alex_karp, stephen_cohen, david_velez,
sebastian_thrun, melanie_perkins, arthur_mensch, scott_wu, ken_griffin and guillermo_rauch.

**Not yet written, for lack of a source I opened:** the Stripe-alumni cluster (lachy_groom ↔ the
Collison brothers ↔ greg_brockman), reid_hoffman ↔ mustafa_suleyman via Inflection, and
chase_coleman ↔ lee_fixel via Tiger Global. All three are in `queue.jsonl`.

## Valuations

Only **one** valuation record: Snowflake at $81bn public market cap (2021-01, MEDIUM), from CNBC's
prose. This workstream's sources — investor portfolio pages and personal investment lists — almost
never state valuations, and I did not manufacture any. Most of the 827 companies will land in
`TIER_U_UNKNOWN`, which the contract treats as a legitimate outcome rather than a failure.

## Small / obscure companies attracting multiple elite backers

From this batch's confirmed edges, excluding pairs that are not independent (the Partovi twins, the
two USV partners, the two YC co-founders):

**Three or more distinct backers, still early:**
- **Kalshi** — Alfred Lin (Sequoia, early 2020) + Neo + SV Angel.
- **Astranis** — Felicis + Martin Casado (a16z board) + SV Angel.
- **Cognition** — Elad Gil + Conviction + Neo.

**Two independent elite backers, genuinely obscure:**
- **Corridor** (Jack Cable, Ashwin Ramaswami) — on **both** Conviction's and Felicis' own portfolio
  pages. Seed-stage security/AI; the strongest small-company signal in this batch.
- **Distributed Spectrum** (Alex Wulff, Isaac Struhl, Ben Harpe) — again **both** Conviction and
  Felicis. RF sensing / defence, seed stage.
- **Mithril** (Jared Quincy Davis; compute orchestration for AI) — Conviction + Shaun Maguire.
- **Bunkerhill Health** (Nishith Khandwala, David Eng) — Sequoia pre-seed 2023 (Alfred Lin) + Felicis.
- **Braintrust** (AI evals) — Elad Gil says he incubated it; Martin Casado sits on its board.
- **Browser Use** (Magnus Müller, Gregor Žunič) — Felicis + SV Angel.
- **Applied Compute** and **Chai Discovery** — Neo + SV Angel each.
- **Armada**, **Mercor** — Felicis + SV Angel.
- **Periodic Labs** — Seven Seven Six + SV Angel.
- **Living Carbon** — Floodgate + Seven Seven Six.
- **Factory** and **Watershed** — SV Angel + Shaun Maguire.
- **Physical Intelligence** — Alfred Lin + Lachy Groom as a named founder.
- **Rowspace** (Michael Manapat, Yibo Ling) — Sequoia pre-seed 2025 + on Conviction's tracked list.

**Single-backer names worth watching**, because of *who* the backer is and how early the stage is:
Sequoia/Maguire's **Reflect Orbital** ("sells sunlight at night"), **Valar Atomics** (also named by
Balaji Srinivasan personally), **Kela**, **Neros**, **Irregular**, **Corma**, **Engram**, **Glow**,
**Sable AI**, **Skyramp**, **WireScreen**; Sequoia/Lin's **Ineffable Intelligence** (David Silver,
seed 2026), **Firetiger**, **Finch**, **Crosby**, **Abby Care**, **Otter**; USV's **Humane
Genomics**, **Pluralis**, **Efficient Computer**, **Isembard**, **Electroflow**, **Tutor
Intelligence**; 776's **Interlune**, **Starcloud**, **Lodestar Space**, **Monumental Labs**,
**Nucleus Genomics**, **Area 2 Farms**, **LambdaVision**; SV Angel's **Netic**, **Iru**, **Matx**,
**Traversal**, **Mind Robotics**, **General Matter**, **Cellanome**; Thrive's **Atum Works**,
**Alsym Energy**, **Ambrook**, **Cadence Solutions**; Floodgate's **Mentava**, **Terradot**,
**Merlin Labs**, **Last Energy**; and, from the personal-angel lists, Immad Akhund's **SelfyCart**,
**OkPanda**, **SwayFinance**, **Seneca Systems**, **OneChronos**, **Varden Labs** and **Aptonomy**,
plus the Partovis' **entree.ai**, **Medicoder**, **Phononx**, **GitStart** and **Zentail**.

## Next steps, in priority order

1. SEC EDGAR full-text + Form D for **Addition**, **Lachy Groom Fund**, **Thrive Capital** and
   **SV Angel** — the four largest reconstruction gaps.
2. 13F-HR for **Altimeter**, **Coatue** and **Tiger Global** (brad_gerstner, philippe_laffont,
   chase_coleman).
3. Re-render the lazy-loading portfolio pages (`jobs.thrivecap.com/companies`, `neo.com/portfolio`,
   `greylock.com/portfolio` filtered to Sarah Guo) with a JS-capable fetch.
4. Read the bylines on USV's per-company "Read the Post" announcements to split fred_wilson from
   albert_wenger.
5. Upgrade the Elad Gil block from CONTROLLED_FUND to PERSONAL_ANGEL wherever an S-1
   principal-stockholder table or a round announcement names him individually.
6. Crankstart Form 990s for michael_moritz.
