# Data dictionary

Research snapshot: **16 September 2026**. This reference describes the existing SQLite schema and the exact saved CSV headers. No table, field or observation was renamed. The SQL DDL remains in [core/db.py](../src/greensnake/core/db.py); enumerations and weights remain in [core/enums.py](../src/greensnake/core/enums.py).

## Population and denominator reconciliation

| Population | Count | Meaning |
|---|---:|---|
| Canonical companies | 2,188 | Every company entity in `companies`, including entities without confirmed relationships |
| Scored companies | 2,143 | `company_scores`; 45 canonical entities have no confirmed relationship |
| Companies with a selected sourced valuation | 145 | Across all canonical companies; 6.6% of 2,188 |
| Canonical companies without selected valuations | 2,043 | All companies, including 20 unscored companies lacking selected valuations |
| Scored companies with unknown valuation | 2,023 | `tier_unknown.csv`; 94.4% of the scored population |
| Economic-intersection companies | 1,814 | At least one confirmed qualifying economic-ownership relationship |
| Economic-intersection companies with unknown valuation | 1,700 | A subset of 2,023; not inferred to be small |
| Relationship records | 3,239 | 3,205 confirmed + 34 unconfirmed; repeated rounds remain separate records |
| Dated relationships | 581 | 17.9% of all 3,239 relationship records |
| Unresolved / rejected claims | 105 / 67 | Separate tables, excluded from confirmed counts |

The five general tier CSVs total **2,143**, not 2,188. They contain 16 / 3 / 20 / 81 / 2,023 rows for A / B / C / D / unknown. Economic-intersection tiers contain 15 / 3 / 20 / 76 / 1,700 rows. Different denominators explain the different totals without changing data.

## Keys, nulls and metric definitions

- `person_key` identifies a tracked person; `company_id` identifies a canonical company. Retain these keys when joining exports.
- `edge_id` identifies an observation. Count **distinct people**, not edge rows, for overlap. `is_confirmed = 1` is the confirmation filter.
- `sources.parent_kind` selects `edge` or `valuation`; join `parent_id` to the corresponding `edge_id` or `valuation_id`. Multiple source rows can cite the same page.
- SQLite `NULL` and empty exported numeric/date cells mean unknown, not zero. Literal `UNKNOWN` enum values are retained. Some categorical fields are unlabelled.
- Date precision may be year, month or day. Do not invent missing components. USD amounts are numeric; formatted display columns are not a substitute for the numeric field.
- Array/object columns are JSON where documented in the DDL. General ranked CSVs flatten `people_list` into names/details/edge IDs; use the database for the structured representation.
- `PORTFOLIO_INTERSECTION_COUNT` is a report-level name; its CSV column is `number_of_elite_people`. It is not a stored SQL column. `direct_personal_or_founder_count + controlled_family_office_or_fund_count` equals it, with direct taking precedence when one person has both.
- `raw_overlap_count` (`raw_people_count` in general CSVs) includes every confirmed relationship type. `confirmed_person_count_strict` is narrower; `confirmed_person_count_broad` additionally includes controlled vehicles, debt and corporate strategic types. BROAD is not identical to the ownership ranking.
- `weighted_person_score`, `independence_adjusted_score`, `technical_elite_score`, density and momentum fields are derived under existing formulas, not factual ownership counts. Technical classifications and person-weight anchors involve judgement.
- Fields named `current_*`, `best_valuation_*`, `staleness_*` and `current_status` describe the saved snapshot. Valuation types include market cap, financing marks and terminal historical observations; inspect type/date/status together.
- `number_of_billionaire_founders` / `billionaire_founder_count` is an explicitly documented proxy based on founder archetype and capital-flexibility band, not independently sourced net worth.

## SQLite tables and exact fields

### `people` — 190 rows

Tracked public profiles and inclusion rationale; one row per person_key.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `person_key` | TEXT | Primary key |
| `full_name` | TEXT | NOT NULL |
| `also_known_as` | TEXT | Nullable |
| `signal_class` | TEXT | NOT NULL |
| `archetypes` | TEXT | Nullable |
| `domains` | TEXT | Nullable |
| `primary_affiliation` | TEXT | Nullable |
| `country` | TEXT | Nullable |
| `rationale` | TEXT | NOT NULL |
| `profile_source_url` | TEXT | Nullable |
| `added_by` | TEXT | Nullable |
| `date_added` | TEXT | Nullable |

### `people_scores` — 190 rows

Asserted score anchors and derived weights; one row per person_key.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `person_key` | TEXT | Primary key |
| `access_score` | INTEGER | Nullable |
| `technical_intelligence_score` | INTEGER | Nullable |
| `early_stage_track_record` | INTEGER | Nullable |
| `founder_network_score` | INTEGER | Nullable |
| `capital_flexibility` | INTEGER | Nullable |
| `independence_score` | INTEGER | Nullable |
| `investment_visibility` | REAL | Nullable |
| `herding_risk` | REAL | Nullable |
| `general_investment_signal` | REAL | Nullable |
| `domain_information_signal` | TEXT | Nullable |
| `person_weight` | REAL | Nullable |
| `score_method_version` | TEXT | Nullable |
| `rationale` | TEXT | Nullable |

### `companies` — 2,188 rows

Canonical entities, status, sector and descriptive metadata; one row per company_id.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `company_id` | TEXT | Primary key |
| `canonical_name` | TEXT | NOT NULL |
| `former_names` | TEXT | Nullable |
| `aliases` | TEXT | Nullable |
| `website` | TEXT | Nullable |
| `country` | TEXT | Nullable |
| `city` | TEXT | Nullable |
| `industry_primary` | TEXT | Nullable |
| `industry_secondary` | TEXT | Nullable |
| `company_description` | TEXT | Nullable |
| `public_or_private` | TEXT | Nullable |
| `ticker` | TEXT | Nullable |
| `exchange` | TEXT | Nullable |
| `founding_year` | INTEGER | Nullable |
| `founders` | TEXT | Nullable |
| `current_status` | TEXT | Nullable |
| `acquired_status` | TEXT | Nullable |
| `parent_company_id` | TEXT | Nullable |
| `total_funding_usd` | REAL | Nullable |
| `notes` | TEXT | Nullable |
| `added_by` | TEXT | Nullable |
| `date_added` | TEXT | Nullable |

### `company_aliases` — 2,234 rows

Auditable raw/normalised names mapped to a canonical company.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `alias_norm` | TEXT | Primary key |
| `alias_raw` | TEXT | NOT NULL |
| `company_id` | TEXT | NOT NULL |
| `resolved_by` | TEXT | Nullable |
| `note` | TEXT | Nullable |

### `valuations` — 150 rows

Sourced valuation observations; one row per valuation_id, with selection flag is_current_best.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `valuation_id` | TEXT | Primary key |
| `company_id` | TEXT | NOT NULL |
| `valuation_usd` | REAL | NOT NULL |
| `valuation_type` | TEXT | NOT NULL |
| `valuation_date` | TEXT | NOT NULL |
| `valuation_confidence` | TEXT | NOT NULL |
| `share_price` | REAL | Nullable |
| `shares_outstanding` | REAL | Nullable |
| `is_current_best` | INTEGER | NOT NULL |
| `staleness_band` | TEXT | Nullable |
| `staleness_days` | INTEGER | Nullable |
| `notes` | TEXT | Nullable |
| `collected_by` | TEXT | Nullable |

### `funding_rounds` — 0 rows

Funding-round schema; no records in this snapshot.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `round_id` | TEXT | Primary key |
| `company_id` | TEXT | NOT NULL |
| `round_name` | TEXT | Nullable |
| `round_date` | TEXT | Nullable |
| `round_total_usd` | REAL | Nullable |
| `post_money_usd` | REAL | Nullable |
| `lead_investors` | TEXT | Nullable |
| `notes` | TEXT | Nullable |

### `person_company_edges` — 3,239 rows

Investigated relationship records; one row per edge_id. Different rounds may share a person/company pair.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `edge_id` | TEXT | Primary key |
| `person_key` | TEXT | NOT NULL |
| `company_id` | TEXT | NOT NULL |
| `relationship_type` | TEXT | NOT NULL |
| `investment_vehicle` | TEXT | Nullable |
| `investment_date` | TEXT | Nullable |
| `round_name` | TEXT | Nullable |
| `amount_personally_invested_usd` | REAL | Nullable |
| `round_total_usd` | REAL | Nullable |
| `entry_valuation_usd` | REAL | Nullable |
| `entry_valuation_type` | TEXT | Nullable |
| `ownership_percentage` | REAL | Nullable |
| `verification_status` | TEXT | NOT NULL |
| `verification_notes` | TEXT | Nullable |
| `date_verified` | TEXT | NOT NULL |
| `collected_by` | TEXT | Nullable |
| `raw_company_name` | TEXT | Nullable |
| `is_confirmed` | INTEGER | NOT NULL |
| `overlap_class` | TEXT | NOT NULL |
| `edge_weight` | REAL | Nullable |
| `entry_multiple_to_current` | REAL | Nullable |

### `sources` — 4,694 rows

Provenance records; polymorphic parent_kind / parent_id refer to an edge or valuation, not necessarily a unique URL.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `source_id` | TEXT | Primary key |
| `parent_kind` | TEXT | NOT NULL |
| `parent_id` | TEXT | NOT NULL |
| `url` | TEXT | NOT NULL |
| `source_type` | TEXT | NOT NULL |
| `tier` | TEXT | NOT NULL |
| `publisher` | TEXT | Nullable |
| `published_date` | TEXT | Nullable |
| `accessed_date` | TEXT | Nullable |
| `evidence_summary` | TEXT | NOT NULL |
| `url_http_status` | INTEGER | Nullable |
| `url_checked_at` | TEXT | Nullable |
| `url_resolved` | TEXT | Nullable |

### `investor_relationships` — 298 rows

Asserted and derived person–person correlation links, identified by rel_id.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `rel_id` | TEXT | Primary key |
| `person_key_a` | TEXT | NOT NULL |
| `person_key_b` | TEXT | NOT NULL |
| `correlation_type` | TEXT | NOT NULL |
| `strength` | REAL | NOT NULL |
| `evidence` | TEXT | NOT NULL |
| `source_url` | TEXT | Nullable |
| `derived` | INTEGER | NOT NULL |

### `company_scores` — 2,143 rows

Materialised derived metrics for companies with confirmed relationships; one row per company_id.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `company_id` | TEXT | Primary key |
| `best_valuation_usd` | REAL | Nullable |
| `best_valuation_date` | TEXT | Nullable |
| `best_valuation_type` | TEXT | Nullable |
| `best_valuation_confidence` | TEXT | Nullable |
| `staleness_band` | TEXT | Nullable |
| `valuation_tier` | TEXT | NOT NULL |
| `confirmed_person_count_strict` | INTEGER | NOT NULL |
| `confirmed_person_count_broad` | INTEGER | NOT NULL |
| `information_network_count` | INTEGER | NOT NULL |
| `raw_overlap_count` | INTEGER | NOT NULL |
| `weighted_person_score` | REAL | NOT NULL |
| `independence_adjusted_score` | REAL | NOT NULL |
| `independence_adjusted_delta0` | REAL | NOT NULL |
| `independence_adjusted_delta1` | REAL | NOT NULL |
| `distinct_information_clusters` | INTEGER | NOT NULL |
| `number_of_founder_operators` | INTEGER | NOT NULL |
| `number_of_technical_people` | INTEGER | NOT NULL |
| `number_of_professional_investors` | INTEGER | NOT NULL |
| `number_of_billionaire_founders` | INTEGER | NOT NULL |
| `number_of_domain_specialists` | INTEGER | NOT NULL |
| `distinct_domains_represented` | INTEGER | NOT NULL |
| `cross_domain_score` | REAL | NOT NULL |
| `technical_elite_score` | REAL | NOT NULL |
| `best_source_tier` | TEXT | Nullable |
| `technical_elite_count` | INTEGER | NOT NULL |
| `elite_density` | REAL | Nullable |
| `technical_elite_density` | REAL | Nullable |
| `independent_signal_density` | REAL | Nullable |
| `dated_edge_person_count` | INTEGER | NOT NULL |
| `elite_connections_24m_ago` | INTEGER | Nullable |
| `elite_connections_12m_ago` | INTEGER | Nullable |
| `elite_connections_6m_ago` | INTEGER | Nullable |
| `elite_connections_now` | INTEGER | Nullable |
| `elite_network_momentum_12m` | INTEGER | Nullable |
| `elite_network_momentum_6m` | INTEGER | Nullable |
| `earliest_elite_entry_date` | TEXT | Nullable |
| `valuation_at_earliest_elite_entry` | REAL | Nullable |
| `current_to_entry_multiple` | REAL | Nullable |
| `people_list` | TEXT | Nullable |

### `research_queue` — 105 rows

Unresolved claims, sources checked and next evidence to seek; one row per queue_id.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `queue_id` | TEXT | Primary key |
| `claim` | TEXT | NOT NULL |
| `person_key` | TEXT | Nullable |
| `company_name` | TEXT | Nullable |
| `reason_unresolved` | TEXT | NOT NULL |
| `sources_checked` | TEXT | Nullable |
| `next_source_to_check` | TEXT | Nullable |
| `priority` | TEXT | Nullable |
| `raised_by` | TEXT | Nullable |
| `date_raised` | TEXT | Nullable |

### `rejected_edges` — 67 rows

Investigated and rejected claims with reasons; one row per rejected_id.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `rejected_id` | TEXT | Primary key |
| `person_key` | TEXT | Nullable |
| `company_name` | TEXT | Nullable |
| `suspected_relationship` | TEXT | Nullable |
| `reason_rejected` | TEXT | NOT NULL |
| `source_url` | TEXT | Nullable |
| `date_checked` | TEXT | Nullable |
| `rejected_by` | TEXT | Nullable |

### `person_outcomes` — 178 rows

Derived historical outcome coverage; one row per person with confirmed relationships.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `person_key` | TEXT | Primary key |
| `number_verified_investments` | INTEGER | Nullable |
| `number_major_outliers` | INTEGER | Nullable |
| `number_exits` | INTEGER | Nullable |
| `number_failures` | INTEGER | Nullable |
| `number_shutdowns` | INTEGER | Nullable |
| `number_down_rounds` | INTEGER | Nullable |
| `hit_rate_proxy` | REAL | Nullable |
| `early_entry_outlier_score` | REAL | Nullable |
| `disclosure_completeness` | TEXT | Nullable |
| `reliability_caveat` | TEXT | Nullable |

### `backtest_observations` — 300 rows

Historical company/date observations and outcome labels; one row per obs_id.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `obs_id` | TEXT | Primary key |
| `company_id` | TEXT | NOT NULL |
| `as_of_date` | TEXT | NOT NULL |
| `valuation_usd` | REAL | Nullable |
| `elite_people_count` | INTEGER | NOT NULL |
| `people_list` | TEXT | Nullable |
| `outcome_label` | TEXT | Nullable |
| `notes` | TEXT | Nullable |

### `run_metadata` — 3 rows

Saved build date, independence discount and completeness grade, keyed by key.

| Field | SQLite type | Key / constraint |
|---|---|---|
| `key` | TEXT | Primary key |
| `value` | TEXT | Nullable |

## CSV inventory and exact headers

Exports are views and derived screens, not one CSV for each SQL table. The [export implementation](../src/greensnake/reporting/exports.py) and [ownership implementation](../scripts/portfolio_intersections.py) define their filters and ordering.

### [backtest_observations.csv](../data/exports/backtest_observations.csv) — 300 rows

`obs_id`, `company`, `as_of_date`, `valuation_usd`, `elite_people_count`, `people_list`, `outcome_label`, `notes`

### [companies.csv](../data/exports/companies.csv) — 2,188 rows

`company_id`, `canonical_name`, `former_names`, `aliases`, `website`, `country`, `city`, `industry_primary`, `industry_secondary`, `company_description`, `public_or_private`, `ticker`, `exchange`, `founding_year`, `founders`, `current_status`, `acquired_status`, `parent_company_id`, `total_funding_usd`, `notes`, `added_by`, `date_added`

### [company_discovery.csv](../data/exports/company_discovery.csv) — 2,062 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_tier`, `sector`, `public_or_private`, `country`, `raw_people_count`, `strict_people_count`, `technical_elite_count`, `distinct_information_clusters`, `distinct_domains_represented`, `weighted_score`, `independence_adjusted_score`, `cross_domain_score`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `source_quality`, `valuation_confidence`, `staleness_band`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [company_overlap_scores.csv](../data/exports/company_overlap_scores.csv) — 2,143 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_type`, `valuation_confidence`, `staleness_band`, `valuation_tier`, `public_or_private`, `ticker`, `country`, `sector`, `current_status`, `raw_people_count`, `strict_people_count`, `broad_people_count`, `information_network_count`, `weighted_score`, `independence_adjusted_score`, `independence_adjusted_delta0`, `independence_adjusted_delta1`, `distinct_information_clusters`, `distinct_domains_represented`, `cross_domain_score`, `technical_elite_count`, `technical_elite_score`, `number_of_founder_operators`, `number_of_professional_investors`, `number_of_domain_specialists`, `number_of_billionaire_founders`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `dated_edge_person_count`, `elite_connections_24m_ago`, `elite_connections_12m_ago`, `elite_connections_6m_ago`, `elite_connections_now`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `source_quality`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [edges_confirmed.csv](../data/exports/edges_confirmed.csv) — 3,205 rows

`edge_id`, `person_key`, `person_name`, `company_id`, `company`, `raw_company_name`, `relationship_type`, `overlap_class`, `investment_vehicle`, `investment_date`, `round_name`, `amount_personally_invested_usd`, `round_total_usd`, `entry_valuation_usd`, `entry_valuation_type`, `ownership_percentage`, `entry_multiple_to_current`, `verification_status`, `verification_notes`, `date_verified`, `collected_by`, `edge_weight`, `source_urls`, `source_types`, `source_tiers`, `evidence_summaries`

### [edges_unverified.csv](../data/exports/edges_unverified.csv) — 34 rows

`edge_id`, `person_key`, `person_name`, `company_id`, `company`, `raw_company_name`, `relationship_type`, `overlap_class`, `investment_vehicle`, `investment_date`, `round_name`, `amount_personally_invested_usd`, `round_total_usd`, `entry_valuation_usd`, `entry_valuation_type`, `ownership_percentage`, `entry_multiple_to_current`, `verification_status`, `verification_notes`, `date_verified`, `collected_by`, `edge_weight`, `source_urls`, `source_types`, `source_tiers`, `evidence_summaries`

### [people.csv](../data/exports/people.csv) — 190 rows

`person_key`, `full_name`, `signal_class`, `primary_affiliation`, `country`, `archetypes`, `domains`, `access_score`, `technical_intelligence_score`, `early_stage_track_record`, `founder_network_score`, `capital_flexibility`, `independence_score`, `investment_visibility`, `herding_risk`, `general_investment_signal`, `domain_information_signal`, `person_weight`, `score_method_version`, `rationale`, `added_by`

### [person_person_network.csv](../data/exports/person_person_network.csv) — 298 rows

`rel_id`, `person_key_a`, `name_a`, `person_key_b`, `name_b`, `correlation_type`, `strength`, `derived`, `evidence`, `source_url`

### [person_scorecard.csv](../data/exports/person_scorecard.csv) — 190 rows

`person_key`, `name`, `primary_and_secondary_domains`, `role`, `signal_class`, `estimated_access_score`, `technical_information_score`, `historical_earliness_score`, `verified_investment_count`, `verified_major_outlier_count`, `failure_count_if_known`, `hit_rate_proxy`, `disclosure_completeness`, `visibility_score`, `herding_risk`, `independence_score`, `general_investment_signal`, `domain_information_signal`, `person_weight`, `confidence`, `reason_for_inclusion`

### [portfolio_intersections.csv](../data/exports/portfolio_intersections.csv) — 1,814 rows

`rank`, `company`, `number_of_elite_people`, `direct_personal_or_founder_count`, `controlled_family_office_or_fund_count`, `vc_partner_exposure_count`, `total_incl_vc_partner`, `names_of_every_person`, `public_or_private`, `ticker`, `current_valuation_if_known`, `current_valuation_usd`, `valuation_date`, `valuation_type`, `valuation_staleness`, `valuation_confidence`, `valuation_tier`, `sector`, `country`, `status`, `source_confidence`, `technical_elite_count`, `billionaire_founder_count`, `frontier_ai_count`, `distinct_primary_domains`, `technical_elite_names`, `weighted_score_secondary`, `independence_adjusted_secondary`, `distinct_networks_secondary`, `company_id`

### [recent_entries.csv](../data/exports/recent_entries.csv) — 580 rows

`investment_date`, `company`, `valuation_tier`, `valuation_usd`, `person`, `signal_class`, `relationship_type`, `overlap_class`, `raw_overlap_count`, `edge_id`, `company_id`

### [rejected_edges.csv](../data/exports/rejected_edges.csv) — 67 rows

`rejected_id`, `person_key`, `company_name`, `suspected_relationship`, `reason_rejected`, `source_url`, `date_checked`, `rejected_by`

### [research_queue.csv](../data/exports/research_queue.csv) — 105 rows

`queue_id`, `claim`, `person_key`, `company_name`, `reason_unresolved`, `sources_checked`, `next_source_to_check`, `priority`, `raised_by`, `date_raised`

### [sources.csv](../data/exports/sources.csv) — 4,694 rows

`source_id`, `parent_kind`, `parent_id`, `url`, `source_type`, `tier`, `publisher`, `published_date`, `accessed_date`, `url_http_status`, `url_checked_at`, `evidence_summary`

### [tier_1b_to_5b.csv](../data/exports/tier_1b_to_5b.csv) — 20 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_type`, `valuation_confidence`, `staleness_band`, `valuation_tier`, `public_or_private`, `ticker`, `country`, `sector`, `current_status`, `raw_people_count`, `strict_people_count`, `broad_people_count`, `information_network_count`, `weighted_score`, `independence_adjusted_score`, `independence_adjusted_delta0`, `independence_adjusted_delta1`, `distinct_information_clusters`, `distinct_domains_represented`, `cross_domain_score`, `technical_elite_count`, `technical_elite_score`, `number_of_founder_operators`, `number_of_professional_investors`, `number_of_domain_specialists`, `number_of_billionaire_founders`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `dated_edge_person_count`, `elite_connections_24m_ago`, `elite_connections_12m_ago`, `elite_connections_6m_ago`, `elite_connections_now`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `source_quality`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [tier_500m_to_1b.csv](../data/exports/tier_500m_to_1b.csv) — 3 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_type`, `valuation_confidence`, `staleness_band`, `valuation_tier`, `public_or_private`, `ticker`, `country`, `sector`, `current_status`, `raw_people_count`, `strict_people_count`, `broad_people_count`, `information_network_count`, `weighted_score`, `independence_adjusted_score`, `independence_adjusted_delta0`, `independence_adjusted_delta1`, `distinct_information_clusters`, `distinct_domains_represented`, `cross_domain_score`, `technical_elite_count`, `technical_elite_score`, `number_of_founder_operators`, `number_of_professional_investors`, `number_of_domain_specialists`, `number_of_billionaire_founders`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `dated_edge_person_count`, `elite_connections_24m_ago`, `elite_connections_12m_ago`, `elite_connections_6m_ago`, `elite_connections_now`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `source_quality`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [tier_over_5b.csv](../data/exports/tier_over_5b.csv) — 81 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_type`, `valuation_confidence`, `staleness_band`, `valuation_tier`, `public_or_private`, `ticker`, `country`, `sector`, `current_status`, `raw_people_count`, `strict_people_count`, `broad_people_count`, `information_network_count`, `weighted_score`, `independence_adjusted_score`, `independence_adjusted_delta0`, `independence_adjusted_delta1`, `distinct_information_clusters`, `distinct_domains_represented`, `cross_domain_score`, `technical_elite_count`, `technical_elite_score`, `number_of_founder_operators`, `number_of_professional_investors`, `number_of_domain_specialists`, `number_of_billionaire_founders`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `dated_edge_person_count`, `elite_connections_24m_ago`, `elite_connections_12m_ago`, `elite_connections_6m_ago`, `elite_connections_now`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `source_quality`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [tier_under_500m.csv](../data/exports/tier_under_500m.csv) — 16 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_type`, `valuation_confidence`, `staleness_band`, `valuation_tier`, `public_or_private`, `ticker`, `country`, `sector`, `current_status`, `raw_people_count`, `strict_people_count`, `broad_people_count`, `information_network_count`, `weighted_score`, `independence_adjusted_score`, `independence_adjusted_delta0`, `independence_adjusted_delta1`, `distinct_information_clusters`, `distinct_domains_represented`, `cross_domain_score`, `technical_elite_count`, `technical_elite_score`, `number_of_founder_operators`, `number_of_professional_investors`, `number_of_domain_specialists`, `number_of_billionaire_founders`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `dated_edge_person_count`, `elite_connections_24m_ago`, `elite_connections_12m_ago`, `elite_connections_6m_ago`, `elite_connections_now`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `source_quality`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [tier_unknown.csv](../data/exports/tier_unknown.csv) — 2,023 rows

`company_id`, `company`, `valuation_usd`, `valuation_date`, `valuation_type`, `valuation_confidence`, `staleness_band`, `valuation_tier`, `public_or_private`, `ticker`, `country`, `sector`, `current_status`, `raw_people_count`, `strict_people_count`, `broad_people_count`, `information_network_count`, `weighted_score`, `independence_adjusted_score`, `independence_adjusted_delta0`, `independence_adjusted_delta1`, `distinct_information_clusters`, `distinct_domains_represented`, `cross_domain_score`, `technical_elite_count`, `technical_elite_score`, `number_of_founder_operators`, `number_of_professional_investors`, `number_of_domain_specialists`, `number_of_billionaire_founders`, `elite_density`, `technical_elite_density`, `independent_signal_density`, `dated_edge_person_count`, `elite_connections_24m_ago`, `elite_connections_12m_ago`, `elite_connections_6m_ago`, `elite_connections_now`, `elite_network_momentum_12m`, `elite_network_momentum_6m`, `earliest_elite_entry_date`, `valuation_at_earliest_elite_entry`, `current_to_entry_multiple`, `source_quality`, `names_of_people`, `people_detail`, `technical_elite_names`, `edge_ids`

### [valuations.csv](../data/exports/valuations.csv) — 150 rows

`valuation_id`, `company_id`, `company`, `valuation_usd`, `valuation_type`, `valuation_date`, `valuation_confidence`, `staleness_band`, `staleness_days`, `is_current_best`, `share_price`, `shares_outstanding`, `notes`, `collected_by`, `source_urls`, `evidence`

## Evidence and research files

[research/batches/](../research/batches/) preserves JSONL observations, source summaries, queue and rejection records, plus workstream notes. [COLLECTION_CONTRACT.md](COLLECTION_CONTRACT.md) defines their fields. [research/state.json](../research/state.json) is the original progress checkpoint. [company_aliases.yaml](../data/company_aliases.yaml) preserves explicit merges and do-not-merge guards. [processed records](../data/processed/) retain ingest rejects and the historical URL-liveness cache.
