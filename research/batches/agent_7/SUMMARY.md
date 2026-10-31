# agent_7 — verification, valuation and deduplication

Collected 2026-09-16. `python3 scripts/validate_batch.py research/batches/agent_7` → **OK**.

| file | records |
|---|---|
| `valuations.jsonl` | 122 |
| `companies.jsonl` | 121 |
| `queue.jsonl` | 3 |
| `edges.jsonl` / `rejected.jsonl` / `people.jsonl` / `correlations.jsonl` | 0 (not my workstream) |

---

## TASK 1 — Valuations

**122 sourced valuations for 122 distinct companies**, every one with a date and at least one
source I opened and read. No record is a snippet-only claim.

### How far down the target list I reached

| | resolved |
|---|---|
| top 25 | 21 / 25 |
| top 50 | **39 / 50** |
| top 75 | 49 / 75 |
| top 100 | 52 / 100 |
| top 150 | **60 / 150** |
| top 200 | 68 / 200 |
| whole list | **85 / 386** |

**I did not hit the "top 150" goal — I resolved 60 of the top 150 (and 85 across the whole
list).** The honest reason is composition, not effort: below roughly rank 80 the list stops being
companies-with-undisclosed-valuations and becomes two long tails that are *structurally*
unvaluable —

* **ranks 81–136**: the Ali/Hadi Partovi angel book, mostly 2000s-era private companies that were
  acquired or died long before a valuation was ever published (Snapvine, Thinkfuse, XL2Web, Opzi,
  BuyerWeb, Vamo, Edusoft, JamLegend, OpenHarbor…). Several are resolvable with acquisition
  prices and would be high-value for the failure analysis — see "what I would do next".
* **ranks 190–270 and 340–386**: the Lowercarbon (Sacca) and USV (Wenger/Wilson) seed books —
  ~130 seed-stage climate and crypto companies that have never disclosed a priced round. These
  legitimately stay in `TIER_U_UNKNOWN`.

The 85 I did resolve are concentrated where they change the answer: **21 of the top 25**.

### Composition of what was recorded

* by type: 46 primary-round post-money · 35 public market cap · 21 shut-down-zero · 11 acquisition
  price · 5 tender/secondary · 4 reported valuation
* by confidence: 75 HIGH · 45 MEDIUM · 2 LOW
* by tier: 74 TIER_D (>=$5B) · 15 TIER_C · 2 TIER_B · **31 TIER_A (<$500M)**

The 31 TIER_A entries are the analytically important ones: 21 are zeros from the failure set.
Before this batch the graph had 6 valuations and no failures at all, so every discriminating
observation in the backtest comes from here.

### Two structural findings that change the graph

1. **SpaceX is now a public company.** It IPO'd on Nasdaq as `SPCX` on 2026-06-12 at $135/share
   ($1.77T), closed day one near $2.1T, and trades at **$2.06T** as of 2026-09-16. Target #3 is
   no longer a private company and every SpaceX edge now has a live mark-to-market.
2. **Cursor (Anysphere) was acquired by SpaceX for $60B**, agreed 2026-06-16 and recorded as
   closed in Q3 2026 — the largest venture-backed startup acquisition on record. Target #66 is
   `ACQUIRED`, not `OPERATING_PRIVATE`. Relatedly, **xAI has been merged into SpaceX** (per CNBC's
   coverage of the Cursor deal), which is why target #336 has no standalone valuation and why
   `stockanalysis.com/private/xai` 404s.

### Method notes (so this is reproducible and checkable)

* **Public companies**: live quote pages on `stockanalysis.com`, opened individually with a
  fetcher, price and market cap read on 2026-09-16 between 10:10 and 10:40 EDT. Recorded under the
  new `market_data_provider` source type.
  **Warning for whoever re-runs this**: cached/aggregated copies of these same pages were
  materially stale — the cached Coinbase page showed $50.39B against a live $44.46B (a 13% error),
  and Pinterest and Palantir were similarly off. Fetch live, do not re-use an extract cache.
* **Private companies**: primary announcement first (company press release or SEC/regulatory
  filing), major wire second. Where no announcement exists I used
  `stockanalysis.com/private/<slug>` — a market-data aggregator that states its private marks come
  from *completed* funding rounds in the last three years. Those records are all marked **MEDIUM**
  and say so in `notes`. I spot-validated the aggregator against figures I had confirmed
  independently (Anthropic $965B, OpenAI $852B, Stripe $159B, Anduril $61B, Ramp $44B, Scale $29B)
  and it matched on all six.
* **Stale marks are recorded with their true date, never refreshed.** Flexport ($8B, Feb 2022),
  Thumbtack ($3.2B, Jun 2021), Rappi ($5.25B, Jul 2021), Ro ($7B, Feb 2022), Solugen ($2.05B, Oct
  2022) and Magic Leap ($450M, Jun 2020) are all almost certainly wrong today. They are in with
  their real dates so the staleness bands flag them rather than hiding it.

### Conflicts I preserved rather than resolved

* **Perplexity** — Reuters (2026-08-23, reporting The Information) describes the last *completed*
  financing as $20B "about a year ago" and the $30B+ Nvidia round as only in talks. Several
  lower-quality outlets assert a closed $23B Series E-6 on 2026-01-09; no Tier-1/Tier-2 source
  supports it and Reuters' framing implicitly contradicts it. **Recorded $20B / 2025-09 / MEDIUM.**
* **Google DeepMind** — Guardian and FT both say £400m (~$650–660m); Re/code (carried by Reuters
  and the BBC) says $400m; Google never confirmed. **Recorded $650M / MEDIUM** with the conflict in
  `notes`.
* **Casper** — Business Insider computes ~$286M equity value at $6.90/share, AP says ~$308M.
  **Recorded $286M / MEDIUM** with both figures noted.

### Vocabulary gap I hit (now closed)

Public market caps had no honest home in `SOURCE_TYPES`. A `market_data_provider` type
(TIER_2_SECONDARY) appeared in `enums.py` while I was working and I used it for all 35 market-cap
records and the two OTC bankruptcy shells. Flagging it so nobody thinks those were press citations.

---

## TASK 2 — Backtest cohort outcomes

**47 of the 51 cohort companies now carry a sourced outcome valuation and a `current_status`.**
I worked failures and mediocre outcomes first, as instructed: **all 24 FAILURE and all 12 MEDIOCRE
entries are sourced**, plus 11 of the 15 winners.

21 of the failures are recorded as `shut_down_zero` with the bankruptcy/wind-down date and either
a court/regulatory filing or two independent wire reports. The rest are acquisition prices that
quantify the loss: Zymergen $300M (vs ~$3B IPO), Blue Apron $103M (vs ~$1.9B IPO), Pebble $23M,
Lordstown's EV business $10.2M, Casper $286M, Inflection AI ~$650M (vs ~$4B).

### Labels I believe are wrong

1. **`Bloom Energy` is labelled MEDIOCRE — "long public life far below first-wave cleantech
   expectations". That is no longer true and it is the single most consequential mis-label in the
   file.** Bloom Energy's market capitalisation on 2026-09-16 is **$79.93B** at $271.40/share.
   It IPO'd in 2018 around $1.6B. On any definition in the cohort's own key ("WINNER = >= ~$10B or
   transformative") Bloom is a **WINNER**, and by a wide margin. Leaving it in the negative-control
   set does not merely mislabel one row — it puts a ~50x outcome into the control group and will
   bias the backtest *against* finding signal. **This should be changed to WINNER before the
   backtest is run.**
2. **`Bird` is labelled MEDIOCRE. It should be FAILURE.** Bird Global filed Chapter 11 on
   2023-12-20 and its assets were sold to a lender-owned vehicle (Third Lane Mobility) in April
   2024; the listed equity did not survive. That is the same outcome class as the entries already
   labelled FAILURE, not a "disappointing but alive" outcome.
3. **`Quibi`'s FAILURE label is right but the note is imprecise.** Quibi wound down with cash on
   the balance sheet and *returned the remainder to shareholders* under its operating agreement.
   Enterprise value went to zero, but investor recovery was partial, not nil. If the backtest
   computes investor multiples rather than enterprise outcomes, Quibi needs a non-zero recovery
   assumption or it will overstate the loss.
4. **`Lordstown Motors` — the FAILURE label is right for the business but the mechanics are
   unusual and will break a naive "equity cancelled" rule.** Under the confirmed plan, Class A
   common and preferred **remained outstanding** and the shell continued as Nu Ride Inc. holding
   cash, NOLs and the Foxconn litigation. Only the EV business was sold, for $10.2M. My record
   captures this in `notes`.
5. **`Character.AI`'s MEDIOCRE label is defensible but sits oddly next to Inflection and Adept.**
   Google paid $2.7B (WSJ) — more than four times Microsoft's Inflection consideration and more
   than twice Adept's last valuation. If "MEDIOCRE" is meant to mean "non-outlier", a $2.7B
   realisation on a ~$1B company is a *good* outcome for the 2023 investors. Worth deciding
   explicitly rather than letting all three acqui-hires sit in one bucket.

### Cohort entries I could not value

* **Commonwealth Fusion Systems (STRONG)** — genuinely unvaluable. CFS has never disclosed a
  valuation; the $1B July 2026 round and the $863M 2025 round were both announced without one and
  CEO Bob Mumgaard explicitly declined to give one to the Boston Globe. The aggregator shows the
  round with valuation `n/a`. Correctly `TIER_U_UNKNOWN`. Queued.
* **Stability AI (MEDIOCRE)** — the June 2024 rescue recapitalisation was announced without a
  valuation and the company declined to comment when Reuters reported it might be a down round.
  WSJ put the new money at ~$80M with ~$100M of supplier debt forgiven and $300M of future
  obligations released. The label is well supported by the facts; the number is not recoverable
  from public sources. Queued. `current_status` recorded.
* **Palantir** and **DeepMind** are valued, but filed under the target-list spellings
  **"Palantir Technologies"** ($410.59B market cap) and **"Google DeepMind"** ($650M acquisition).
  These need aliasing — see dedup findings.

---

## TASK 3a — Deduplication audit

I did **not** edit the database. Findings for `data/company_aliases.yaml`.

### Confirmed MISSED MERGES (one company split across several ids) — apply these

| ids | why | impact |
|---|---|---|
| `c_boring` ("Boring Company") + `c_the_boring` ("The Boring Company") | Same company. Disjoint backer sets: Jurvetson, Saenko, Thiel, Stephens on one; Lonsdale, Musk, Maguire, Li Ka-shing on the other. | **Highest-impact item found.** The target list carries it twice (#30 with 4 backers and #69 with 3). Merged it has **8 confirmed backers**, which would move it near the top of the whole ranking. The split is silently halving the headline metric for one of the most-backed companies in the graph. |
| `c_zillow` ("Zillow Group") + `c_zillow_com` ("Zillow.com") | Same company, and **the same person (`bill_gurley`) is on both**, so this is double-counting one investor. | Inflates edge counts, corrupts T08's no-double-counting guarantee. |
| `c_radiant` ("Radiant") + `c_radiant_industries` ("Radiant Industries"/"Radiant Nuclear") | `c_radiant_industries` already absorbs the bare alias "Radiant"; `c_radiant` (rachel_slaybaugh, a nuclear-energy investor) is almost certainly the same nuclear microreactor company. | 1 backer stranded. |
| `c_decart` ("Decart", shaun_maguire) + `c_decart_ai` ("Decart.ai", oren_zeev) | Decart is a single Israeli AI-video company backed by both Sequoia and Oren Zeev. | 2-backer company recorded as two 1-backer companies — drops out of the >=2-backer target list entirely. |
| `c_medra` ("Medra", alexis_ohanian) + `c_medra_ai` ("Medra AI", patrick_hsu) | Same bio-robotics company. | Same as above — a >=2-backer company made invisible. |
| `c_olive` ("Olive", keith_rabois) + `c_olive_ai` ("Olive AI", 0 edges) | `c_olive_ai` is an edge-less stub created by the cohort file; `c_olive` carries the edge. Needs a decision, then one id. | Cohort row will not resolve to the edge-bearing company. |

Note the pattern in rows 4–5: **the `X` / `X.ai` / `X AI` split is systematically hiding
two-backer companies from the ranking**, because each half falls below the >=2 threshold. There are
8 such normalised-name collisions in the `companies` table; I judged 4 of the 8 to be real splits.

### Probable WRONG MERGE (two different companies collapsed into one) — please check

* **`c_brilliant`** merges raw names **"Brilliant Labs"** and **"Brilliant"** (backers
  `eric_migicovsky`, `jason_calacanis`). These are very likely two different companies — Brilliant
  Labs (open-source AR glasses) and Brilliant (smart-home lighting control). This is the one merge
  in the sample I would actively unwind.

### Merges that are technically correct but analytically harmful

* **`c_x_formerly_twitter`** merges **"Twitter"** and **"X (formerly Twitter)"**. Legally one
  entity lineage, so the merge is defensible — but it destroys the ability to distinguish a
  2007-era Twitter angel position (outcome: acquired at $44B in 2022) from a 2025-era X/xAI
  position. **For a backtest that measures entry → outcome multiples this is a real problem**: the
  same company id now spans two completely different economic events. Consider a `former_names`
  split with distinct valuation epochs rather than one id.
* **`c_impulse_space`** correctly merges "Impulse Space" and the bare "Impulse" from Founders
  Fund's portfolio page — but note the target list carries both (#154 and #292) as separate rows,
  so the same de-duplication needs applying to the ranking inputs, not just the graph.

### Correct splits I verified and would leave alone

`c_arbor`/`c_arbor_biotechnologies`, `c_matter`/`c_matter_neuroscience`, `c_curie`/`c_curie_bio`,
`c_evolv`/`c_evolv_ai`, `c_human`/`c_human_interest`, `c_odyssey`/`c_odyssey_therapeutics`,
`c_essential`/`c_essential_products` (Sarah Guo's "Essential" is not Andy Rubin's dead
Essential Products), and the existing alias merges for Scale, Anduril, Google DeepMind, Anchorage,
Character.AI, eGenesis, Harmonic and Arrived Homes.

### Aliases to add for this batch to resolve

`Palantir` → `Palantir Technologies` · `DeepMind` → `Google DeepMind` ·
`Boring Company` → `The Boring Company` (I filed a record under both target-list spellings so the
ranking resolves either way; they should end up as one company).

### Unresolved in T03

Of the 17 T03 near-miss pairs, several reference ids that no longer exist in `companies`
(`c_impulse`, `c_inflection`, `c_character`, `c_anchorage`, `c_arrived`,
`c_commonwealth_fusion_systems_cfs`, `c_egenesis_bio`, `c_harmonic_ai`) — those are stale warnings
from before the merges landed and can be cleared.

---

## TASK 3b — Edge audit (15 random confirmed edges)

Sample drawn from the 3,206 distinct confirmed edges with `random.seed(20260916)` so it is
reproducible. I opened every cited URL.

**Result: 11 of 15 verify cleanly at the cited URL. 4 do not — none because the underlying claim
is false, all because the cited evidence does not do what the evidence summary says it does.**

### Verified clean (11)

| # | edge | check |
|---|---|---|
| 2 | `nat_friedman` → Vercel, PERSONAL_ANGEL | OK — vercel.com/about has a separate "Individual investors" list; Friedman is the **first name in it**, distinct from the institutional backers. |
| 3 | `guillermo_rauch` → Substrate, PERSONAL_ANGEL | OK — Substrate Labs' own Business Wire release names "Guillermo Rauch (Vercel)" individually among participants in the $8M seed. |
| 5 | `eric_schmidt` → Anthropic, FAMILY_OFFICE | OK — Anthropic's own Series A release names Eric Schmidt among participants in the $124M round, 2021-05-28. Correctly *not* typed as a personal angel cheque. |
| 6 | `vinod_khosla` → Slash, CONTROLLED_FUND | OK — Slash on khoslaventures.com/portfolio ("Business banking for specialized verticals"). |
| 7 | `aydin_senkut` → Astranis, CONTROLLED_FUND | OK — Astranis on felicis.com/portfolio with founders and stage. |
| 8 | `peter_thiel` → Nominal, CONTROLLED_FUND | OK — Nominal listed on foundersfund.com/portfolio. |
| 9 | `vinod_khosla` → Limbic, CONTROLLED_FUND | OK — Limbic on khoslaventures.com/portfolio ("AI therapist"). |
| 10 | `peter_kolchinsky` → Artiva Biotherapeutics, CONTROLLED_FUND | OK — I opened the actual `infotable.xml` in the cited SEC filing: **17,955,642 shares, $174,169,727** — matches the evidence summary to the share. Best-evidenced edge in the sample. |
| 13 | `chris_sacca` → River, CONTROLLED_FUND | OK — River on Lowercarbon's companies page ("India's practical, badass e-moto"). |
| 15 | `chris_sacca` → Minus, CONTROLLED_FUND | OK — Minus on Lowercarbon's companies page ("Coffee minus coffee"). |
| 4 (role half) | `eric_toone` at BEV | OK — Material Impact bio confirms Carmichael Roberts co-leads the BEV investment committee; the VEIR–BEV link verifies independently (see below). |

### Failed the audit (4) — every one, with the reason

**1. `carmichael_roberts` → Albedo (#1), `eric_toone` → VEIR (#4), `bill_gates` → Fleetzero (#12)
— the cited BEV portfolio URL serves no company list to any fetcher.**

`https://www.breakthroughenergy.org/portfolio/index.html` returns only a newsletter signup form.
I fetched it twice with two independent fetchers; both got zero companies. The page is
client-rendered, so the evidence summaries ("BEV's own portfolio page lists X as a portfolio
company") **cannot be verified at the cited URL by anyone, including a future auditor**.

I then verified all three claims independently, and **all three are true**:
* Fleetzero — Fleetzero's own PR Newswire release (2026-01-16) names Breakthrough Energy Ventures
  as an existing investor in its $43M Series A.
* VEIR — VEIR's Business Wire release (2021-03-04) states the Series A was **led by** BEV, and
  quotes Carmichael Roberts of BEV in the release.
* Albedo — BEV co-led Albedo's $48M Series A (Payload, 2022-09-07), and BEV's own published
  portfolio guide PDF profiles Albedo, VEIR and Fleetzero.

**Severity: this is a systemic citation defect, not three isolated ones. That single URL is the
evidence for 309 confirmed edges** (103 `CONTROLLED_FUND_INVESTMENT` + 206
`VC_FUND_PARTNER_INVESTMENT`) — the most-cited URL in the entire graph. The claims are probably
mostly sound, but as it stands ~10% of the confirmed edge base rests on a citation that cannot be
checked. **Recommended fix**: re-source against BEV's portfolio guide PDF
(`https://assets.swoogo.com/uploads/2121112-634862175072a.pdf`, which profiles 87 BEV companies in
plain text) or against per-company funding announcements naming BEV. Note the same risk applies to
the other high-count portfolio-page URLs in the top-cited list —
`lowercarboncapital.com/companies/` (202 edges) now 301-redirects to `lowercarbon.com/companies/`,
so the stored URL is stale even though the content verifies at the new location.

**2. `carl_june` → Verismo Therapeutics (#11) — the evidence summary overstates what the page
says.**

The summary claims the site "lists the founding team as Bryan Kim, Laura A Johnson, Michael C
Milone, Donald Siegel and Carl June." The page does **not** say that. It says "Verismo was founded
by the inventors of Kymriah" and separately lists five people under "The experts behind KIR-CAR
and SynKIR". Inferring `FOUNDER_EQUITY` requires the reader to supply the premise that June is a
Kymriah inventor — true, but not stated on the cited page. **The claim is very likely correct; the
evidence summary asserts more than the source supports and should be softened or re-sourced.**

**3. `xavier_niel` → Vertical Compute (#14) — inconclusive at the cited URL; claim independently
confirmed.**

`kimaventures.com/portfolio` is a single alphabetical page of many hundreds of companies; neither
fetcher returned far enough into the alphabet to reach "Vertical Compute", so the citation is not
practically checkable. **Independently confirmed**: Vertical Compute's own press release
(2026-03-04) names Kima Ventures among the participants in its €57M seed. The edge stands; the
citation should point at the company's release instead of a giant unpaginated list.

**4. `eric_toone` → VEIR (#4) — the CNBC corroborating source 403s.**

`cnbc.com/2022/05/07/what-is-carbon-capture-eric-toone...` returned 403 Forbidden on repeated
attempts. That URL is cited on **103 confirmed edges**. The database's own `url_http_status`
column already shows **651 confirmed-edge sources returning 403**, plus 12 × 404, 6 × 401 and 3 ×
429 — about 15% of confirmed-edge sources are not retrievable by a third party. The 403s are
mostly paywall/bot-blocking rather than dead links, but a reader cannot check them.

### What the audit says overall

No fabricated relationships and no category errors. Every relationship type in the sample was
typed correctly and conservatively — fund holdings as `CONTROLLED_FUND_INVESTMENT`, Roberts' and
Toone's BEV roles as `VC_FUND_PARTNER_INVESTMENT` rather than personal cheques, Schmidt's
Anthropic position as `FAMILY_OFFICE_INVESTMENT`. The anti-hallucination discipline is holding.

**The weakness is citation durability, not truthfulness.** Roughly a fifth of confirmed edges
lean on a handful of JS-rendered portfolio pages and paywalled articles that a later auditor
cannot reproduce. That is a silent decay risk: today the claims are verifiable with extra work,
in two years they may not be.

---

## Companies I could not value, and why

* **No valuation has ever been disclosed** (queued): Commonwealth Fusion Systems (#11 — CEO
  explicitly declined to disclose), Erebor (#15 — too new, no priced round, no aggregator entry),
  Stability AI (recapitalisation announced without a valuation).
* **Not covered by any accessible source**: Chroma (#23), Periodic Labs (#55), Electra (#16),
  Nominal (#39), Heirloom (#28), Living Carbon (#32), Watershed (#35), Noya (#37), Zanskar (#38)
  and the bulk of ranks 190–270 / 340–386. These are seed and Series A climate/crypto companies
  whose rounds are announced without post-money figures. `TIER_U_UNKNOWN` is the correct and
  honest answer for them.
* **Paywalled**: Bloomberg and The Information articles were readable only as page-body extracts,
  never in full; I cited them only where the extract itself contained the figure. The FT Stripe
  piece was headline-only and I used Stripe's own release instead.
* **Merged into a parent, so no standalone mark exists**: xAI (into SpaceX), Google DeepMind
  (into Alphabet — recorded at its 2014 acquisition price instead), Oculus and Zappos (recorded at
  acquisition prices).

---

## What I would do next, in priority order

1. **Re-label Bloom Energy as WINNER before the backtest runs.** A $79.9B company sitting in the
   negative-control set will actively suppress measured signal.
2. **Apply the Boring Company merge.** It is the single largest distortion to the headline
   ranking that I found.
3. **Re-source the 309 BEV-portfolio edges** against the BEV portfolio PDF or per-company
   announcements, and re-point the 202 Lowercarbon edges at the redirected URL.
4. **Work target ranks 81–136 (the Partovi book) for acquisition prices and shutdown dates.**
   These are 1998–2016 exits with public outcomes — IronPort/Cisco, OPOWER/Oracle, Tellme/Microsoft,
   LinkExchange/Microsoft, Nervana/Intel, BlueKai/Oracle, Codecademy/Skillsoft, PracticeFusion,
   DeepScale/Tesla, Planetary Resources, Bigfoot/Abbott. Roughly 40 resolvable rows, and they are
   *old* enough to produce realised multiples rather than paper marks. For a backtest, they are
   worth more per row than another 2026 AI company.
5. **Decide the acqui-hire bucket** (Inflection / Adept / Character.AI) explicitly rather than
   lumping three very different realisations into "MEDIOCRE".
