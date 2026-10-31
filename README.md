# GREENSNAKE — Open Research Dataset

A source-backed graph of investment relationships among founders, scientists, investors and high-information capital networks. It maps documented relationships to companies to identify companies appearing across multiple such networks.

> Which companies repeatedly appear across the investment networks of exceptionally informed people?

**Research snapshot: 16 September 2026.** All relationships, company statuses, valuations and scores below describe the saved research snapshot; they are not live market data.

**Publication status: public research release — 31 October 2026.** Published with an independent, audited Git history and GitHub noreply attribution. The original history is preserved privately; [publication and preservation notes](docs/PUBLICATION_NOTES.md#historical-privacy-blocker-and-resolution) explain the resolved metadata blocker and limits on recalling earlier exposure.

[Complete rankings](reports/PORTFOLIO_INTERSECTIONS.md) · [Source evidence](data/exports/sources.csv) · [Reproducibility](#reproducibility) · [Licensing](DATA_LICENSE.md) · [Citation](CITATION.cff) · [Download SQLite](https://github.com/MoheetBrain/Greensnake/raw/refs/heads/main/database/elite_graph.sqlite) · [CSV datasets](data/exports/) · [Methodology](docs/METHODOLOGY.md) · [Research guide](docs/RESEARCH_GUIDE.md)

## Research at a glance

| Tracked people | Canonical companies | Confirmed person–company relationships | Source records |
|---:|---:|---:|---:|
| **190** | **2,188** | **3,205** | **4,694** |

Reconciled to the committed SQLite database and [quality report](reports/DATA_QUALITY.md). Relationships are edge records, not a count of distinct personal shareholdings. Source records may cite the same URL. The graph also retains **34 unconfirmed relationships, 105 unresolved claims and 67 rejected claims**.

## Top 10 portfolio intersections

The highest-overlap companies by **`PORTFOLIO_INTERSECTION_COUNT`**: distinct tracked people with at least one confirmed qualifying economic-ownership relationship. One person counts once per company.

| Rank | Company | Sector | Economic exposure | Direct / founder | Controlled vehicle | Sourced valuation | Valuation date | Public / private |
|---:|---|---|---:|---:|---:|---:|---|---|
| 1 | Anduril Industries | Defence | 10 | 3 | 7 | $61.00B | 2026-05 | Private |
| 2 | Uber | Transport Mobility | 9 | 4 | 5 | $145.14B | 2026-09-16 | Public |
| 3 | Cognition | Ai Software | 9 | 3 | 6 | $48.00B | 2026-09 | Private |
| 4 | Perplexity | Ai Software | 8 | 6 | 2 | $20.00B | 2025-09 | Private |
| 5 | Airbnb | Consumer Internet | 8 | 3 | 5 | $99.75B | 2026-09-16 | Public |
| 6 | Commonwealth Fusion Systems | Unlabelled | 8 | 2 | 6 | Unknown | — | Unknown |
| 7 | SpaceX | Space | 7 | 3 | 4 | $2.06T | 2026-09-16 | Public |
| 8 | Stripe | Fintech | 7 | 0 | 7 | $159.00B | 2026-02 | Private |
| 9 | Granola | Ai Software | 6 | 4 | 2 | $1.50B | 2026-03 | Private |
| 10 | Anthropic | Ai Software | 6 | 2 | 4 | $965.00B | 2026-05 | Private |

**Cutoff tie:** The Boring Company also has **6** connections (1 direct/founder, 5 controlled), placing 11th under the saved ordering. Counts sort descending, then direct/founder connections descending, then company name ascending. Rank is an ordered position; tied economic counts do not imply stronger evidence or expected returns.

Counted relationships are personal angel/equity investment, personal SPV and founder equity, plus family-office and controlled-fund investment. If someone qualifies through both direct and controlled relationships, they appear in the direct column only. Advisory, board-only, philanthropic, LP and ordinary VC-partner associations do **not** count. Debt, corporate strategic and other verified relationships are also excluded from this ownership metric.

The values and public/private labels above are reproduced from the saved dataset, including its unknown fields. Valuations have different bases—priced rounds, secondary/tender marks, reported valuations and public market capitalisations—and are not directly equivalent. Dates retain the source's precision. See [all 1,814 ranked companies and their backers](reports/PORTFOLIO_INTERSECTIONS.md), the [full CSV](data/exports/portfolio_intersections.csv) and [valuation evidence](data/exports/valuations.csv).

## How the model works

```text
People → Verified Relationships → Companies → Network Analysis → Overlap Rankings
```

| Relationship layer | Interpretation |
|---|---|
| Direct personal investment | Documented personal angel/equity or personal-SPV exposure |
| Founder equity | Founding ownership; kept distinguishable from later investment selection |
| Controlled investment funds | Exposure through a fund the tracked person controls |
| Family-office investments | Exposure attributed to the person's family-office vehicle |
| Venture-fund partner involvement | Firm participation associated with a partner; personal ownership is not implied |
| Information-network relationships | Board, advisory, LP and other verified links; useful for network analysis |

**Not every person–company relationship represents a personal shareholding.** The headline ownership metric is narrower than the methodology's BROAD metric, which also includes debt and corporate strategic relationships. Network and technical reports can use all confirmed relationship types. [Definitions and formulas](docs/METHODOLOGY.md) are preserved as published.

## Rankings by valuation

These are the same economic-exposure counts, filtered by the saved valuation tier and ordered exactly as the portfolio-intersection CSV. No missing valuation is estimated. Dollar boundaries are half-open; the final known tier includes **$5B and above**.

### Under $500M

0 ≤ value < $500M · 15 companies in the economic-intersection universe.

| Company | Economic exposure | Sourced valuation | Valuation date | Saved status |
|---|---:|---:|---|---|
| Editas Medicine | 4 | $405.45M | 2026-09-16 | Operating Public |
| Convoy | 2 | $0 | 2023-10 | Shut Down |
| Letta | 2 | $70.00M | 2024-09 | Operating Private |

### $500M–$1B

$500M ≤ value < $1B · 3 companies in the economic-intersection universe.

| Company | Economic exposure | Sourced valuation | Valuation date | Saved status |
|---|---:|---:|---|---|
| Google DeepMind | 4 | $650.00M | 2014-01 | Acquired |
| Inflection AI | 2 | $650.00M | 2024-03 | Operating Private |
| /dev/agents | 1 | $500.00M | 2024-12 | Operating Private |

### $1B–$5B

$1B ≤ value < $5B · 20 companies in the economic-intersection universe.

| Company | Economic exposure | Sourced valuation | Valuation date | Saved status |
|---|---:|---:|---|---|
| Granola | 6 | $1.50B | 2026-03 | Operating Private |
| Beam Therapeutics | 5 | $2.34B | 2026-09-16 | Operating Public |
| Character.AI | 4 | $2.70B | 2024-08 | Operating Private |

### Above $5B (including exactly $5B)

$5B ≤ value · 76 companies in the economic-intersection universe.

| Company | Economic exposure | Sourced valuation | Valuation date | Saved status |
|---|---:|---:|---|---|
| Anduril Industries | 10 | $61.00B | 2026-05 | Operating Private |
| Uber | 9 | $145.14B | 2026-09-16 | Operating Public |
| Cognition | 9 | $48.00B | 2026-09 | Operating Private |

### Valuation unknown

No sourced selected valuation · 1,700 companies in the economic-intersection universe.

| Company | Economic exposure | Sourced valuation | Valuation date | Saved status |
|---|---:|---:|---|---|
| Commonwealth Fusion Systems | 8 | Unknown | — | Unknown |
| GRAIL, Inc. | 5 | Unknown | — | Operating Public |
| Erebor | 5 | Unknown | — | Operating Private |

Acquired, merged, bankrupt and shut-down companies remain in the historical dataset and these unfiltered ownership tables; their marks can be acquisition prices or terminal values. They are distinguished by status, not presented as operating-company discoveries. Unknown status stays unknown. **Unknown valuation does not mean small.**

The broader [tier exports](data/exports/) and [executive report](reports/EXECUTIVE_REPORT.md) cover a different universe and may rank differently. There are 2,143 scored companies versus 2,188 canonical companies; 45 lack confirmed relationships. See the [denominator reconciliation](docs/DATA_DICTIONARY.md#population-and-denominator-reconciliation).

## Network independence

Ten people from the same investment network may reflect fewer than ten independent investment decisions. The existing derived adjustment discounts additional contributions within each correlated cluster:

$$
IA(\delta)=\sum_{c \in \mathcal{C}}\left[\max_{p\in c} a_p + \delta\left(\sum_{p\in c}a_p-\max_{p\in c}a_p\right)\right]
$$

Here $a_p$ is the person's published weight multiplied by their strongest confirmed relationship weight. At the default **δ = 0.35**, the strongest contribution in each cluster counts fully and the remainder count at 35%. The saved outputs also show δ = 0 and δ = 1. These are model assumptions and derived scores, separate from raw factual counts.

Clusters are computed **leave-one-out**: when scoring a company, its own co-investments are removed from the evidence used to connect its backers. Correlation components use the existing strength threshold of 0.50; derived co-investment links require at least three other shared confirmed companies. Co-founders of the scored company are grouped as one founding decision. Network independence is distinct from domain diversity and does not establish statistical independence.

Read the [network analysis](reports/NETWORK_ANALYSIS.md), [formula details](docs/METHODOLOGY.md) and [guide to the different rankings](docs/RESEARCH_GUIDE.md). The economic-intersection ranking is not reordered by these scores.

## Reproducibility

Requires **Python 3.11+**, **PyYAML** and **requests**. Publication checks used Python 3.12. The database is ordinary SQLite; invariant tests use the standard library.

```bash
git clone https://github.com/MoheetBrain/Greensnake.git
cd Greensnake
python3 -m venv .venv
source .venv/bin/activate
python -m pip install PyYAML requests

# Verify the preserved snapshot without modifying it.
python scripts/verify_snapshot.py
python tests/test_invariants.py

# Read company evidence and broader information-network screens.
python scripts/query.py company "Granola"
python scripts/query.py screen --min-clusters 3 --sort independence

# View the saved ownership ranking without regenerating outputs.
python -c 'import csv; from itertools import islice; print(*[(r["rank"], r["company"], r["number_of_elite_people"]) for r in islice(csv.DictReader(open("data/exports/portfolio_intersections.csv")), 11)], sep="\n")'
```

Rebuild in a **separate checkout**: the existing build script reinitialises its database and rewrites exports and reports. Pin the research date explicitly.

```bash
git worktree add --detach ../Greensnake-rebuild HEAD
cd ../Greensnake-rebuild
../Greensnake/.venv/bin/python scripts/build_graph.py --as-of 2026-09-16
../Greensnake/.venv/bin/python tests/test_invariants.py
../Greensnake/.venv/bin/python scripts/portfolio_intersections.py
git status --short
```

The publication audit reproduced the headline counts and all economic-intersection counts and ordering, and the economic-intersection report in a disposable rebuild. **Byte-identical full rebuilds are not established:** collection/build metadata uses the execution date, JSON key order can vary, and small derived-score rounding differences can change other report/export ordering. The published snapshot remains authoritative and unchanged. See [publication notes](docs/PUBLICATION_NOTES.md) before accepting rebuilt outputs. [Updating instructions](docs/UPDATING.md) describe the existing research workflow; this release adds no research.

## Data quality and limitations

The saved completeness assessment is **EXPLORATORY**.

- **145 / 2,188 companies (6.6%)** have a selected sourced valuation; **2,043** have none across the canonical universe. Unknown valuations remain visible.
- **581 / 3,239 relationship records (17.9%)** have investment dates, including confirmed and unconfirmed records. Temporal analysis excludes undated observations.
- Public portfolio disclosure is incomplete. Absence of a relationship is not evidence of no investment; successful investments are systematically easier to discover than failures.
- People inclusion, score anchors and network correlation assumptions involve judgement. Scores are not independently validated measures of ability.
- The historical backtest **does not yet establish predictive investment performance**; failure-arm coverage is insufficient. Its negative results and controls are retained.
- Saved validation has **8 PASS, 3 WARN, 0 FAIL**: eight near-match entity pairs, seven founder-equity records with priced-round labels, and 24 confirmed relationships with no citation recorded as still resolving. Existing review decisions are in the [review log](reports/REVIEW_LOG.md).
- The historical URL check recorded 736 failing source records out of 4,676 checked; HTTP 401/403/405/429 count as resolving. These are source-record counts, not unique URL counts, and do not describe present-day availability.

The dataset does not establish that backers retain their original stakes, that an investment is accessible, or that any company will outperform. Dates, statuses and valuations have not been refreshed for this presentation. Consult [data quality](reports/DATA_QUALITY.md), [coverage gaps](docs/COVERAGE_GAPS.md) and [validation results](reports/validation_results.json).

## Dataset and documentation

| Resource | Contents |
|---|---|
| [SQLite database](database/elite_graph.sqlite) · [direct download](https://github.com/MoheetBrain/Greensnake/raw/refs/heads/main/database/elite_graph.sqlite) | Complete saved graph: 15 tables, 7,761,920 bytes |
| [All 20 CSV exports](data/exports/) · [inventory and fields](docs/DATA_DICTIONARY.md) | People, companies, relationships, valuations, sources, rankings, networks, backtest, queue and rejections |
| [Raw evidence batches](research/batches/) | Original observations, source summaries, collection notes and unresolved/rejected claims |
| [Tracked people](research/people/people_universe.yaml) · [historical cohort](research/companies/backtest_cohort.yaml) · [checkpoint](research/state.json) | Universe design, winners/failures and research state |
| [Methodology](docs/METHODOLOGY.md) · [collection protocol](docs/COLLECTION_CONTRACT.md) | Existing formulas, evidence requirements, relationship definitions and field rules |
| [Portfolio intersections](reports/PORTFOLIO_INTERSECTIONS.md) | Primary economic-ownership ranking and full backer lists |
| [Executive report](reports/EXECUTIVE_REPORT.md) · [company discovery](reports/COMPANY_DISCOVERY.md) | Existing tier findings and alternative ranking methods |
| [Network analysis](reports/NETWORK_ANALYSIS.md) · [technical/cross-domain analysis](reports/TECHNICAL_AND_CROSSDOMAIN.md) | Correlation, technical-capability and domain-diversity findings |
| [Backtest](reports/BACKTEST.md) · [secondary questions](reports/SECONDARY_QUESTIONS.md) | Historical research, failures and limits |
| [Open work](reports/OPEN_WORK.md) · [coverage gaps](docs/COVERAGE_GAPS.md) | Unresolved questions, rejected claims and collection gaps |
| [Source code](src/greensnake/) · [scripts](scripts/) · [tests](tests/) | Existing computation, query interfaces and invariants |
| [Publication notes](docs/PUBLICATION_NOTES.md) · [snapshot hashes](docs/SNAPSHOT_MANIFEST.json) | Preservation, verification and release status |

## Attribution and licensing

An independently authored project maintained by **[@MoheetBrain](https://github.com/MoheetBrain)**. Original research-workstream provenance is retained; the complete original Git history is preserved privately. Use [CITATION.cff](CITATION.cff) for attribution.

Original software is available under the [MIT License](LICENSE). Original research annotations and original compilation/arrangement are offered under [CC BY 4.0, with the scope and exclusions in the data notice](docs/DATA_LICENSE.md). Third-party articles, source pages, quotations, trademarks and other underlying material remain subject to their own rights; those rights are not granted by this project. Source URLs and attribution are retained.

**Research disclaimer:** a historical, exploratory dataset for inspection and reproducible analysis. Portfolio overlap is not an investment recommendation or evidence of future performance.
