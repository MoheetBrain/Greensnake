# Research guide

All findings refer to the **16 September 2026** snapshot. Start with the [README](../README.md), then choose a question below. These are different views of the same preserved evidence, not interchangeable rankings.

| Reading priority | Exact metric and scope | Saved source |
|---|---|---|
| Primary: highest-overlap companies | `PORTFOLIO_INTERSECTION_COUNT`, exported as `number_of_elite_people`; distinct confirmed people across personal angel/equity, personal SPV, founder equity, family-office and controlled-fund types. Sort: count descending, direct/founder descending, company ascending. 1,814 companies. | [Portfolio report](../reports/PORTFOLIO_INTERSECTIONS.md), [CSV](../data/exports/portfolio_intersections.csv), [implementation](../scripts/portfolio_intersections.py) |
| Secondary: independence | `independence_adjusted_score` at δ=0.35; weighted contributions across **all confirmed relationship types**, clustered leave-one-out. `distinct_information_clusters` is a separate component count. The saved executive report publishes alternative orderings; it is not the ownership ranking. | [Executive report](../reports/EXECUTIVE_REPORT.md), [network report](../reports/NETWORK_ANALYSIS.md), [score CSV](../data/exports/company_overlap_scores.csv) |
| Technical intelligence | `technical_elite_count` and `technical_elite_score` over confirmed relationships, including non-ownership types; the technical report filters to at least two qualifying people. Technical band ≥4 plus research/academic archetype, or band 5 plus founder-operator archetype. | [Technical and cross-domain report](../reports/TECHNICAL_AND_CROSSDOMAIN.md), [methodology](METHODOLOGY.md) |
| Small-company discovery | Saved sourced valuation tiers: under $500M, $500M–$1B, $1B–$5B, $5B+. README uses economic-intersection rows; tier CSVs use all scored companies. Unknown valuations have their own universe. The executive operating-company headlines exclude terminal statuses, whereas the ownership report retains them. | [Tier exports](../data/exports/), [discovery report](../reports/COMPANY_DISCOVERY.md), [executive report](../reports/EXECUTIVE_REPORT.md) |
| Historical research | `elite_people_count` at each `as_of_date`, with outcome labels and a hindsight guard; 300 observations. Winners and failures remain. Inadequate failure collection prevents a predictive-performance claim. | [Backtest](../reports/BACKTEST.md), [observations](../data/exports/backtest_observations.csv), [cohort](../research/companies/backtest_cohort.yaml) |

## Why orderings disagree

Ownership count, raw information-network count, technical score, weighted overlap, independent-network components and independence-adjusted score answer different questions. The first does not include ordinary VC-partner, board or advisory relationships. The latter views may include them, weight them differently, or cluster correlated people together. Domain diversity is also distinct from network independence. No unified ordering has been manufactured for this presentation.

The original reports include interpretations and earlier research-workstream suggestions. Those suggestions are historical evidence, not instructions applied in this publication. Terminal companies, missing values, rejected claims and warnings remain inspectable. Historical report wording such as “current valuation” means current within the saved research snapshot.

## Walk a headline back to evidence

1. Find a company in [portfolio_intersections.csv](../data/exports/portfolio_intersections.csv) and retain `company_id`.
2. Match that ID to [edges_confirmed.csv](../data/exports/edges_confirmed.csv). Restrict to the six qualifying ownership types when reconciling the headline count; deduplicate `person_key`.
3. Match each `edge_id` to [sources.csv](../data/exports/sources.csv), where `parent_kind = edge` and `parent_id = edge_id`.
4. Inspect the URL, tier, access date and evidence summary, then the original [research batch](../research/batches/). Source liveness is historical and does not prove the claim.
5. For a valuation, follow `company_id` to [valuations.csv](../data/exports/valuations.csv), then `valuation_id` to sources with `parent_kind = valuation`.

`python scripts/query.py company "Granola"` performs a read-only company lookup and lists the broader set of confirmed connections and sources. Its `screen` subcommand uses the graph's general metrics, not the headline economic count. The complete ownership ranking is already saved; opening it does not require rebuilding.

## Before interpreting a result

Read [data quality](../reports/DATA_QUALITY.md), [coverage gaps](COVERAGE_GAPS.md), [review log](../reports/REVIEW_LOG.md) and [open work](../reports/OPEN_WORK.md). Then consult the [data dictionary](DATA_DICTIONARY.md) for denominators and field meanings. Absence of disclosure is not absence of investment; known historical exposure does not establish present ownership.
