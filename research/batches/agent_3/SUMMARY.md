# Agent 3 — Biotech / Life Sciences — Collection Summary

**Collected by:** `agent_3` · **Date:** 2026-09-16
**Validator:** `python3 scripts/validate_batch.py research/batches/agent_3` → OK

## Totals

| file | records |
|---|---|
| `edges.jsonl` | 502 |
| `companies.jsonl` | 36 |
| `valuations.jsonl` | 10 |
| `correlations.jsonl` | 26 |
| `rejected.jsonl` | 10 |
| `queue.jsonl` | 8 |
| `people.jsonl` | 0 — all 26 assignees were already in `people_universe.yaml`; no new people added |

**Distinct companies:** 445. **Companies touched by ≥2 of my 26 people:** 50.

### Edges by verification status
| status | count |
|---|---|
| `CONFIRMED_PRIMARY` | 465 |
| `CONFIRMED_MULTI_SOURCE` | 16 |
| `PROBABLE_BUT_NOT_CONFIRMED` | 21 |
| `CONFIRMED_REPUTABLE_SECONDARY` | 0 |

481 of 502 edges are confirmed. No edge carries a `CONFIRMED_*` status without a source I opened
and read. The 21 probable rows are all Patrick Hsu's own "I invest in and advise" list, where his
page does not separate investing from advising company by company.

### Edges by relationship type
| type | count |
|---|---|
| `CONTROLLED_FUND_INVESTMENT` | 246 |
| `FOUNDER_EQUITY` | 104 |
| `BOARD_ONLY` | 45 |
| `VC_FUND_PARTNER_INVESTMENT` | 40 |
| `ADVISOR_ONLY` | 40 |
| `PERSONAL_ANGEL_INVESTMENT` | 19 (all PROBABLE) |
| `OTHER_VERIFIED` | 4 |
| `FAMILY_OFFICE_INVESTMENT` | 3 |
| `PERSONAL_EQUITY_INVESTMENT` | 1 |

**Read the fund edges correctly.** The 246 `CONTROLLED_FUND_INVESTMENT` rows are fund-level, not
personal: ARCH Venture Partners' portfolio page (125 rows → Bob Nelsen, ARCH co-founder), Flagship
Pioneering's companies page (34 → Noubar Afeyan, Flagship founder/CEO), and Q2-2026 Form 13F-HR
holdings for EcoR1 (31 → Oleg Nodelman), RA Capital (25 → Peter Kolchinsky) and Casdin Capital
(25 → Eli Casdin), plus a handful of named-in-filing positions. Arie Belldegrun's Vida Ventures
portfolio (30 rows) is deliberately the weaker `VC_FUND_PARTNER_INVESTMENT` — see "could not
reconstruct" below.

### Edges per person
bob_nelsen 130 · george_church 85 · arie_belldegrun 42 · noubar_afeyan 35 · oleg_nodelman 32 ·
eli_casdin 28 · patrick_hsu 27 · peter_kolchinsky 25 · kristina_burow 19 · david_liu 11 ·
jorge_conde 11 · bob_langer 10 · feng_zhang 7 · jennifer_doudna 5 · eric_lander 5 ·
john_maraganore 5 · rick_klausner 4 · carl_june 4 · krishna_yeshwant 4 · daphne_koller 3 ·
alex_zhavoronkov 3 · vijay_pande 3 · stephane_bancel 1 · hal_barron 1 · jeff_huber 1 ·
silvana_konermann 1

All 26 assigned people are covered.

## Where the evidence came from

1. **SEC filings (Tier 1, the backbone of this batch).** EDGAR full-text search
   (`https://efts.sec.gov/LATEST/search-index?q="<name>"&forms=S-1`, which needs gzip and a real
   User-Agent) plus `data.sec.gov/submissions/CIK…json` made it possible to go name-by-name
   through S-1s, 13F-HRs, Form Ds and 10-K covers. Founder language in a company's own
   registration statement is the most reliable evidence in this domain. Highlights:
   - Editas S-1/A names Zhang, Church, Liu, Joung as founders and Doudna as a founder who had left.
   - Beam S-1/A: "founded in 2017 by David Liu, Feng Zhang and Keith Joung."
   - Caribou S-1: Doudna a co-founder holding **6.28% pre-IPO** via the James and Jennifer Doudna
     Cate Living Trust — the single cleanest ownership number in the batch.
   - Kite Pharma S-1/A cover page gives Belldegrun's title as "President, CEO, Chairman, Founder".
   - Kronos Bio S-1/A: founded by Belldegrun + Two River, and he "also founded Agensys … and
     Cougar Biotechnology".
   - Moderna S-1: Afeyan and Langer named co-founders, and footnote 3 discloses that Bancel's
     **OCHA LLC and Boston Biotech Ventures bought Series A–G preferred for ~$3.9m, ≈4.6% of
     pre-IPO as-converted common**.
   - Lyell S-1 (Klausner founder, "co-founder of Juno and GRAIL"), GRAIL S-1 (Huber "one of our
     founders" and founding CEO), Nurix S-1 (Carl June leading the DeCART founding team),
     Codiak S-1/A (Lander co-founded Infinity Discovery in 2001), EQRx S-1 (Casdin, Conde and
     Yeshwant on one board; Casdin CEO of CM Life Sciences III), Beam S-1/A again for Kristina
     Burow's Receptos and Sapphire Energy co-foundings and her 13 directorships.
2. **Scientists' own pages.** George Church's tech-transfer page is unique: he maintains it, states
   that the first date on each line is the founding year, and marks companies he founded with "F".
   That produced 46 founder edges and 38 clearly separated advisory edges from one source, with
   dates suppressed wherever his involvement window does not start in the founding year. David
   Liu's lab page carries an explicit conflict-of-interest disclosure ("He owns founders' equity in
   these companies"). Patrick Hsu's personal site named Stylus Medicine and Terrain Biosciences as
   co-foundings and listed his personal startup involvements.
3. **Company launch releases** for the private names that matter most: Stylus Medicine, Aera,
   Moonwalk, Capstan, Tmunity, Verismo, Scribe, Mammoth, Sherlock, Pairwise, Altos Labs, Prime
   Medicine, Arc Institute, Deep Longevity.
4. **A non-SEC regulatory filing:** Regent Pacific's HKEX announcement of the Deep Longevity
   acquisition, which puts Alex Zhavoronkov above 5% of InSilico Medicine Cayman TopCo and at
   ~3.35% of the enlarged Regent Pacific — the only hard ownership figures available for him.
5. **Valuations** are all sourced: nine are the "aggregate market value of common equity held by
   non-affiliates" stated on fiscal-2025 Form 10-K covers, measured at the 2025-06-30 close (a
   floor for market cap, flagged as such and recorded at MEDIUM confidence); the tenth is Deep
   Longevity's ~US$3.79m acquisition price from the acquirer's own announcement.

## Most interesting small / obscure companies with multiple elite backers

| company | who is on it | why it stands out |
|---|---|---|
| **Parabilis Medicines** | ARCH (Nelsen) + RA Capital ($791.9m / 28.9m shares) + Casdin ($17.7m) | RA Capital's second-largest disclosed position after Ascendis; the only name where three separate elite pools converge |
| **Aera Therapeutics** | Feng Zhang (founder) + ARCH + GV + Lux; Maraganore board chair, Nelsen on board | $193m Series A+B, still private, protein-nanoparticle delivery |
| **Arbor Biotechnologies** | Feng Zhang (founder, named on the Form D as a director) + ARCH + Patrick Hsu (personal, probable) | founder + angel + fund stack on a private gene-editing company |
| **Moonwalk Biosciences** | Feng Zhang (scientific co-founder) + ARCH + GV + Khosla + Alpha Wave | only $57m raised — genuinely early, epigenetic editing |
| **Stylus Medicine** | Patrick Hsu (scientific founder) + RA Capital and Khosla as *founding* investors | $85m, out of stealth May 2025; RA's Joshua Resnick sits on the board with Hsu |
| **Capstan Therapeutics** | Carl June (founder with disclosed equity) + Vida Ventures (Belldegrun) + RA Capital + five pharma venture arms | Penn's in-vivo CAR-T spinout; the Penn disclosure states June owns equity outright |
| **Aktis Oncology** | Vida Ventures (Belldegrun) + EcoR1 ($155.5m) | targeted radiopharmaceuticals; EcoR1's third-largest position |
| **Hemab Therapeutics** | John Maraganore (board chair) + RA Capital ($286.8m) | Maraganore's post-Alnylam vehicle of choice |
| **Qihan Biotech** | George Church (founder) + ARCH | Hangzhou pig-genome engineering, almost invisible in Western coverage |
| **nChroma Bio** (ex-Chroma Medicine) | David Liu (founder equity) + ARCH | epigenetic editing |
| **Neurogene** | Casdin ($48.6m) + EcoR1 ($40.0m) | two specialist funds in the same micro-cap |
| **Sionna Therapeutics · Septerna · Taysha Gene Therapies** | Casdin + RA Capital | a repeated Casdin/RA pairing across small caps |
| **Tessera Therapeutics** | Flagship (Afeyan) + George Church (advisory) | gene writing |
| **Terrain Biosciences, Eugit Therapeutics, JuraBio, Tenza, Regula Bio, Connectomes Inc., AdoraPet BioSciences, Breaking (Samri), Cache DNA, Cellgorithmics** | one elite founder each | Church- and Hsu-founded companies with essentially no public footprint — the sparsest, highest-novelty names in the batch |

## Whose portfolios could NOT be reconstructed, and why

- **Hal Barron (1 edge).** Documented only as an Altos Labs board director and incoming CEO. No
  filing or release I opened discloses any personal or fund investment by him. His signal is
  positional — where he chooses to work — not transactional. Queued.
- **Stephane Bancel (1 edge).** His single edge is high quality (the OCHA LLC Series A–G purchase),
  but OCHA's other holdings appear in no SEC filing and his non-Moderna activity is invisible from
  US primary sources. Queued.
- **Jeff Huber (1 edge).** GRAIL founder/founding CEO is solid; his post-GRAIL venture activity is
  not visible in any filing or release I opened. Queued.
- **Silvana Konermann (1 edge).** She genuinely has no company portfolio: her one verified
  relationship is co-founding the Arc Institute, a non-profit with no equity (recorded as
  `OTHER_VERIFIED`, not `FOUNDER_EQUITY`). A documented absence, not a gap — she is an
  institution-builder, not an investor.
- **Vijay Pande (3 edges).** a16z board seats attributed to him (Apeel, BioAge, Devoted Health,
  Freenome, insitro, Nautilus, Omada, Q.bio, Slingshot AI) appear only on Wikipedia and
  data-aggregator profiles; only Scribe is confirmed by a company release. Logged in
  `rejected.jsonl` rather than smuggled in.
- **Rick Klausner (4 edges).** Juno, GRAIL, Lyell and Altos are solid; Mindstrong and other
  attributed co-foundings had no primary source. Queued.
- **Krishna Yeshwant and Jorge Conde.** Everything verified is board-level. GV's and a16z's
  portfolios are the firms' capital and neither man controls his firm, so nothing was upgraded
  beyond `BOARD_ONLY` / `VC_FUND_PARTNER_INVESTMENT`.
- **Alex Zhavoronkov (3 edges).** Insilico is private and Cayman-domiciled; the only ownership
  figures anywhere came from a Hong Kong acquirer's announcement.
- **Eric Lander.** Deliberately *shrunk*. The Broad Institute's own biography says he was a
  "founding scientific advisor" of Millennium and Foundation Medicine, not a founder — both are
  `ADVISOR_ONLY` with matching `rejected.jsonl` rows.
- **Arie Belldegrun's Vida Ventures exposure** is the largest single unresolved question: 30 edges
  hang on whether he founded/controls Vida (weight 0.70) or is merely its Senior Managing Director
  (weight 0.35). Every SEC filing I opened says only the latter.

## Claims chased and killed (`rejected.jsonl`, 10 rows)

1. Bancel as a Moderna co-founder — the S-1 consistently calls him founding *CEO* and names
   Afeyan, Rossi, Langer and Chien as co-founders.
2. Langer as a founder of Lyra Therapeutics — Lyra's S-1 makes him a director since 2006 only.
3. & 4. Lander as founder of Millennium Pharmaceuticals and of Foundation Medicine — founding
   scientific *advisor* per Broad's own bio.
5. Doudna as an Intellia founder — Editas' S-1 calls her a publicly-identified *advisor* to
   Intellia; Caribou's S-1 credits Rachel Haurwitz as the Intellia co-founder.
6. Church as a 23andMe founder — his own page lists 23andMe without the "F" marker.
7. Carl June as a Cabaletta Bio founder — no primary source found.
8. Conde as a Syros founder — he was Chief Strategy/Financial/Product Officer, an employment role.
9. Belldegrun's Vida portfolio as *controlled*-fund exposure — downgraded, not deleted.
10. Pande's a16z board seats beyond Scribe — aggregator-only.

## Paywalled / blocked sources

- **Boston Business Journal, Business Insider, Boston Globe, Endpoints News and BioCentury**
  returned subscriber walls or partial text. Where a fact mattered I re-sourced it from the
  company's own release rather than bypassing the wall — this is why Aera, Moonwalk, Stylus and
  Capstan are cited to Business Wire / company sites rather than to the trade press that broke them.
- **`vidaventures.com/team` and `/about-us` returned 404**, and `bellco.com` failed to fetch. This
  is the single most consequential gap in the batch.
- **`archventure.com/portfolio` is JavaScript-rendered** and returned 0 bytes to `curl`; recovered
  with a rendering fetch.
- **`sherlock.bio` now redirects to OraSure**, so Sherlock's founder list was taken from GenomeWeb
  plus a verbatim reprint of the Business Wire launch release (two Tier-2 sources → MULTI_SOURCE).
- **LinkedIn and financial-data aggregators (Zonebourse, Equilar, Altss, startupintros,
  marketscreener)** surfaced repeatedly for exactly the facts I most wanted — Bellco's principals,
  Pande's board seats, Hsu's Monet AI. None of it was used as evidence.

## Next steps (highest value first)

1. **Resolve Vida Ventures and Bellco Capital** via SEC Form ADV / IAPD and Vida's own Form Ds.
   This one question re-weights 32 Belldegrun edges.
2. **Split Patrick Hsu's "invest in and advise" list** (19 PROBABLE rows) using Form D
   related-person tables and funding releases. He is the most active individual angel among the 26
   and the list contains several pre-seed AI-for-bio names.
3. **Pull Form Ds for the private founder companies** — Stylus, Aera, Moonwalk, Terrain, Eugit,
   JuraBio, Tenza, Regula Bio, Connectomes — to upgrade founder edges and surface co-investors that
   never appear in a press release.
4. **Historic SC 13D/13G filings** for EcoR1, RA Capital and Casdin would add dated entry points;
   this batch used only the latest 13F, so `investment_date` is null on all 81 of those rows
   (a 13F states the holding at the report date, never when the position was opened).
5. **Sweep the remaining ~90 non-"F" companies on Church's page** if full advisory coverage is
   wanted; I took a 38-company subset weighted toward the small and obscure.
