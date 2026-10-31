# HISTORICAL BACKTEST AND NEGATIVE CONTROLS

## How this test is constructed

Every snapshot is computed **two ways**, because an edge can be true in 2016 and only become public in a 2021 filing. Counting the latter as visible in 2016 would be cheating.

| view | definition | use |
|---|---|---|
| `AS_INVESTED` | `investment_date ≤ T` | what was **true** at T. Upper bound, contaminated by hindsight. |
| `AS_KNOWABLE` | `investment_date ≤ T` **and** earliest source publication `≤ T` | what a researcher running this system at T could actually have **seen**. |
| `upper bound` | AS_KNOWABLE + edges whose source carries no publication date | the most it could have been. |

**Only `AS_KNOWABLE` is a legitimate backtest number**, and it is a **strict lower bound**: many sources (portfolio pages, personal investment lists, SEC filing indexes) carry no publication date at all, so an edge that was genuinely public at T is excluded from it. Those edges are counted separately, and the true value lies between AS_KNOWABLE and the upper bound. Where the two are far apart the test is uninformative and says so rather than pretending otherwise.

Edges with no `investment_date` are excluded from both rather than imputed; `temporal coverage` below shows what fraction of each company's confirmed edges the test could actually use.

## Cohort coverage

| outcome | companies in graph |
|---|---|
| `WINNER` | 15 |
| `STRONG` | 1 |
| `MEDIOCRE` | 9 |
| `FAILURE` | 25 |

**1 cohort companies carry no confirmed edge in the graph and are therefore absent from this test**: Adept AI

This is a collection gap, not a finding about those companies. It biases the test toward whichever arm happens to be better covered, which is why the discrimination result below is reported with that caveat attached.

---

## Snapshots

### Anduril Industries — `WINNER`

_14 confirmed edges now; temporal coverage 0.14 (12 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 2 | 2 | 2 | — | — |
| 2020-01 | **0** | 2 | 2 | 2 | — | — |
| 2022-01 | **0** | 2 | 2 | 2 | — | — |
| 2024-01 | **0** | 2 | 2 | 2 | — | — |
| 2026-01 | **0** | 2 | 2 | 2 | — | — |

### Anthropic — `WINNER`

_8 confirmed edges now; temporal coverage 0.38 (5 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **3** | 3 | 3 | 0 | — | Daniela Amodei, Dario Amodei, Eric Schmidt |
| 2024-01 | **3** | 3 | 3 | 0 | — | Daniela Amodei, Dario Amodei, Eric Schmidt |
| 2026-01 | **3** | 3 | 3 | 0 | — | Daniela Amodei, Dario Amodei, Eric Schmidt |

### Bloom Energy — `WINNER`

_1 confirmed edges now; temporal coverage 1.00 (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 1 | 1 | 1 | — | — |
| 2018-01 | **0** | 1 | 1 | 1 | — | — |
| 2020-01 | **0** | 1 | 1 | 1 | — | — |
| 2022-01 | **0** | 1 | 1 | 1 | — | — |
| 2024-01 | **0** | 1 | 1 | 1 | — | — |
| 2026-01 | **0** | 1 | 1 | 1 | — | — |

### Canva — `WINNER`

_3 confirmed edges now; temporal coverage 0.00 (3 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | $42.00B | — |

### Databricks — `WINNER`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### DeepMind — `WINNER`

_5 confirmed edges now; temporal coverage 0.60 (2 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 1 | 3 | 3 | $650.00M | — |
| 2018-01 | **0** | 1 | 3 | 3 | $650.00M | — |
| 2020-01 | **0** | 1 | 3 | 3 | $650.00M | — |
| 2022-01 | **1** | 2 | 3 | 2 | $650.00M | Li Ka-shing |
| 2024-01 | **2** | 3 | 3 | 1 | $650.00M | Mustafa Suleyman, Li Ka-shing |
| 2026-01 | **2** | 3 | 3 | 1 | $650.00M | Mustafa Suleyman, Li Ka-shing |

### Figma — `WINNER`

_6 confirmed edges now; temporal coverage 0.00 (6 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Nubank — `WINNER`

_3 confirmed edges now; temporal coverage 0.00 (3 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### OpenAI — `WINNER`

_15 confirmed edges now; temporal coverage 0.67 (5 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **8** | 8 | 8 | 0 | — | Andrej Karpathy, Elon Musk, Greg Brockman, Ilya Sutskever, John Schulman, Peter Thiel, Sam Altman, Yoshua Bengio |
| 2018-01 | **8** | 8 | 8 | 0 | — | Andrej Karpathy, Elon Musk, Greg Brockman, Ilya Sutskever, John Schulman, Peter Thiel, Sam Altman, Yoshua Bengio |
| 2020-01 | **8** | 8 | 8 | 0 | — | Andrej Karpathy, Elon Musk, Greg Brockman, Ilya Sutskever, John Schulman, Peter Thiel, Sam Altman, Yoshua Bengio |
| 2022-01 | **8** | 8 | 8 | 0 | — | Andrej Karpathy, Elon Musk, Greg Brockman, Ilya Sutskever, John Schulman, Peter Thiel, Sam Altman, Yoshua Bengio |
| 2024-01 | **8** | 8 | 8 | 0 | — | Andrej Karpathy, Elon Musk, Greg Brockman, Ilya Sutskever, John Schulman, Peter Thiel, Sam Altman, Yoshua Bengio |
| 2026-01 | **8** | 8 | 8 | 0 | — | Andrej Karpathy, Elon Musk, Greg Brockman, Ilya Sutskever, John Schulman, Peter Thiel, Sam Altman, Yoshua Bengio |

### Palantir — `WINNER`

_7 confirmed edges now; temporal coverage 0.00 (7 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Revolut — `WINNER`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Scale AI — `WINNER`

_5 confirmed edges now; temporal coverage 0.20 (4 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 1 | 1 | — | — |
| 2018-01 | **0** | 0 | 1 | 1 | — | — |
| 2020-01 | **0** | 0 | 1 | 1 | — | — |
| 2022-01 | **0** | 0 | 1 | 1 | — | — |
| 2024-01 | **0** | 0 | 1 | 1 | — | — |
| 2026-01 | **0** | 0 | 1 | 1 | $29.00B | — |

### SpaceX — `WINNER`

_11 confirmed edges now; temporal coverage 0.09 (10 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 1 | 1 | — | — |
| 2018-01 | **0** | 0 | 1 | 1 | — | — |
| 2020-01 | **0** | 0 | 1 | 1 | — | — |
| 2022-01 | **0** | 0 | 1 | 1 | — | — |
| 2024-01 | **0** | 0 | 1 | 1 | — | — |
| 2026-01 | **0** | 0 | 1 | 1 | — | — |

### Stripe — `WINNER`

_10 confirmed edges now; temporal coverage 0.00 (10 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Wiz — `WINNER`

_2 confirmed edges now; temporal coverage 0.00 (2 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Commonwealth Fusion Systems — `STRONG`

_10 confirmed edges now; temporal coverage 0.20 (8 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 1 | 2 | 2 | — | — |
| 2020-01 | **0** | 1 | 2 | 2 | — | — |
| 2022-01 | **0** | 1 | 2 | 2 | — | — |
| 2024-01 | **0** | 1 | 2 | 2 | — | — |
| 2026-01 | **1** | 2 | 2 | 1 | — | Bob Mumgaard |

### Blue Apron — `MEDIOCRE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $103.00M | — |
| 2026-01 | **0** | 0 | 0 | 0 | $103.00M | — |

### Casper — `MEDIOCRE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | $286.00M | — |
| 2024-01 | **0** | 0 | 0 | 0 | $286.00M | — |
| 2026-01 | **0** | 0 | 0 | 0 | $286.00M | — |

### Character.AI — `MEDIOCRE`

_4 confirmed edges now; temporal coverage 0.50 (2 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 1 | 1 | — | — |
| 2024-01 | **2** | 2 | 2 | 0 | $1.00B | Noam Shazeer, Nat Friedman |
| 2026-01 | **2** | 2 | 2 | 0 | $2.70B | Noam Shazeer, Nat Friedman |

### Clover Health — `MEDIOCRE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Inflection AI — `MEDIOCRE`

_3 confirmed edges now; temporal coverage 0.67 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **1** | 1 | 1 | 0 | — | Li Ka-shing |
| 2024-01 | **2** | 2 | 2 | 0 | — | Li Ka-shing, Mustafa Suleyman |
| 2026-01 | **2** | 2 | 2 | 0 | $650.00M | Li Ka-shing, Mustafa Suleyman |

### Magic Leap — `MEDIOCRE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | $450.00M | — |
| 2024-01 | **0** | 0 | 0 | 0 | $450.00M | — |
| 2026-01 | **0** | 0 | 0 | 0 | $450.00M | — |

### Opendoor — `MEDIOCRE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Stability AI — `MEDIOCRE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### Virgin Galactic — `MEDIOCRE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | — | — |

### 23andMe — `FAILURE`

_2 confirmed edges now; temporal coverage 0.00 (2 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | $305.00M | — |

### Argo AI — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Better Place — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2018-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2020-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Bird — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Britishvolt — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Convoy — `FAILURE`

_2 confirmed edges now; temporal coverage 0.00 (2 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Essential Products — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### FTX — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Fast — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Juicero — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2020-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Katerra — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Lordstown Motors — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $10.20M | — |
| 2026-01 | **0** | 0 | 0 | 0 | $10.20M | — |

### Nikola — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Olive AI — `FAILURE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Pebble — `FAILURE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | $23.00M | — |
| 2020-01 | **0** | 0 | 0 | 0 | $23.00M | — |
| 2022-01 | **0** | 0 | 0 | 0 | $23.00M | — |
| 2024-01 | **0** | 0 | 0 | 0 | $23.00M | — |
| 2026-01 | **0** | 0 | 0 | 0 | $23.00M | — |

### Proterra — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Quibi — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Rethink Robotics — `FAILURE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Solyndra — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2018-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2020-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Theranos — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2022-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### View — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Virgin Hyperloop — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### WeWork — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | — | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Zume — `FAILURE`

_0 confirmed edges now; temporal coverage — (0 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $0 | — |
| 2026-01 | **0** | 0 | 0 | 0 | $0 | — |

### Zymergen — `FAILURE`

_1 confirmed edges now; temporal coverage 0.00 (1 undated edges excluded)_

| as of | AS_KNOWABLE | upper bound | AS_INVESTED | hindsight gap | valuation then | who was knowable |
|---|---|---|---|---|---|---|
| 2016-01 | **0** | 0 | 0 | 0 | — | — |
| 2018-01 | **0** | 0 | 0 | 0 | — | — |
| 2020-01 | **0** | 0 | 0 | 0 | — | — |
| 2022-01 | **0** | 0 | 0 | 0 | — | — |
| 2024-01 | **0** | 0 | 0 | 0 | $300.00M | — |
| 2026-01 | **0** | 0 | 0 | 0 | $300.00M | — |

---

## Discrimination: do winners separate from failures?

`AS_KNOWABLE` overlap by outcome group at each date.

**2016-01**

| outcome | n | mean | median | max | with zero overlap |
|---|---|---|---|---|---|
| `WINNER` | 15 | 0.53 | 0 | 8 | 14 |
| `STRONG` | 1 | 0.00 | 0 | 0 | 1 |
| `MEDIOCRE` | 9 | 0.00 | 0 | 0 | 9 |
| `FAILURE` | 25 | 0.00 | 0 | 0 | 25 |

_winner mean − failure mean: **0.53**_

**2018-01**

| outcome | n | mean | median | max | with zero overlap |
|---|---|---|---|---|---|
| `WINNER` | 15 | 0.53 | 0 | 8 | 14 |
| `STRONG` | 1 | 0.00 | 0 | 0 | 1 |
| `MEDIOCRE` | 9 | 0.00 | 0 | 0 | 9 |
| `FAILURE` | 25 | 0.00 | 0 | 0 | 25 |

_winner mean − failure mean: **0.53**_

**2020-01**

| outcome | n | mean | median | max | with zero overlap |
|---|---|---|---|---|---|
| `WINNER` | 15 | 0.53 | 0 | 8 | 14 |
| `STRONG` | 1 | 0.00 | 0 | 0 | 1 |
| `MEDIOCRE` | 9 | 0.00 | 0 | 0 | 9 |
| `FAILURE` | 25 | 0.00 | 0 | 0 | 25 |

_winner mean − failure mean: **0.53**_

**2022-01**

| outcome | n | mean | median | max | with zero overlap |
|---|---|---|---|---|---|
| `WINNER` | 15 | 0.80 | 0 | 8 | 12 |
| `STRONG` | 1 | 0.00 | 0 | 0 | 1 |
| `MEDIOCRE` | 9 | 0.11 | 0 | 1 | 8 |
| `FAILURE` | 25 | 0.00 | 0 | 0 | 25 |

_winner mean − failure mean: **0.80**_

**2024-01**

| outcome | n | mean | median | max | with zero overlap |
|---|---|---|---|---|---|
| `WINNER` | 15 | 0.87 | 0 | 8 | 12 |
| `STRONG` | 1 | 0.00 | 0 | 0 | 1 |
| `MEDIOCRE` | 9 | 0.44 | 0 | 2 | 7 |
| `FAILURE` | 25 | 0.00 | 0 | 0 | 25 |

_winner mean − failure mean: **0.87**_

**2026-01**

| outcome | n | mean | median | max | with zero overlap |
|---|---|---|---|---|---|
| `WINNER` | 15 | 0.87 | 0 | 8 | 12 |
| `STRONG` | 1 | 1.00 | 1 | 1 | 0 |
| `MEDIOCRE` | 9 | 0.44 | 0 | 2 | 7 |
| `FAILURE` | 25 | 0.00 | 0 | 0 | 25 |

_winner mean − failure mean: **0.87**_

---

## How to read this

`ANALYSIS` — with cohorts this size the separation figures are **descriptive, not a significance test**. Three things must hold before elite overlap can be called predictive, and they are not yet all satisfied here:

1. **Both arms need comparable edge coverage.** The research workstreams were pointed at people, and people's portfolios are documented through their *wins*. Failures are systematically under-collected, which inflates any measured separation. Fixing this requires collecting failure edges deliberately, not waiting for them to appear.
2. **The `AS_KNOWABLE` view must carry the result.** If separation exists only in `AS_INVESTED`, the signal is retrospective and untradeable.
3. **Correlation adjustment must not erase it.** If independence-adjusted overlap separates the arms no better than raw overlap does, what looked like many independent signals was one network.

The negative controls in `SECONDARY_QUESTIONS.md` question 14 list the companies that had elite backing and still failed. Those are the rows that keep this honest.

