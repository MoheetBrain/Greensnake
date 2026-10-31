"""SQLite schema for elite_graph.sqlite.

Design rules:
  * Every derived number must be traceable back to an edge, and every edge back
    to a source row. `sources` is therefore its own table keyed by edge/valuation.
  * Nothing is stored as a bare string where an enum exists -- CHECK constraints
    make a schema violation a hard failure at write time, not a silent one.
  * Ranking tables are materialised views recomputed from scratch on every run
    so they can never drift from the edges underneath them.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

DDL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS people (
    person_key            TEXT PRIMARY KEY,
    full_name             TEXT NOT NULL,
    also_known_as         TEXT,
    signal_class          TEXT NOT NULL,
    archetypes            TEXT,            -- JSON array
    domains               TEXT,            -- JSON array
    primary_affiliation   TEXT,
    country               TEXT,
    rationale             TEXT NOT NULL,
    profile_source_url    TEXT,
    added_by              TEXT,
    date_added            TEXT
);

CREATE TABLE IF NOT EXISTS people_scores (
    person_key                   TEXT PRIMARY KEY REFERENCES people(person_key),
    access_score                 INTEGER,
    technical_intelligence_score INTEGER,
    early_stage_track_record     INTEGER,
    founder_network_score        INTEGER,
    capital_flexibility          INTEGER,
    independence_score           INTEGER,
    investment_visibility        REAL,     -- DERIVED from this graph
    herding_risk                 REAL,     -- DERIVED from this graph
    general_investment_signal    REAL,
    domain_information_signal    TEXT,     -- JSON {domain: score}
    person_weight                REAL,     -- final weight used in scoring
    score_method_version         TEXT,
    rationale                    TEXT
);

CREATE TABLE IF NOT EXISTS companies (
    company_id                    TEXT PRIMARY KEY,
    canonical_name                TEXT NOT NULL,
    former_names                  TEXT,   -- JSON array
    aliases                       TEXT,   -- JSON array
    website                       TEXT,
    country                       TEXT,
    city                          TEXT,
    industry_primary              TEXT,
    industry_secondary            TEXT,
    company_description           TEXT,
    public_or_private             TEXT,
    ticker                        TEXT,
    exchange                      TEXT,
    founding_year                 INTEGER,
    founders                      TEXT,   -- JSON array
    current_status                TEXT,
    acquired_status               TEXT,
    parent_company_id             TEXT REFERENCES companies(company_id),
    total_funding_usd             REAL,
    notes                         TEXT,
    added_by                      TEXT,
    date_added                    TEXT
);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(canonical_name);

-- Alias -> canonical resolution table. Makes dedupe auditable rather than magic.
CREATE TABLE IF NOT EXISTS company_aliases (
    alias_norm   TEXT PRIMARY KEY,
    alias_raw    TEXT NOT NULL,
    company_id   TEXT NOT NULL REFERENCES companies(company_id),
    resolved_by  TEXT,
    note         TEXT
);

CREATE TABLE IF NOT EXISTS valuations (
    valuation_id          TEXT PRIMARY KEY,
    company_id            TEXT NOT NULL REFERENCES companies(company_id),
    valuation_usd         REAL NOT NULL,
    valuation_type        TEXT NOT NULL,
    valuation_date        TEXT NOT NULL,
    valuation_confidence  TEXT NOT NULL,
    share_price           REAL,
    shares_outstanding    REAL,
    is_current_best       INTEGER NOT NULL DEFAULT 0,
    staleness_band        TEXT,
    staleness_days        INTEGER,
    notes                 TEXT,
    collected_by          TEXT
);
CREATE INDEX IF NOT EXISTS idx_val_company ON valuations(company_id);

CREATE TABLE IF NOT EXISTS funding_rounds (
    round_id        TEXT PRIMARY KEY,
    company_id      TEXT NOT NULL REFERENCES companies(company_id),
    round_name      TEXT,
    round_date      TEXT,
    round_total_usd REAL,
    post_money_usd  REAL,
    lead_investors  TEXT,
    notes           TEXT
);

CREATE TABLE IF NOT EXISTS person_company_edges (
    edge_id                         TEXT PRIMARY KEY,
    person_key                      TEXT NOT NULL REFERENCES people(person_key),
    company_id                      TEXT NOT NULL REFERENCES companies(company_id),
    relationship_type               TEXT NOT NULL,
    investment_vehicle              TEXT,
    investment_date                 TEXT,
    round_name                      TEXT,
    amount_personally_invested_usd  REAL,
    round_total_usd                 REAL,
    entry_valuation_usd             REAL,
    entry_valuation_type            TEXT,
    ownership_percentage            REAL,
    verification_status             TEXT NOT NULL,
    verification_notes              TEXT,
    date_verified                   TEXT NOT NULL,
    collected_by                    TEXT,
    raw_company_name                TEXT,
    is_confirmed                    INTEGER NOT NULL,
    overlap_class                   TEXT NOT NULL,  -- STRICT | BROAD | INFO_NETWORK
    edge_weight                     REAL,
    entry_multiple_to_current       REAL,
    CHECK (overlap_class IN ('STRICT','BROAD','INFO_NETWORK'))
);
CREATE INDEX IF NOT EXISTS idx_edges_company ON person_company_edges(company_id);
CREATE INDEX IF NOT EXISTS idx_edges_person ON person_company_edges(person_key);
CREATE UNIQUE INDEX IF NOT EXISTS idx_edges_natural ON person_company_edges(
    person_key, company_id, relationship_type,
    COALESCE(investment_date,''), COALESCE(round_name,''));

CREATE TABLE IF NOT EXISTS sources (
    source_id         TEXT PRIMARY KEY,
    parent_kind       TEXT NOT NULL,   -- 'edge' | 'valuation' | 'company' | 'correlation'
    parent_id         TEXT NOT NULL,
    url               TEXT NOT NULL,
    source_type       TEXT NOT NULL,
    tier              TEXT NOT NULL,
    publisher         TEXT,
    published_date    TEXT,
    accessed_date     TEXT,
    evidence_summary  TEXT NOT NULL,
    url_http_status   INTEGER,         -- filled by the liveness checker
    url_checked_at    TEXT,
    url_resolved      TEXT              -- the variant that actually resolves, if
                                        -- it differs from the cited URL. The cited
                                        -- URL is never overwritten.
);
CREATE INDEX IF NOT EXISTS idx_sources_parent ON sources(parent_kind, parent_id);

CREATE TABLE IF NOT EXISTS investor_relationships (
    rel_id           TEXT PRIMARY KEY,
    person_key_a     TEXT NOT NULL REFERENCES people(person_key),
    person_key_b     TEXT NOT NULL REFERENCES people(person_key),
    correlation_type TEXT NOT NULL,
    strength         REAL NOT NULL,
    evidence         TEXT NOT NULL,
    source_url       TEXT,
    derived          INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS company_scores (
    company_id                       TEXT PRIMARY KEY REFERENCES companies(company_id),
    best_valuation_usd               REAL,
    best_valuation_date              TEXT,
    best_valuation_type              TEXT,
    best_valuation_confidence        TEXT,
    staleness_band                   TEXT,
    valuation_tier                   TEXT NOT NULL,
    confirmed_person_count_strict    INTEGER NOT NULL,
    confirmed_person_count_broad     INTEGER NOT NULL,
    information_network_count        INTEGER NOT NULL,
    raw_overlap_count                INTEGER NOT NULL,
    weighted_person_score            REAL NOT NULL,
    independence_adjusted_score      REAL NOT NULL,
    independence_adjusted_delta0     REAL NOT NULL,
    independence_adjusted_delta1     REAL NOT NULL,
    distinct_information_clusters    INTEGER NOT NULL,
    number_of_founder_operators      INTEGER NOT NULL,
    number_of_technical_people       INTEGER NOT NULL,
    number_of_professional_investors INTEGER NOT NULL,
    number_of_billionaire_founders   INTEGER NOT NULL,
    number_of_domain_specialists     INTEGER NOT NULL,
    distinct_domains_represented     INTEGER NOT NULL,
    cross_domain_score               REAL NOT NULL,
    technical_elite_score            REAL NOT NULL,
    best_source_tier                 TEXT,
    technical_elite_count            INTEGER NOT NULL DEFAULT 0,
    -- exploratory density metrics (NOT proven predictors; inputs preserved)
    elite_density                    REAL,
    technical_elite_density          REAL,
    independent_signal_density       REAL,
    -- temporal: computed ONLY from edges carrying a real investment_date
    dated_edge_person_count          INTEGER NOT NULL DEFAULT 0,
    elite_connections_24m_ago        INTEGER,
    elite_connections_12m_ago        INTEGER,
    elite_connections_6m_ago         INTEGER,
    elite_connections_now            INTEGER,
    elite_network_momentum_12m       INTEGER,
    elite_network_momentum_6m        INTEGER,
    earliest_elite_entry_date        TEXT,
    valuation_at_earliest_elite_entry REAL,
    current_to_entry_multiple        REAL,
    people_list                      TEXT       -- JSON [{person_key, relationship_type, ...}]
);

CREATE TABLE IF NOT EXISTS research_queue (
    queue_id          TEXT PRIMARY KEY,
    claim             TEXT NOT NULL,
    person_key        TEXT,
    company_name      TEXT,
    reason_unresolved TEXT NOT NULL,
    sources_checked   TEXT,
    next_source_to_check TEXT,
    priority          TEXT,
    raised_by         TEXT,
    date_raised       TEXT
);

CREATE TABLE IF NOT EXISTS rejected_edges (
    rejected_id            TEXT PRIMARY KEY,
    person_key             TEXT,
    company_name           TEXT,
    suspected_relationship TEXT,
    reason_rejected        TEXT NOT NULL,
    source_url             TEXT,
    date_checked           TEXT,
    rejected_by            TEXT
);

CREATE TABLE IF NOT EXISTS person_outcomes (
    person_key               TEXT PRIMARY KEY REFERENCES people(person_key),
    number_verified_investments INTEGER,
    number_major_outliers    INTEGER,
    number_exits             INTEGER,
    number_failures          INTEGER,
    number_shutdowns         INTEGER,
    number_down_rounds       INTEGER,
    hit_rate_proxy           REAL,
    early_entry_outlier_score REAL,
    disclosure_completeness  TEXT,
    reliability_caveat       TEXT
);

CREATE TABLE IF NOT EXISTS backtest_observations (
    obs_id             TEXT PRIMARY KEY,
    company_id         TEXT NOT NULL REFERENCES companies(company_id),
    as_of_date         TEXT NOT NULL,
    valuation_usd      REAL,
    elite_people_count INTEGER NOT NULL,
    people_list        TEXT,
    outcome_label      TEXT,      -- WINNER | MEDIOCRE | FAILURE | UNRESOLVED
    notes              TEXT
);

CREATE TABLE IF NOT EXISTS run_metadata (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_db(path: str | Path, fresh: bool = False) -> sqlite3.Connection:
    p = Path(path)
    if fresh and p.exists():
        p.unlink()
    con = connect(p)
    con.executescript(DDL)
    con.commit()
    return con
