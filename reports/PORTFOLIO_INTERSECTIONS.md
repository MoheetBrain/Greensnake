# PORTFOLIO INTERSECTIONS — which companies show up in the most elite portfolios?

_1814 companies have at least one tracked person with confirmed economic ownership exposure, out of 190 people tracked._

## The metric

```
PORTFOLIO_INTERSECTION_COUNT =
    distinct tracked people with a CONFIRMED relationship to the company
    representing real economic ownership exposure
```

**Counted** — `PERSONAL_ANGEL_INVESTMENT`, `PERSONAL_EQUITY_INVESTMENT`, `SPV_INVESTMENT`, `FOUNDER_EQUITY` (the *direct* column) and `FAMILY_OFFICE_INVESTMENT`, `CONTROLLED_FUND_INVESTMENT` (the *controlled* column).

**Shown but NOT counted in the ranking** — `VC_FUND_PARTNER_INVESTMENT`, in its own column. A partner at a firm they do not control has exposure to the deal, not necessarily to the company.

**Excluded entirely** — `BOARD_ONLY`, `ADVISOR_ONLY`, `GRANT_FUNDING`, `PHILANTHROPIC_FUNDING`, `LP_INDIRECT`, `DEBT_FINANCING`, `CORPORATE_STRATEGIC_INVESTMENT`, `OTHER_VERIFIED`. None of these is ownership.

**One person counts once per company**, regardless of how many rounds they joined or how many sources confirm it. Only `CONFIRMED_*` edges count; anything uncertain is left out.

The ranking is the **raw count**. Weighted and independence-adjusted scores appear as secondary columns in the CSV and never affect the ordering.

---

# OUTPUT 1 — TOP 30 PORTFOLIO INTERSECTIONS

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Anduril Industries** | **10** | 3 | 7 | 4 | $61.00B | D | DEFENCE | OPERATING_PRIVATE |
| 2 | **Uber** | **9** | 4 | 5 | 3 | $145.14B | D | TRANSPORT_MOBILITY | OPERATING_PUBLIC |
| 3 | **Cognition** | **9** | 3 | 6 | 1 | $48.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 4 | **Perplexity** | **8** | 6 | 2 | 0 | $20.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 5 | **Airbnb** | **8** | 3 | 5 | 2 | $99.75B | D | CONSUMER_INTERNET | OPERATING_PUBLIC |
| 6 | **Commonwealth Fusion Systems** | **8** | 2 | 6 | 2 | — | U | — | UNKNOWN |
| 7 | **SpaceX** | **7** | 3 | 4 | 3 | $2.06T | D | SPACE | OPERATING_PUBLIC |
| 8 | **Stripe** | **7** | 0 | 7 | 3 | $159.00B | D | FINTECH | OPERATING_PRIVATE |
| 9 | **Granola** | **6** | 4 | 2 | 0 | $1.50B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 10 | **Anthropic** | **6** | 2 | 4 | 2 | $965.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 11 | **The Boring Company** | **6** | 1 | 5 | 2 | $23.00B | D | TRANSPORT_MOBILITY | OPERATING_PRIVATE |
| 12 | **Dropbox** | **5** | 3 | 2 | 0 | $8.24B | D | AI_SOFTWARE | OPERATING_PUBLIC |
| 13 | **Meta Platforms** | **5** | 3 | 2 | 0 | $1.73T | D | — | UNKNOWN |
| 14 | **Beam Therapeutics** | **5** | 2 | 3 | 0 | $2.34B | C | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 15 | **GRAIL, Inc.** | **5** | 2 | 3 | 0 | — | U | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 16 | **Erebor** | **5** | 1 | 4 | 0 | — | U | FINTECH | OPERATING_PRIVATE |
| 17 | **Planet Labs** | **5** | 1 | 4 | 1 | $5.81B | D | SPACE | OPERATING_PUBLIC |
| 18 | **Applied Intuition** | **5** | 0 | 5 | 2 | $15.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 19 | **Base Power** | **5** | 0 | 5 | 0 | $13.00B | D | ENERGY_CLIMATE | OPERATING_PRIVATE |
| 20 | **Heirloom** | **5** | 0 | 5 | 2 | — | U | — | UNKNOWN |
| 21 | **Editas Medicine** | **4** | 4 | 0 | 0 | $405.45M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 22 | **Palantir Technologies** | **4** | 4 | 0 | 1 | $410.59B | D | AI_SOFTWARE | OPERATING_PUBLIC |
| 23 | **SkyPilot** | **4** | 4 | 0 | 0 | — | U | AI_SOFTWARE | OPERATING_PRIVATE |
| 24 | **Character.AI** | **4** | 3 | 1 | 0 | $2.70B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 25 | **Vercel** | **4** | 3 | 1 | 0 | $9.30B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 26 | **Chroma** | **4** | 2 | 2 | 0 | — | U | AI_SOFTWARE | OPERATING_PRIVATE |
| 27 | **Coinbase** | **4** | 2 | 2 | 0 | $44.46B | D | CRYPTO | OPERATING_PUBLIC |
| 28 | **ElevenLabs** | **4** | 2 | 2 | 0 | $11.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 29 | **Figma** | **4** | 2 | 2 | 2 | $12.28B | D | AI_SOFTWARE | OPERATING_PUBLIC |
| 30 | **Google DeepMind** | **4** | 2 | 2 | 1 | $650.00M | B | AI_SOFTWARE | ACQUIRED |


_Tier key: A = under $500M · B = $500M–$1B · C = $1B–$5B · D = $5B+ · U = unknown._
Full ranked list of all 1814 companies: `data/exports/portfolio_intersections.csv`.

---

# OUTPUT 2 — THE ACTUAL INTERSECTIONS

Every tracked person behind each of the top 30, with the relationship that counted them. `(VC)` marks people with fund-partner exposure only — they are listed for completeness and are **not** in the headline count.

### 1. Anduril Industries — 10 people

_$61.00B · 2026-05 · PRIVATE · DEFENCE · OPERATING_PRIVATE_

- **Brian Schimpf** — FOUNDER_EQUITY · 2017  _(technical elite)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Jeff Bezos** — FAMILY_OFFICE_INVESTMENT  _(founder w/ large personal capital)_
- **Joe Lonsdale** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Josh Wolfe** — CONTROLLED_FUND_INVESTMENT
- **Joshua Kushner** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Palmer Luckey** — FOUNDER_EQUITY · 2017  _(technical elite; founder w/ large personal capital)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Ron Conway** — CONTROLLED_FUND_INVESTMENT
- **Trae Stephens** — FOUNDER_EQUITY, VC_FUND_PARTNER_INVESTMENT  _(founder w/ large personal capital)_
- _(VC) fund-partner exposure only: David Ulevitch, Hemant Taneja, Katherine Boyle, Trae Stephens_

**10 total**

### 2. Uber — 9 people

_$145.14B · 2026-09-16 · PUBLIC · TRANSPORT_MOBILITY · OPERATING_PUBLIC_

- **Ali Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Chris Sacca** — CONTROLLED_FUND_INVESTMENT
- **Crystal Sacca** — CONTROLLED_FUND_INVESTMENT
- **Cyan Banister** — PERSONAL_ANGEL_INVESTMENT
- **Eric Schmidt** — CONTROLLED_FUND_INVESTMENT
- **Hadi Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Jason Calacanis** — CONTROLLED_FUND_INVESTMENT
- **Jeff Bezos** — FAMILY_OFFICE_INVESTMENT  _(founder w/ large personal capital)_
- **Naval Ravikant** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Alfred Lin, Bill Gurley, John Doerr_

**9 total**

### 3. Cognition — 9 people

_$48.00B · 2026-09 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Ali Partovi** — CONTROLLED_FUND_INVESTMENT
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **John Collison** — PERSONAL_ANGEL_INVESTMENT · 2024-03  _(founder w/ large personal capital)_
- **Josh Wolfe** — CONTROLLED_FUND_INVESTMENT
- **Patrick Collison** — PERSONAL_ANGEL_INVESTMENT · 2024-03  _(technical elite; founder w/ large personal capital)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Sarah Guo** — CONTROLLED_FUND_INVESTMENT
- **Scott Wu** — FOUNDER_EQUITY · 2023  _(technical elite)_
- **Vinod Khosla** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Trae Stephens_

**9 total**

### 4. Perplexity — 8 people

_$20.00B · 2025-09 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Andrej Karpathy** — PERSONAL_ANGEL_INVESTMENT · 2024-04  _(technical elite)_
- **Balaji Srinivasan** — PERSONAL_ANGEL_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Daniel Gross** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Guillermo Rauch** — PERSONAL_ANGEL_INVESTMENT  _(technical elite)_
- **Jeff Bezos** — FAMILY_OFFICE_INVESTMENT  _(founder w/ large personal capital)_
- **Nat Friedman** — PERSONAL_ANGEL_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Tobias Lutke** — PERSONAL_ANGEL_INVESTMENT  _(technical elite; founder w/ large personal capital)_

**8 total**

### 5. Airbnb — 8 people

_$99.75B · 2026-09-16 · PUBLIC · CONSUMER_INTERNET · OPERATING_PUBLIC_

- **Ali Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Bernard Arnault** — FAMILY_OFFICE_INVESTMENT
- **Brian Chesky** — FOUNDER_EQUITY  _(founder w/ large personal capital)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Hadi Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Jeff Bezos** — FAMILY_OFFICE_INVESTMENT  _(founder w/ large personal capital)_
- **Jessica Livingston** — CONTROLLED_FUND_INVESTMENT
- **Paul Graham** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Alfred Lin, Reid Hoffman_

**8 total**

### 6. Commonwealth Fusion Systems — 8 people

_valuation unknown · UNKNOWN · sector unlabelled · UNKNOWN_

- **Bill Gates** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Bob Mumgaard** — FOUNDER_EQUITY · 2018  _(technical elite)_
- **Chris Sacca** — CONTROLLED_FUND_INVESTMENT
- **Crystal Sacca** — CONTROLLED_FUND_INVESTMENT
- **Dennis Whyte** — FOUNDER_EQUITY · 2018  _(technical elite)_
- **Maryanna Saenko** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- **Steve Jurvetson** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- **Vinod Khosla** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Carmichael Roberts, Eric Toone_

**8 total**

### 7. SpaceX — 7 people

_$2.06T · 2026-09-16 · PUBLIC · SPACE · OPERATING_PUBLIC_

- **Daniel Gross** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Elon Musk** — FOUNDER_EQUITY · 2002  _(technical elite; founder w/ large personal capital)_
- **Hadi Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Maryanna Saenko** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Steve Jurvetson** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- _(VC) fund-partner exposure only: Ion Yadigaroglu, Shaun Maguire, Trae Stephens_

**7 total**

### 8. Stripe — 7 people

_$159.00B · 2026-02 · PRIVATE · FINTECH · OPERATING_PRIVATE_

- **Bernard Arnault** — FAMILY_OFFICE_INVESTMENT
- **Chris Sacca** — CONTROLLED_FUND_INVESTMENT
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Jessica Livingston** — CONTROLLED_FUND_INVESTMENT
- **Paul Graham** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Vinod Khosla** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Hemant Taneja, Keith Rabois, Trae Stephens_

**7 total**

### 9. Granola — 6 people

_$1.50B · 2026-03 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Amjad Masad** — PERSONAL_ANGEL_INVESTMENT · 2025-05  _(technical elite)_
- **Daniel Gross** — CONTROLLED_FUND_INVESTMENT · 2025-05  _(founder w/ large personal capital)_
- **Guillermo Rauch** — PERSONAL_ANGEL_INVESTMENT · 2025-05  _(technical elite)_
- **Mike Krieger** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Nat Friedman** — CONTROLLED_FUND_INVESTMENT · 2025-05  _(technical elite; founder w/ large personal capital)_
- **Tobias Lutke** — PERSONAL_ANGEL_INVESTMENT · 2025-05  _(technical elite; founder w/ large personal capital)_

**6 total**

### 10. Anthropic — 6 people

_$965.00B · 2026-05 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Alexis Ohanian** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Daniela Amodei** — FOUNDER_EQUITY · 2021
- **Dario Amodei** — FOUNDER_EQUITY · 2021  _(technical elite)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Eric Schmidt** — FAMILY_OFFICE_INVESTMENT · 2021-05
- **Ron Conway** — CONTROLLED_FUND_INVESTMENT
- _(VC) fund-partner exposure only: Alfred Lin, Hemant Taneja_

**6 total**

### 11. The Boring Company — 6 people

_$23.00B · 2026-09 · PRIVATE · TRANSPORT_MOBILITY · OPERATING_PRIVATE_

- **Elon Musk** — FOUNDER_EQUITY  _(technical elite; founder w/ large personal capital)_
- **Joe Lonsdale** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Li Ka-shing** — FAMILY_OFFICE_INVESTMENT · 2019  _(founder w/ large personal capital)_
- **Maryanna Saenko** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Steve Jurvetson** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- _(VC) fund-partner exposure only: Shaun Maguire, Trae Stephens_

**6 total**

### 12. Dropbox — 5 people

_$8.24B · 2026-09-16 · PUBLIC · AI_SOFTWARE · OPERATING_PUBLIC_

- **Ali Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Drew Houston** — FOUNDER_EQUITY · 2007  _(founder w/ large personal capital)_
- **Hadi Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Jessica Livingston** — CONTROLLED_FUND_INVESTMENT
- **Paul Graham** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_

**5 total**

### 13. Meta Platforms — 5 people

_$1.73T · 2026-09-16 · UNKNOWN · sector unlabelled · UNKNOWN_

- **Ali Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Hadi Partovi** — PERSONAL_ANGEL_INVESTMENT
- **Li Ka-shing** — FAMILY_OFFICE_INVESTMENT · 2007  _(founder w/ large personal capital)_
- **Sean Parker** — FOUNDER_EQUITY · 2004  _(founder w/ large personal capital)_
- **Stanley Druckenmiller** — FAMILY_OFFICE_INVESTMENT · 2026-06-30

**5 total**

### 14. Beam Therapeutics — 5 people

_$2.34B · 2026-09-16 · PUBLIC · BIOTECH_LIFESCIENCES · OPERATING_PUBLIC_

- **David Liu** — FOUNDER_EQUITY · 2017  _(technical elite)_
- **Eli Casdin** — CONTROLLED_FUND_INVESTMENT
- **Feng Zhang** — FOUNDER_EQUITY · 2017  _(technical elite)_
- **Robert Nelsen** — CONTROLLED_FUND_INVESTMENT
- **Stanley Druckenmiller** — FAMILY_OFFICE_INVESTMENT · 2026-06-30

**5 total**

### 15. GRAIL, Inc. — 5 people

_valuation unknown · PUBLIC · BIOTECH_LIFESCIENCES · OPERATING_PUBLIC_

- **Eli Casdin** — CONTROLLED_FUND_INVESTMENT
- **Jeff Bezos** — FAMILY_OFFICE_INVESTMENT  _(founder w/ large personal capital)_
- **Jeffrey Huber** — FOUNDER_EQUITY · 2016  _(technical elite)_
- **Richard Klausner** — FOUNDER_EQUITY  _(technical elite)_
- **Robert Nelsen** — CONTROLLED_FUND_INVESTMENT

**5 total**

### 16. Erebor — 5 people

_valuation unknown · PRIVATE · FINTECH · OPERATING_PRIVATE_

- **Alexis Ohanian** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Joe Lonsdale** — CONTROLLED_FUND_INVESTMENT · 2025  _(founder w/ large personal capital)_
- **Josh Wolfe** — CONTROLLED_FUND_INVESTMENT
- **Palmer Luckey** — PERSONAL_EQUITY_INVESTMENT · 2025  _(technical elite; founder w/ large personal capital)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT · 2025  _(founder w/ large personal capital)_

**5 total**

### 17. Planet Labs — 5 people

_$5.81B · 2026-09-16 · PUBLIC · SPACE · OPERATING_PUBLIC_

- **Eric Schmidt** — CONTROLLED_FUND_INVESTMENT
- **Maryanna Saenko** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Steve Jurvetson** — CONTROLLED_FUND_INVESTMENT  _(technical elite)_
- **Will Marshall** — FOUNDER_EQUITY · 2010  _(technical elite)_
- _(VC) fund-partner exposure only: Ion Yadigaroglu_

**5 total**

### 18. Applied Intuition — 5 people

_$15.00B · 2025-06 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Josh Wolfe** — CONTROLLED_FUND_INVESTMENT
- **Marc Andreessen** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Mike Maples Jr** — CONTROLLED_FUND_INVESTMENT
- **Ron Conway** — CONTROLLED_FUND_INVESTMENT
- _(VC) fund-partner exposure only: Bilal Zuberi, Hemant Taneja_

**5 total**

### 19. Base Power — 5 people

_$13.00B · 2026-08 · PRIVATE · ENERGY_CLIMATE · OPERATING_PRIVATE_

- **Chris Sacca** — CONTROLLED_FUND_INVESTMENT
- **Crystal Sacca** — CONTROLLED_FUND_INVESTMENT
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Joshua Kushner** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Ron Conway** — CONTROLLED_FUND_INVESTMENT

**5 total**

### 20. Heirloom — 5 people

_valuation unknown · UNKNOWN · sector unlabelled · UNKNOWN_

- **Alexis Ohanian** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Bill Gates** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Chris Sacca** — CONTROLLED_FUND_INVESTMENT
- **Crystal Sacca** — CONTROLLED_FUND_INVESTMENT
- **Matt Rogers** — FAMILY_OFFICE_INVESTMENT  _(technical elite)_
- _(VC) fund-partner exposure only: Carmichael Roberts, Eric Toone_

**5 total**

### 21. Editas Medicine — 4 people

_$405.45M · 2026-09-16 · PUBLIC · BIOTECH_LIFESCIENCES · OPERATING_PUBLIC_

- **David Liu** — FOUNDER_EQUITY · 2013  _(technical elite)_
- **Feng Zhang** — FOUNDER_EQUITY · 2013  _(technical elite)_
- **George Church** — FOUNDER_EQUITY · 2013  _(technical elite)_
- **Jennifer Doudna** — FOUNDER_EQUITY · 2013  _(technical elite)_

**4 total**

### 22. Palantir Technologies — 4 people

_$410.59B · 2026-09-16 · PUBLIC · AI_SOFTWARE · OPERATING_PUBLIC_

- **Alexander Karp** — FOUNDER_EQUITY  _(founder w/ large personal capital)_
- **Joe Lonsdale** — FOUNDER_EQUITY  _(founder w/ large personal capital)_
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT, FOUNDER_EQUITY  _(founder w/ large personal capital)_
- **Stephen Cohen** — FOUNDER_EQUITY  _(technical elite; founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Trae Stephens_

**4 total**

### 23. SkyPilot — 4 people

_valuation unknown · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Amjad Masad** — PERSONAL_ANGEL_INVESTMENT · 2026-07  _(technical elite)_
- **Clement Delangue** — PERSONAL_ANGEL_INVESTMENT · 2026-07
- **Guillermo Rauch** — PERSONAL_ANGEL_INVESTMENT · 2026-07  _(technical elite)_
- **Jeff Dean** — PERSONAL_ANGEL_INVESTMENT · 2026-07  _(technical elite)_

**4 total**

### 24. Character.AI — 4 people

_$2.70B · 2024-08 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Daniel Gross** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Nat Friedman** — PERSONAL_ANGEL_INVESTMENT · 2023-03  _(technical elite; founder w/ large personal capital)_
- **Noam Shazeer** — FOUNDER_EQUITY · 2021  _(technical elite)_

**4 total**

### 25. Vercel — 4 people

_$9.30B · 2025-09 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Alexandr Wang** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Gokul Rajaram** — PERSONAL_ANGEL_INVESTMENT
- **Nat Friedman** — PERSONAL_ANGEL_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Vinod Khosla** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_

**4 total**

### 26. Chroma — 4 people

_valuation unknown · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Amjad Masad** — PERSONAL_ANGEL_INVESTMENT · 2023-04  _(technical elite)_
- **Daniel Gross** — CONTROLLED_FUND_INVESTMENT · 2022-05  _(founder w/ large personal capital)_
- **Guillermo Rauch** — PERSONAL_ANGEL_INVESTMENT · 2023-04  _(technical elite)_
- **Nat Friedman** — CONTROLLED_FUND_INVESTMENT · 2022-05  _(technical elite; founder w/ large personal capital)_

**4 total**

### 27. Coinbase — 4 people

_$44.46B · 2026-09-16 · PUBLIC · CRYPTO · OPERATING_PUBLIC_

- **Brian Armstrong** — FOUNDER_EQUITY  _(founder w/ large personal capital)_
- **Daniel Gross** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Marc Andreessen** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_

**4 total**

### 28. ElevenLabs — 4 people

_$11.00B · 2026-02 · PRIVATE · AI_SOFTWARE · OPERATING_PRIVATE_

- **Alexis Ohanian** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- **Daniel Gross** — PERSONAL_ANGEL_INVESTMENT · 2024-01  _(founder w/ large personal capital)_
- **Nat Friedman** — PERSONAL_ANGEL_INVESTMENT · 2024-01  _(technical elite; founder w/ large personal capital)_
- **Nikolay Storonsky** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_

**4 total**

### 29. Figma — 4 people

_$12.28B · 2026-09-16 · PUBLIC · AI_SOFTWARE · OPERATING_PUBLIC_

- **Daniel Gross** — PERSONAL_ANGEL_INVESTMENT  _(founder w/ large personal capital)_
- **Elad Gil** — CONTROLLED_FUND_INVESTMENT  _(technical elite; founder w/ large personal capital)_
- **Gokul Rajaram** — PERSONAL_ANGEL_INVESTMENT
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Reid Hoffman, Trae Stephens_

**4 total**

### 30. Google DeepMind — 4 people

_$650.00M · 2014-01 · SUBSIDIARY · AI_SOFTWARE · ACQUIRED_

- **Demis Hassabis** — FOUNDER_EQUITY · 2010  _(technical elite)_
- **Li Ka-shing** — FAMILY_OFFICE_INVESTMENT · 2012  _(founder w/ large personal capital)_
- **Mustafa Suleyman** — FOUNDER_EQUITY · 2010
- **Peter Thiel** — CONTROLLED_FUND_INVESTMENT  _(founder w/ large personal capital)_
- _(VC) fund-partner exposure only: Trae Stephens_

**4 total**

---

# OUTPUT 3 — THE SAME METRIC, BY VALUATION BUCKET

Identical raw count, partitioned by the best sourced current valuation. **The unknown bucket is not a leftover pile** — most of the graph is in it, because portfolio pages name companies without valuing them, and several of the most interesting names are there.

## Combined: everything under $1B — 18 companies

**There are not 30 companies here, and the reason matters.** Only 18 companies in the whole graph carry a *sourced* valuation below $1B. That is a statement about valuation coverage, not about how many small companies elite people back: 1700 companies have no sourced valuation at all, and that is where the genuinely early, genuinely obscure companies live. Portfolio pages name companies without valuing them.

Several rows below are also acquired, bankrupt or shut down — kept because they are factually in the bucket, but they are history, not opportunities.

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Editas Medicine** | **4** | 4 | 0 | 0 | $405.45M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 2 | **Google DeepMind** | **4** | 2 | 2 | 1 | $650.00M | B | AI_SOFTWARE | ACQUIRED |
| 3 | **Convoy** | **2** | 2 | 0 | 0 | $0 | A | TRANSPORT_MOBILITY | SHUT_DOWN |
| 4 | **Letta** | **2** | 2 | 0 | 0 | $70.00M | A | AI_SOFTWARE | OPERATING_PRIVATE |
| 5 | **Inflection AI** | **2** | 1 | 1 | 1 | $650.00M | B | AI_SOFTWARE | OPERATING_PRIVATE |
| 6 | **Prime Medicine** | **2** | 1 | 1 | 0 | $238.76M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 7 | **Chegg** | **2** | 0 | 2 | 0 | $81.05M | A | CONSUMER_INTERNET | OPERATING_PUBLIC |
| 8 | **Sana Biotechnology** | **2** | 0 | 2 | 0 | $295.10M | A | — | UNKNOWN |
| 9 | **/dev/agents** | **1** | 1 | 0 | 0 | $500.00M | B | AI_SOFTWARE | OPERATING_PRIVATE |
| 10 | **23andMe** | **1** | 1 | 0 | 0 | $305.00M | A | BIOTECH_LIFESCIENCES | BANKRUPT |
| 11 | **Allogene Therapeutics, Inc.** | **1** | 1 | 0 | 1 | $184.00M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 12 | **Caribou Biosciences, Inc.** | **1** | 1 | 0 | 0 | $112.50M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 13 | **Deep Longevity, Inc** | **1** | 1 | 0 | 0 | $3.79M | A | BIOTECH_LIFESCIENCES | ACQUIRED |
| 14 | **Lamini** | **1** | 1 | 0 | 0 | $325.00M | A | AI_SOFTWARE | OPERATING_PRIVATE |
| 15 | **Liquid AI** | **1** | 1 | 0 | 0 | $303.00M | A | AI_SOFTWARE | OPERATING_PRIVATE |
| 16 | **Pebble** | **1** | 1 | 0 | 0 | $23.00M | A | CONSUMER_INTERNET | ACQUIRED |
| 17 | **Rethink Robotics** | **1** | 1 | 0 | 0 | $0 | A | ROBOTICS | SHUT_DOWN |
| 18 | **Zymergen** | **1** | 0 | 1 | 0 | $300.00M | A | BIOTECH_LIFESCIENCES | ACQUIRED |


### The sub-$1B universe the valuations cannot see

Unvalued companies with **3 or more** elite backers, which is where most genuinely small companies in this graph actually sit. Size is unknown, so these are **not** confirmed to be under $1B — but the early-stage ones are the closest thing to an answer to 'small company, many elite backers'.

| # | company | backers | technical elite | sector | who |
|---|---|---|---|---|---|
| 1 | **Commonwealth Fusion Systems** | **8** | 5 | — | Bill Gates; Bob Mumgaard; Chris Sacca; Crystal Sacca; Dennis Whyte; Maryanna Saenko; Steve Jurvetson; Vinod Khosla |
| 2 | **GRAIL, Inc.** | **5** | 2 | BIOTECH_LIFESCIENCES | Eli Casdin; Jeff Bezos; Jeffrey Huber; Richard Klausner; Robert Nelsen |
| 3 | **Erebor** | **5** | 1 | FINTECH | Alexis Ohanian; Joe Lonsdale; Josh Wolfe; Palmer Luckey; Peter Thiel |
| 4 | **Heirloom** | **5** | 1 | — | Alexis Ohanian; Bill Gates; Chris Sacca; Crystal Sacca; Matt Rogers |
| 5 | **Chroma** | **4** | 3 | AI_SOFTWARE | Amjad Masad; Daniel Gross; Guillermo Rauch; Nat Friedman |
| 6 | **SkyPilot** | **4** | 3 | AI_SOFTWARE | Amjad Masad; Clement Delangue; Guillermo Rauch; Jeff Dean |
| 7 | **Mill** | **4** | 1 | — | Bill Gates; Chris Sacca; Crystal Sacca; Matt Rogers |
| 8 | **Antora Energy** | **4** | 0 | ENERGY_CLIMATE | Bill Gates; Chris Sacca; Crystal Sacca; Mike Cannon-Brookes |
| 9 | **Electra** | **4** | 0 | — | Bill Gates; Chris Sacca; Crystal Sacca; Xavier Niel |
| 10 | **Living Carbon** | **4** | 0 | ENERGY_CLIMATE | Alexis Ohanian; Chris Sacca; Crystal Sacca; Mike Maples Jr |
| 11 | **Loam Bio** | **4** | 0 | ENERGY_CLIMATE | Chris Sacca; Crystal Sacca; Li Ka-shing; Mike Cannon-Brookes |
| 12 | **X (formerly Twitter)** | **4** | 0 | CONSUMER_INTERNET | Chris Sacca; Jack Dorsey; Jeff Bezos; Naval Ravikant |
| 13 | **Alphabet** | **3** | 2 | — | Larry Page; Sergey Brin; Stanley Druckenmiller |
| 14 | **Altos Labs** | **3** | 2 | BIOTECH_LIFESCIENCES | Richard Klausner; Robert Nelsen; Yuri Milner |
| 15 | **Moonwalk Biosciences** | **3** | 2 | BIOTECH_LIFESCIENCES | Feng Zhang; Robert Nelsen; Vinod Khosla |
| 16 | **Varda Space Industries** | **3** | 2 | SPACE | Balaji Srinivasan; Peter Thiel; Vinod Khosla |
| 17 | **eGenesis** | **3** | 2 | BIOTECH_LIFESCIENCES | George Church; Robert Nelsen; Vinod Khosla |
| 18 | **Benchling** | **3** | 1 | — | Balaji Srinivasan; Joshua Kushner; Ron Conway |
| 19 | **Earn.com** | **3** | 1 | — | Ali Partovi; Balaji Srinivasan; Hadi Partovi |
| 20 | **Factory AI** | **3** | 1 | — | Nikolay Storonsky; Ron Conway; Vinod Khosla |
| 21 | **Impulse Space** | **3** | 1 | SPACE | Josh Wolfe; Peter Thiel; Tom Mueller |
| 22 | **Juno Therapeutics** | **3** | 1 | — | Jeff Bezos; Richard Klausner; Robert Nelsen |
| 23 | **Kronos Bio, Inc.** | **3** | 1 | BIOTECH_LIFESCIENCES | Arie Belldegrun; Eli Casdin; Oleg Nodelman |
| 24 | **Lyell Immunopharma, Inc.** | **3** | 1 | BIOTECH_LIFESCIENCES | Bill Gates; Richard Klausner; Robert Nelsen |
| 25 | **Oculus VR** | **3** | 1 | — | Joe Lonsdale; Palmer Luckey; Peter Thiel |
| 26 | **OpenGov** | **3** | 1 | — | Balaji Srinivasan; Joe Lonsdale; Marc Andreessen |
| 27 | **Parabilis Medicines** | **3** | 1 | — | Eli Casdin; Peter Kolchinsky; Robert Nelsen |
| 28 | **Vicarious** | **3** | 1 | — | Elon Musk; Joe Lonsdale; Peter Thiel |
| 29 | **insitro** | **3** | 1 | BIOTECH_LIFESCIENCES | Daphne Koller; Jeff Bezos; Robert Nelsen |
| 30 | **Airloom** | **3** | 0 | ENERGY_CLIMATE | Bill Gates; Chris Sacca; Crystal Sacca |

## Under $500M — 15 companies

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Editas Medicine** | **4** | 4 | 0 | 0 | $405.45M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 2 | **Convoy** | **2** | 2 | 0 | 0 | $0 | A | TRANSPORT_MOBILITY | SHUT_DOWN |
| 3 | **Letta** | **2** | 2 | 0 | 0 | $70.00M | A | AI_SOFTWARE | OPERATING_PRIVATE |
| 4 | **Prime Medicine** | **2** | 1 | 1 | 0 | $238.76M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 5 | **Chegg** | **2** | 0 | 2 | 0 | $81.05M | A | CONSUMER_INTERNET | OPERATING_PUBLIC |
| 6 | **Sana Biotechnology** | **2** | 0 | 2 | 0 | $295.10M | A | — | UNKNOWN |
| 7 | **23andMe** | **1** | 1 | 0 | 0 | $305.00M | A | BIOTECH_LIFESCIENCES | BANKRUPT |
| 8 | **Allogene Therapeutics, Inc.** | **1** | 1 | 0 | 1 | $184.00M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 9 | **Caribou Biosciences, Inc.** | **1** | 1 | 0 | 0 | $112.50M | A | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 10 | **Deep Longevity, Inc** | **1** | 1 | 0 | 0 | $3.79M | A | BIOTECH_LIFESCIENCES | ACQUIRED |
| 11 | **Lamini** | **1** | 1 | 0 | 0 | $325.00M | A | AI_SOFTWARE | OPERATING_PRIVATE |
| 12 | **Liquid AI** | **1** | 1 | 0 | 0 | $303.00M | A | AI_SOFTWARE | OPERATING_PRIVATE |
| 13 | **Pebble** | **1** | 1 | 0 | 0 | $23.00M | A | CONSUMER_INTERNET | ACQUIRED |
| 14 | **Rethink Robotics** | **1** | 1 | 0 | 0 | $0 | A | ROBOTICS | SHUT_DOWN |
| 15 | **Zymergen** | **1** | 0 | 1 | 0 | $300.00M | A | BIOTECH_LIFESCIENCES | ACQUIRED |


## $500M – $1B — 3 companies

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Google DeepMind** | **4** | 2 | 2 | 1 | $650.00M | B | AI_SOFTWARE | ACQUIRED |
| 2 | **Inflection AI** | **2** | 1 | 1 | 1 | $650.00M | B | AI_SOFTWARE | OPERATING_PRIVATE |
| 3 | **/dev/agents** | **1** | 1 | 0 | 0 | $500.00M | B | AI_SOFTWARE | OPERATING_PRIVATE |


## $1B – $5B — 20 companies

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Granola** | **6** | 4 | 2 | 0 | $1.50B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 2 | **Beam Therapeutics** | **5** | 2 | 3 | 0 | $2.34B | C | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 3 | **Character.AI** | **4** | 3 | 1 | 0 | $2.70B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 4 | **AMI Labs** | **3** | 2 | 1 | 0 | $3.50B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 5 | **Weights & Biases** | **3** | 2 | 1 | 0 | $1.25B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 6 | **FieldAI** | **3** | 0 | 3 | 0 | $2.00B | C | — | UNKNOWN |
| 7 | **Solugen** | **3** | 0 | 3 | 1 | $2.05B | C | MATERIALS | OPERATING_PRIVATE |
| 8 | **Adept** | **2** | 2 | 0 | 0 | $1.00B | C | AI_SOFTWARE | OPERATING_PRIVATE |
| 9 | **Stubhub / Viagogo** | **2** | 2 | 0 | 0 | $2.25B | C | CONSUMER_INTERNET | OPERATING_PUBLIC |
| 10 | **Thumbtack** | **2** | 2 | 0 | 0 | $3.20B | C | CONSUMER_INTERNET | OPERATING_PRIVATE |
| 11 | **Zappos** | **2** | 2 | 0 | 1 | $1.20B | C | CONSUMER_INTERNET | ACQUIRED |
| 12 | **Astranis** | **2** | 0 | 2 | 0 | $2.80B | C | SPACE | OPERATING_PRIVATE |
| 13 | **QuantumScape** | **2** | 0 | 2 | 4 | $3.10B | C | ENERGY_CLIMATE | OPERATING_PUBLIC |
| 14 | **Nest** | **1** | 1 | 0 | 0 | $3.20B | C | — | UNKNOWN |
| 15 | **Netscape** | **1** | 1 | 0 | 1 | $2.90B | C | — | UNKNOWN |
| 16 | **Clover Health** | **1** | 0 | 1 | 0 | $2.48B | C | HEALTHCARE_SERVICES | OPERATING_PUBLIC |
| 17 | **Form Energy** | **1** | 0 | 1 | 3 | $2.27B | C | ENERGY_CLIMATE | OPERATING_PRIVATE |
| 18 | **Mach Industries** | **1** | 0 | 1 | 1 | $3.70B | C | DEFENCE | OPERATING_PRIVATE |
| 19 | **Opendoor** | **1** | 0 | 1 | 0 | $2.57B | C | CONSUMER_INTERNET | OPERATING_PUBLIC |
| 20 | **Upstart** | **1** | 0 | 1 | 1 | $2.47B | C | FINTECH | OPERATING_PUBLIC |


## $5B and above — 76 companies

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Anduril Industries** | **10** | 3 | 7 | 4 | $61.00B | D | DEFENCE | OPERATING_PRIVATE |
| 2 | **Uber** | **9** | 4 | 5 | 3 | $145.14B | D | TRANSPORT_MOBILITY | OPERATING_PUBLIC |
| 3 | **Cognition** | **9** | 3 | 6 | 1 | $48.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 4 | **Perplexity** | **8** | 6 | 2 | 0 | $20.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 5 | **Airbnb** | **8** | 3 | 5 | 2 | $99.75B | D | CONSUMER_INTERNET | OPERATING_PUBLIC |
| 6 | **SpaceX** | **7** | 3 | 4 | 3 | $2.06T | D | SPACE | OPERATING_PUBLIC |
| 7 | **Stripe** | **7** | 0 | 7 | 3 | $159.00B | D | FINTECH | OPERATING_PRIVATE |
| 8 | **Anthropic** | **6** | 2 | 4 | 2 | $965.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 9 | **The Boring Company** | **6** | 1 | 5 | 2 | $23.00B | D | TRANSPORT_MOBILITY | OPERATING_PRIVATE |
| 10 | **Dropbox** | **5** | 3 | 2 | 0 | $8.24B | D | AI_SOFTWARE | OPERATING_PUBLIC |
| 11 | **Meta Platforms** | **5** | 3 | 2 | 0 | $1.73T | D | — | UNKNOWN |
| 12 | **Planet Labs** | **5** | 1 | 4 | 1 | $5.81B | D | SPACE | OPERATING_PUBLIC |
| 13 | **Applied Intuition** | **5** | 0 | 5 | 2 | $15.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 14 | **Base Power** | **5** | 0 | 5 | 0 | $13.00B | D | ENERGY_CLIMATE | OPERATING_PRIVATE |
| 15 | **Palantir Technologies** | **4** | 4 | 0 | 1 | $410.59B | D | AI_SOFTWARE | OPERATING_PUBLIC |
| 16 | **Vercel** | **4** | 3 | 1 | 0 | $9.30B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 17 | **Coinbase** | **4** | 2 | 2 | 0 | $44.46B | D | CRYPTO | OPERATING_PUBLIC |
| 18 | **ElevenLabs** | **4** | 2 | 2 | 0 | $11.00B | D | AI_SOFTWARE | OPERATING_PRIVATE |
| 19 | **Figma** | **4** | 2 | 2 | 2 | $12.28B | D | AI_SOFTWARE | OPERATING_PUBLIC |
| 20 | **Rippling** | **4** | 2 | 2 | 1 | $16.80B | D | AI_SOFTWARE | OPERATING_PRIVATE |


## Valuation unknown — 1700 companies

| # | company | elite backers | direct | controlled | VC-partner | valuation | tier | sector | status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Commonwealth Fusion Systems** | **8** | 2 | 6 | 2 | — | U | — | UNKNOWN |
| 2 | **GRAIL, Inc.** | **5** | 2 | 3 | 0 | — | U | BIOTECH_LIFESCIENCES | OPERATING_PUBLIC |
| 3 | **Erebor** | **5** | 1 | 4 | 0 | — | U | FINTECH | OPERATING_PRIVATE |
| 4 | **Heirloom** | **5** | 0 | 5 | 2 | — | U | — | UNKNOWN |
| 5 | **SkyPilot** | **4** | 4 | 0 | 0 | — | U | AI_SOFTWARE | OPERATING_PRIVATE |
| 6 | **Chroma** | **4** | 2 | 2 | 0 | — | U | AI_SOFTWARE | OPERATING_PRIVATE |
| 7 | **X (formerly Twitter)** | **4** | 2 | 2 | 2 | — | U | CONSUMER_INTERNET | ACQUIRED |
| 8 | **Mill** | **4** | 1 | 3 | 2 | — | U | — | UNKNOWN |
| 9 | **Antora Energy** | **4** | 0 | 4 | 2 | — | U | ENERGY_CLIMATE | OPERATING_PRIVATE |
| 10 | **Electra** | **4** | 0 | 4 | 2 | — | U | — | UNKNOWN |
| 11 | **Living Carbon** | **4** | 0 | 4 | 0 | — | U | ENERGY_CLIMATE | OPERATING_PRIVATE |
| 12 | **Loam Bio** | **4** | 0 | 4 | 0 | — | U | ENERGY_CLIMATE | OPERATING_PRIVATE |
| 13 | **Airtime** | **3** | 3 | 0 | 0 | — | U | CONSUMER_INTERNET | OPERATING_PRIVATE |
| 14 | **Causes** | **3** | 3 | 0 | 0 | — | U | — | UNKNOWN |
| 15 | **Earn.com** | **3** | 3 | 0 | 0 | — | U | — | UNKNOWN |
| 16 | **Vicarious** | **3** | 3 | 0 | 0 | — | U | — | UNKNOWN |
| 17 | **Alphabet** | **3** | 2 | 1 | 1 | — | U | — | UNKNOWN |
| 18 | **Groq** | **3** | 2 | 1 | 0 | — | U | — | UNKNOWN |
| 19 | **Oculus VR** | **3** | 2 | 1 | 1 | — | U | — | UNKNOWN |
| 20 | **OpenGov** | **3** | 2 | 1 | 0 | — | U | — | UNKNOWN |


---

# OUTPUT 4 — INTERESTING OBSCURE INTERSECTIONS

`ANALYTICAL INTERPRETATION`, kept deliberately separate from the factual ranking above. Filter: **private or unvalued**, **not** above $5B, **≥2** elite backers, and either a frontier sector or **≥2 technically elite** backers. Ranked by technically elite backers, then raw count.

Household names are removed by an explicit list in the script, because obscurity is a judgement and not a field in the data — a company can sit in the unknown bucket simply because nobody sourced a market cap for it, which is how Alphabet first appeared here.

| company | backers | technical elite | valuation | sector | who |
|---|---|---|---|---|---|
| **Commonwealth Fusion Systems** | 8 | 5 | unknown | — | Bill Gates; Bob Mumgaard; Chris Sacca; Crystal Sacca; Dennis Whyte; Maryanna Saenko; Steve Jurvetson; Vinod Khosla |
| **Granola** | 6 | 4 | $1.50B | AI_SOFTWARE | Amjad Masad; Daniel Gross; Guillermo Rauch; Mike Krieger; Nat Friedman; Tobias Lutke |
| **Character.AI** | 4 | 3 | $2.70B | AI_SOFTWARE | Daniel Gross; Elad Gil; Nat Friedman; Noam Shazeer |
| **Chroma** | 4 | 3 | unknown | AI_SOFTWARE | Amjad Masad; Daniel Gross; Guillermo Rauch; Nat Friedman |
| **SkyPilot** | 4 | 3 | unknown | AI_SOFTWARE | Amjad Masad; Clement Delangue; Guillermo Rauch; Jeff Dean |
| **Altos Labs** | 3 | 2 | unknown | BIOTECH_LIFESCIENCES | Richard Klausner; Robert Nelsen; Yuri Milner |
| **Moonwalk Biosciences** | 3 | 2 | unknown | BIOTECH_LIFESCIENCES | Feng Zhang; Robert Nelsen; Vinod Khosla |
| **Varda Space Industries** | 3 | 2 | unknown | SPACE | Balaji Srinivasan; Peter Thiel; Vinod Khosla |
| **eGenesis** | 3 | 2 | unknown | BIOTECH_LIFESCIENCES | George Church; Robert Nelsen; Vinod Khosla |
| **Adept** | 2 | 2 | $1.00B | AI_SOFTWARE | Andrej Karpathy; David Luan |
| **Mastra** | 2 | 2 | unknown | AI_SOFTWARE | Amjad Masad; Guillermo Rauch |
| **MythicAI** | 2 | 2 | unknown | — | Maryanna Saenko; Steve Jurvetson |
| **Pairwise Plants** | 2 | 2 | unknown | — | David Liu; Feng Zhang |
| **Stylus Medicine, Inc.** | 2 | 2 | unknown | BIOTECH_LIFESCIENCES | Patrick Hsu; Vinod Khosla |
| **Valar Atomics** | 2 | 2 | unknown | ENERGY_CLIMATE | Balaji Srinivasan; Palmer Luckey |
| **Xona** | 2 | 2 | unknown | — | Maryanna Saenko; Steve Jurvetson |
| **AMI Labs** | 3 | 1 | $3.50B | AI_SOFTWARE | Bernard Arnault; Eric Schmidt; Yann LeCun |
| **Impulse Space** | 3 | 1 | unknown | SPACE | Josh Wolfe; Peter Thiel; Tom Mueller |
| **Weights & Biases** | 3 | 1 | $1.25B | AI_SOFTWARE | Aydin Senkut; Daniel Gross; Nat Friedman |
| **insitro** | 3 | 1 | unknown | BIOTECH_LIFESCIENCES | Daphne Koller; Jeff Bezos; Robert Nelsen |
| **Aera Therapeutics** | 2 | 1 | unknown | BIOTECH_LIFESCIENCES | Feng Zhang; Robert Nelsen |
| **Arbor Biotechnologies** | 2 | 1 | unknown | BIOTECH_LIFESCIENCES | Feng Zhang; Robert Nelsen |
| **Composite** | 2 | 1 | unknown | AI_SOFTWARE | Daniel Gross; Nat Friedman |
| **EvolutionaryScale** | 2 | 1 | unknown | BIOTECH_LIFESCIENCES | Daniel Gross; Nat Friedman |
| **Helical** | 2 | 1 | unknown | BIOTECH_LIFESCIENCES | Aidan Gomez; Clement Delangue |
| **Helion Energy** | 2 | 1 | unknown | ENERGY_CLIMATE | David Kirtley; Sam Altman |
| **Koloma** | 2 | 1 | unknown | ENERGY_CLIMATE | Bill Gates; Carmichael Roberts |
| **Letta** | 2 | 1 | $70.00M | AI_SOFTWARE | Clement Delangue; Jeff Dean |
| **Lovable** | 2 | 1 | unknown | AI_SOFTWARE | Nikolay Storonsky; Vinod Khosla |
| **Mammoth Biosciences** | 2 | 1 | unknown | BIOTECH_LIFESCIENCES | Jennifer Doudna; Ron Conway |

---

# OUTPUT 5 — HIGHEST INTERSECTION BY PERSON TYPE

Secondary views. The main answer above is still company → how many tracked people own or backed it.

## Most technically elite backers

_Technical band ≥4 with a research or academic archetype, or band 5 with a founder-operator archetype. Celebrity is never evidence of technical capability._

| company | technical elite count | total backers | valuation | who |
|---|---|---|---|---|
| **Perplexity** | **6** | 8 | $20.00B | Andrej Karpathy; Balaji Srinivasan; Elad Gil; Guillermo Rauch; Nat Friedman; Tobias Lutke |
| **Commonwealth Fusion Systems** | **5** | 8 | unknown | Bob Mumgaard; Dennis Whyte; Maryanna Saenko; Steve Jurvetson; Vinod Khosla |
| **Cognition** | **4** | 9 | $48.00B | Elad Gil; Patrick Collison; Scott Wu; Vinod Khosla |
| **SpaceX** | **4** | 7 | $2.06T | Elad Gil; Elon Musk; Maryanna Saenko; Steve Jurvetson |
| **Granola** | **4** | 6 | $1.50B | Amjad Masad; Guillermo Rauch; Nat Friedman; Tobias Lutke |
| **Editas Medicine** | **4** | 4 | $405.45M | David Liu; Feng Zhang; George Church; Jennifer Doudna |
| **Anduril Industries** | **3** | 10 | $61.00B | Brian Schimpf; Elad Gil; Palmer Luckey |
| **Stripe** | **3** | 7 | $159.00B | Elad Gil; Paul Graham; Vinod Khosla |
| **The Boring Company** | **3** | 6 | $23.00B | Elon Musk; Maryanna Saenko; Steve Jurvetson |
| **Planet Labs** | **3** | 5 | $5.81B | Maryanna Saenko; Steve Jurvetson; Will Marshall |
| **Character.AI** | **3** | 4 | $2.70B | Elad Gil; Nat Friedman; Noam Shazeer |
| **Chroma** | **3** | 4 | unknown | Amjad Masad; Guillermo Rauch; Nat Friedman |

## Most founder-operators with large personal capital

_**PROXY, not a sourced net-worth claim**: founder-operators at capital-flexibility band 5._

| company | billionaire founder count | total backers | valuation | who |
|---|---|---|---|---|
| **Anduril Industries** | **7** | 10 | $61.00B | Brian Schimpf; Elad Gil; Jeff Bezos; Joe Lonsdale; Josh Wolfe; Joshua Kushner; Palmer Luckey; Peter Thiel; Ron |
| **Perplexity** | **6** | 8 | $20.00B | Andrej Karpathy; Balaji Srinivasan; Daniel Gross; Elad Gil; Guillermo Rauch; Jeff Bezos; Nat Friedman; Tobias  |
| **Cognition** | **5** | 9 | $48.00B | Ali Partovi; Elad Gil; John Collison; Josh Wolfe; Patrick Collison; Peter Thiel; Sarah Guo; Scott Wu; Vinod Kh |
| **Airbnb** | **4** | 8 | $99.75B | Ali Partovi; Bernard Arnault; Brian Chesky; Elad Gil; Hadi Partovi; Jeff Bezos; Jessica Livingston; Paul Graha |
| **SpaceX** | **4** | 7 | $2.06T | Daniel Gross; Elad Gil; Elon Musk; Hadi Partovi; Maryanna Saenko; Peter Thiel; Steve Jurvetson |
| **Stripe** | **4** | 7 | $159.00B | Bernard Arnault; Chris Sacca; Elad Gil; Jessica Livingston; Paul Graham; Peter Thiel; Vinod Khosla |
| **Granola** | **4** | 6 | $1.50B | Amjad Masad; Daniel Gross; Guillermo Rauch; Mike Krieger; Nat Friedman; Tobias Lutke |
| **The Boring Company** | **4** | 6 | $23.00B | Elon Musk; Joe Lonsdale; Li Ka-shing; Maryanna Saenko; Peter Thiel; Steve Jurvetson |
| **Erebor** | **4** | 5 | unknown | Alexis Ohanian; Joe Lonsdale; Josh Wolfe; Palmer Luckey; Peter Thiel |
| **Coinbase** | **4** | 4 | $44.46B | Brian Armstrong; Daniel Gross; Elad Gil; Marc Andreessen |
| **ElevenLabs** | **4** | 4 | $11.00B | Alexis Ohanian; Daniel Gross; Nat Friedman; Nikolay Storonsky |
| **Palantir Technologies** | **4** | 4 | $410.59B | Alexander Karp; Joe Lonsdale; Peter Thiel; Stephen Cohen |

## Most frontier-AI people

_People whose primary information lens is AI._

| company | frontier ai count | total backers | valuation | who |
|---|---|---|---|---|
| **Perplexity** | **5** | 8 | $20.00B | Andrej Karpathy; Balaji Srinivasan; Daniel Gross; Elad Gil; Guillermo Rauch; Jeff Bezos; Nat Friedman; Tobias  |
| **Granola** | **5** | 6 | $1.50B | Amjad Masad; Daniel Gross; Guillermo Rauch; Mike Krieger; Nat Friedman; Tobias Lutke |
| **Airbnb** | **4** | 8 | $99.75B | Ali Partovi; Bernard Arnault; Brian Chesky; Elad Gil; Hadi Partovi; Jeff Bezos; Jessica Livingston; Paul Graha |
| **Dropbox** | **4** | 5 | $8.24B | Ali Partovi; Drew Houston; Hadi Partovi; Jessica Livingston; Paul Graham |
| **Character.AI** | **4** | 4 | $2.70B | Daniel Gross; Elad Gil; Nat Friedman; Noam Shazeer |
| **Chroma** | **4** | 4 | unknown | Amjad Masad; Daniel Gross; Guillermo Rauch; Nat Friedman |
| **SkyPilot** | **4** | 4 | unknown | Amjad Masad; Clement Delangue; Guillermo Rauch; Jeff Dean |
| **Cognition** | **3** | 9 | $48.00B | Ali Partovi; Elad Gil; John Collison; Josh Wolfe; Patrick Collison; Peter Thiel; Sarah Guo; Scott Wu; Vinod Kh |
| **SpaceX** | **3** | 7 | $2.06T | Daniel Gross; Elad Gil; Elon Musk; Hadi Partovi; Maryanna Saenko; Peter Thiel; Steve Jurvetson |
| **Anthropic** | **3** | 6 | $965.00B | Alexis Ohanian; Daniela Amodei; Dario Amodei; Elad Gil; Eric Schmidt; Ron Conway |
| **Coinbase** | **3** | 4 | $44.46B | Brian Armstrong; Daniel Gross; Elad Gil; Marc Andreessen |
| **Scale AI** | **3** | 4 | $29.00B | Alexandr Wang; Elad Gil; Guillermo Rauch; Peter Thiel |

## Most distinct primary domains represented

_One primary lens per person, so a few multi-domain people cannot manufacture apparent breadth._

| company | distinct primary domains | total backers | valuation | who |
|---|---|---|---|---|
| **Anduril Industries** | **5** | 10 | $61.00B | Brian Schimpf; Elad Gil; Jeff Bezos; Joe Lonsdale; Josh Wolfe; Joshua Kushner; Palmer Luckey; Peter Thiel; Ron |
| **Cognition** | **5** | 9 | $48.00B | Ali Partovi; Elad Gil; John Collison; Josh Wolfe; Patrick Collison; Peter Thiel; Sarah Guo; Scott Wu; Vinod Kh |
| **Uber** | **5** | 9 | $145.14B | Ali Partovi; Chris Sacca; Crystal Sacca; Cyan Banister; Eric Schmidt; Hadi Partovi; Jason Calacanis; Jeff Bezo |
| **Airbnb** | **5** | 8 | $99.75B | Ali Partovi; Bernard Arnault; Brian Chesky; Elad Gil; Hadi Partovi; Jeff Bezos; Jessica Livingston; Paul Graha |
| **Stripe** | **5** | 7 | $159.00B | Bernard Arnault; Chris Sacca; Elad Gil; Jessica Livingston; Paul Graham; Peter Thiel; Vinod Khosla |
| **Commonwealth Fusion Systems** | **4** | 8 | unknown | Bill Gates; Bob Mumgaard; Chris Sacca; Crystal Sacca; Dennis Whyte; Maryanna Saenko; Steve Jurvetson; Vinod Kh |
| **Perplexity** | **4** | 8 | $20.00B | Andrej Karpathy; Balaji Srinivasan; Daniel Gross; Elad Gil; Guillermo Rauch; Jeff Bezos; Nat Friedman; Tobias  |
| **SpaceX** | **4** | 7 | $2.06T | Daniel Gross; Elad Gil; Elon Musk; Hadi Partovi; Maryanna Saenko; Peter Thiel; Steve Jurvetson |
| **The Boring Company** | **4** | 6 | $23.00B | Elon Musk; Joe Lonsdale; Li Ka-shing; Maryanna Saenko; Peter Thiel; Steve Jurvetson |
| **Planet Labs** | **4** | 5 | $5.81B | Eric Schmidt; Maryanna Saenko; Peter Thiel; Steve Jurvetson; Will Marshall |
| **X (formerly Twitter)** | **4** | 4 | unknown | Chris Sacca; Jack Dorsey; Jeff Bezos; Naval Ravikant |
| **Anthropic** | **3** | 6 | $965.00B | Alexis Ohanian; Daniela Amodei; Dario Amodei; Elad Gil; Eric Schmidt; Ron Conway |

---

## What this does and does not say

`FACT` — every count above is distinct people with sourced, confirmed economic exposure. Each is traceable: `company_id` → `people_list` → `edge_ids` → `sources` → original URL.

`NOT ESTABLISHED` — that a high intersection predicts anything. The backtest in `reports/BACKTEST.md` cannot yet discriminate winners from failures, because the failure arm is under-collected. Several companies in the tables above had heavy elite backing and failed.

`COVERAGE` — a company appears here only because someone published something. An equally backed company whose investors publish nothing is absent entirely, and large fund portfolios (ARCH, Breakthrough Energy, Khosla, Lowercarbon) contribute many controlled-fund rows while quiet personal cheques contribute none.

