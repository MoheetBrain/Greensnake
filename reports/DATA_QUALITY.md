# DATA QUALITY AND COVERAGE

**DATA COMPLETENESS ASSESSMENT: `EXPLORATORY`**

- only 7% of companies carry a sourced current valuation
- only 18% of edges carry an investment date, which limits every temporal metric
- Angel and family-office investing is structurally under-disclosed: absence of an edge is never evidence of absence of an investment.
- Losses and write-offs are disclosed far less often than wins, so the failure database understates true failure rates.

## People

| metric | value |
|---|---|
| total candidates researched | 190 |
| CORE_HIGH_SIGNAL | 47 |
| EXTENDED_SIGNAL | 80 |
| DOMAIN_SPECIALIST | 42 |
| WATCHLIST | 19 |
| LOW_SIGNAL_OR_POOR_VISIBILITY | 2 |
| with ≥1 confirmed edge | 178 |
| with no edge at all | 12 |

## Companies and relationships

| metric | value |
|---|---|
| raw company name strings seen | 2234 |
| canonical companies after dedup | 2188 |
| name strings merged by dedup | 46 |
| relationships investigated (edges + rejected + queued) | 3411 |
| CONFIRMED_PRIMARY | 2795 |
| CONFIRMED_MULTI_SOURCE | 331 |
| CONFIRMED_REPUTABLE_SECONDARY | 79 |
| PROBABLE_BUT_NOT_CONFIRMED | 34 |
| CONFLICTING_EVIDENCE | 0 |
| UNVERIFIED | 0 |
| REJECTED (investigated and not supported) | 67 |
| unresolved claims in research queue | 105 |
| **% of confirmed edges with Tier-1 primary evidence** | **97.2%** |
| % of confirmed edges resting only on reputable secondary | 2.8% |
| distinct source domains cited | 209 |
| % of edges carrying an investment date | 17.9% |

### Confirmed edges by relationship type

| relationship | n |
|---|---|
| `CONTROLLED_FUND_INVESTMENT` | 1375 |
| `VC_FUND_PARTNER_INVESTMENT` | 590 |
| `FAMILY_OFFICE_INVESTMENT` | 406 |
| `PERSONAL_ANGEL_INVESTMENT` | 299 |
| `FOUNDER_EQUITY` | 259 |
| `BOARD_ONLY` | 109 |
| `PERSONAL_EQUITY_INVESTMENT` | 55 |
| `ADVISOR_ONLY` | 49 |
| `OTHER_VERIFIED` | 37 |
| `PHILANTHROPIC_FUNDING` | 23 |
| `CORPORATE_STRATEGIC_INVESTMENT` | 2 |
| `LP_INDIRECT` | 1 |

## Valuation coverage

| metric | value |
|---|---|
| companies with a sourced current valuation | 145 (6.6%) |
| **companies with UNKNOWN valuation** | **2043** |
| companies with entry-valuation information | 5 |
| public companies | 49 |
| private companies | 455 |
| public/private unknown | 1684 |

### Valuation age (share of valued companies)

| band | n | % |
|---|---|---|
| LT_6M | 60 | 41.4% |
| 6_TO_12M | 15 | 10.3% |
| 12_TO_18M | 21 | 14.5% |
| 18_TO_36M | 15 | 10.3% |
| GT_36M | 34 | 23.4% |

### Companies per tier

| tier | n |
|---|---|
| `TIER_A_UNDER_500M` | 16 |
| `TIER_B_500M_TO_1B` | 3 |
| `TIER_C_1B_TO_5B` | 20 |
| `TIER_D_5B_PLUS` | 81 |
| `TIER_U_UNKNOWN` | 2023 |

## Sector and geography coverage

`1682` of 2188 companies carry no sector label and `1836` no country. Both are collection gaps: most edges came from portfolio pages and filings that name a company without describing it. **An unlabelled company is invisible to any sector-level analysis**, so the sector table below understates every category.

| sector | companies |
|---|---|
| (unlabelled) | 1682 |
| AI_SOFTWARE | 98 |
| INDUSTRIAL_DEEPTECH | 80 |
| ENERGY_CLIMATE | 66 |
| BIOTECH_LIFESCIENCES | 59 |
| FINTECH | 49 |
| CONSUMER_INTERNET | 32 |
| MATERIALS | 29 |
| SPACE | 19 |
| DEFENCE | 18 |
| ROBOTICS | 13 |
| TRANSPORT_MOBILITY | 12 |
| HEALTHCARE_SERVICES | 10 |
| AGRICULTURE_FOOD | 7 |
| SEMICONDUCTORS | 5 |
| QUANTUM | 3 |
| GENERALIST | 3 |
| CRYPTO | 3 |

| country | companies |
|---|---|
| (unstated) | 1836 |
| US | 209 |
| FR | 28 |
| GB | 22 |
| CA | 16 |
| AU | 10 |
| IL | 7 |
| ID | 6 |
| HK | 6 |
| IN | 5 |
| SE | 4 |
| NZ | 4 |
| DE | 4 |
| BR | 4 |
| TR | 3 |
| PH | 2 |
| MX | 2 |
| CO | 2 |
| CH | 2 |
| BE | 2 |
| Australia | 2 |
| UA | 1 |

### Confirmed edges by workstream

| workstream | confirmed edges |
|---|---|
| `agent_5` | 1043 |
| `agent_2` | 864 |
| `agent_3` | 479 |
| `agent_6` | 470 |
| `agent_4` | 203 |
| `agent_1` | 146 |

See `docs/COVERAGE_GAPS.md` for the named, specific gaps each workstream reported — paywalled sources, image-only portfolio pages and people whose vehicles publish nothing.


## Source liveness

- URLs checked: 4676
- resolving: 84.3%
- failing: 736 (401/403/405/429 count as resolving — a paywalled page is a real page)

## People whose portfolios could not be reconstructed

12 of 190 tracked people have **no confirmed edge**. 

This is a coverage statement, not a statement about those people. Several were included precisely to measure the visibility floor. **Absence of an edge is never evidence of absence of an investment.**

| person | class |
|---|---|
| Jensen Huang | CORE_HIGH_SIGNAL |
| Chris Olah | DOMAIN_SPECIALIST |
| Jared Kaplan | DOMAIN_SPECIALIST |
| Lisa Su | DOMAIN_SPECIALIST |
| Shane Legg | DOMAIN_SPECIALIST |
| Brad Gerstner | EXTENDED_SIGNAL |
| Chase Coleman | EXTENDED_SIGNAL |
| Lee Fixel | EXTENDED_SIGNAL |
| Michael Moritz | EXTENDED_SIGNAL |
| Philippe Laffont | EXTENDED_SIGNAL |
| Kevin Scott | WATCHLIST |
| Satya Nadella | WATCHLIST |
