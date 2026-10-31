"""Controlled vocabularies for the Greensnake elite-capital intelligence graph.

Single source of truth. Every collector (human or agent) writes into these
enums. Anything outside them is rejected at ingest, never silently coerced.
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# Relationship types (STEP 2 of the research contract)
# --------------------------------------------------------------------------
RELATIONSHIP_TYPES = {
    # --- direct, personal economic exposure -------------------------------
    "PERSONAL_ANGEL_INVESTMENT",   # named individual angel in a financing round
    "PERSONAL_EQUITY_INVESTMENT",  # personal purchase of equity (incl. secondary)
    "FOUNDER_EQUITY",              # founded / co-founded -> founder shares
    "SPV_INVESTMENT",              # committed personal capital via a disclosed SPV
    # --- controlled vehicles ---------------------------------------------
    "FAMILY_OFFICE_INVESTMENT",    # their family office / personal holding co
    "CONTROLLED_FUND_INVESTMENT",  # fund they founded / control (eponymous GP)
    "CORPORATE_STRATEGIC_INVESTMENT",  # a corporate they control invested
    "DEBT_FINANCING",              # personally / via controlled vehicle lent money
    # --- informational / non-economic ------------------------------------
    "VC_FUND_PARTNER_INVESTMENT",  # firm they are a partner at (but do NOT control)
    "BOARD_ONLY",                  # board seat, no verified investment
    "ADVISOR_ONLY",                # advisor/advisory shares unverified
    "LP_INDIRECT",                 # LP in a fund that invested
    # --- non-equity capital ----------------------------------------------
    "GRANT_FUNDING",
    "PHILANTHROPIC_FUNDING",
    # --- escape hatch -----------------------------------------------------
    "OTHER_VERIFIED",
}

# Which relationship types roll up into which overlap definition.
# These three sets are nested: STRICT subset of BROAD subset of INFO_NETWORK.
STRICT_TYPES = {
    "PERSONAL_ANGEL_INVESTMENT",
    "PERSONAL_EQUITY_INVESTMENT",
    "FOUNDER_EQUITY",
    "SPV_INVESTMENT",
}
BROAD_EXTRA_TYPES = {
    "FAMILY_OFFICE_INVESTMENT",
    "CONTROLLED_FUND_INVESTMENT",
    "CORPORATE_STRATEGIC_INVESTMENT",
    "DEBT_FINANCING",
}
INFO_NETWORK_EXTRA_TYPES = {
    "VC_FUND_PARTNER_INVESTMENT",
    "BOARD_ONLY",
    "ADVISOR_ONLY",
    "LP_INDIRECT",
    "GRANT_FUNDING",
    "PHILANTHROPIC_FUNDING",
    "OTHER_VERIFIED",
}
BROAD_TYPES = STRICT_TYPES | BROAD_EXTRA_TYPES
INFO_NETWORK_TYPES = BROAD_TYPES | INFO_NETWORK_EXTRA_TYPES

assert RELATIONSHIP_TYPES == INFO_NETWORK_TYPES, "enum partition drift"

# Relationship weight used in weighted overlap. Expresses "how much economic +
# informational signal does this edge carry", NOT "how likely is it true"
# (that is verification_status' job, applied as a separate multiplier).
RELATIONSHIP_WEIGHT = {
    "PERSONAL_ANGEL_INVESTMENT": 1.00,
    "PERSONAL_EQUITY_INVESTMENT": 1.00,
    "FOUNDER_EQUITY": 0.90,   # high info, but founding is not a selection signal
    "SPV_INVESTMENT": 0.90,
    "FAMILY_OFFICE_INVESTMENT": 0.85,
    "CONTROLLED_FUND_INVESTMENT": 0.70,
    "CORPORATE_STRATEGIC_INVESTMENT": 0.45,
    "DEBT_FINANCING": 0.40,
    "VC_FUND_PARTNER_INVESTMENT": 0.35,
    "BOARD_ONLY": 0.30,
    "ADVISOR_ONLY": 0.20,
    "LP_INDIRECT": 0.10,
    "GRANT_FUNDING": 0.15,
    "PHILANTHROPIC_FUNDING": 0.10,
    "OTHER_VERIFIED": 0.25,
}

# --------------------------------------------------------------------------
# Verification (STEP 3)
# --------------------------------------------------------------------------
VERIFICATION_STATUSES = {
    "CONFIRMED_PRIMARY",
    "CONFIRMED_MULTI_SOURCE",
    "CONFIRMED_REPUTABLE_SECONDARY",
    "PROBABLE_BUT_NOT_CONFIRMED",
    "CONFLICTING_EVIDENCE",
    "UNVERIFIED",
    "REJECTED",
}
# Only these enter the principal confirmed-overlap calculations.
CONFIRMED_STATUSES = {
    "CONFIRMED_PRIMARY",
    "CONFIRMED_MULTI_SOURCE",
    "CONFIRMED_REPUTABLE_SECONDARY",
}
# Evidence-strength multiplier applied on top of relationship weight.
STATUS_WEIGHT = {
    "CONFIRMED_PRIMARY": 1.00,
    "CONFIRMED_MULTI_SOURCE": 1.00,
    "CONFIRMED_REPUTABLE_SECONDARY": 0.85,
}

SOURCE_TIERS = {"TIER_1_PRIMARY", "TIER_2_SECONDARY", "TIER_3_DATABASE"}

SOURCE_TYPES = {
    # TIER 1
    "sec_filing", "companies_house_filing", "other_regulatory_filing",
    "company_press_release", "official_funding_announcement",
    "company_website", "investor_portfolio_page", "personal_website", "shareholder_disclosure",
    "prospectus", "annual_report", "acquisition_document", "court_document",
    "official_interview_or_statement", "government_award_record",
    # TIER 2
    "financial_times", "bloomberg", "reuters", "wall_street_journal", "cnbc",
    "forbes_original_reporting", "fortune", "the_information", "techcrunch",
    "axios", "business_insider", "specialist_trade_press", "other_reputable_press",
    "market_data_provider",
    # TIER 3
    "crunchbase", "pitchbook", "dealroom", "tracxn", "cb_insights",
    "harmonic", "wellfound", "other_private_market_database",
}
TIER_OF_SOURCE_TYPE = {}
for _t in ("sec_filing", "companies_house_filing", "other_regulatory_filing",
           "company_press_release", "official_funding_announcement",
           "company_website", "investor_portfolio_page", "personal_website", "shareholder_disclosure",
           "prospectus", "annual_report", "acquisition_document", "court_document",
           "official_interview_or_statement", "government_award_record"):
    TIER_OF_SOURCE_TYPE[_t] = "TIER_1_PRIMARY"
for _t in ("financial_times", "bloomberg", "reuters", "wall_street_journal", "cnbc",
           "forbes_original_reporting", "fortune", "the_information", "techcrunch",
           "axios", "business_insider", "specialist_trade_press", "other_reputable_press",
           "market_data_provider"):
    TIER_OF_SOURCE_TYPE[_t] = "TIER_2_SECONDARY"
for _t in ("crunchbase", "pitchbook", "dealroom", "tracxn", "cb_insights",
           "harmonic", "wellfound", "other_private_market_database"):
    TIER_OF_SOURCE_TYPE[_t] = "TIER_3_DATABASE"

# Sources that can never, on their own, confirm an edge.
NON_CONFIRMING_SOURCE_TYPES = set(
    t for t, tier in TIER_OF_SOURCE_TYPE.items() if tier == "TIER_3_DATABASE"
)

# --------------------------------------------------------------------------
# Valuation (STEP 5 / STEP 6)
# --------------------------------------------------------------------------
VALUATION_TYPES = {
    "public_market_cap",
    "primary_round_post_money",
    "primary_round_pre_money",
    "tender_or_secondary",
    "acquisition_price",
    "reported_valuation",      # credible reporting, no round disclosed
    "shut_down_zero",          # company dead -> valuation 0
}
VALUATION_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}

# Mutually exclusive buckets over the best current defensible valuation (USD).
TIER_BOUNDS = [
    ("TIER_A_UNDER_500M", 0.0, 500_000_000.0),
    ("TIER_B_500M_TO_1B", 500_000_000.0, 1_000_000_000.0),
    ("TIER_C_1B_TO_5B", 1_000_000_000.0, 5_000_000_000.0),
    ("TIER_D_5B_PLUS", 5_000_000_000.0, float("inf")),
]
TIER_UNKNOWN = "TIER_U_UNKNOWN"

STALENESS_BANDS = [
    ("LT_6M", 0, 183),
    ("6_TO_12M", 183, 366),
    ("12_TO_18M", 366, 549),
    ("18_TO_36M", 549, 1096),
    ("GT_36M", 1096, 10**9),
]

# --------------------------------------------------------------------------
# People (DO NOT STOP AT THE FIRST 100 PEOPLE)
# --------------------------------------------------------------------------
PERSON_SIGNAL_CLASSES = {
    "CORE_HIGH_SIGNAL",
    "EXTENDED_SIGNAL",
    "DOMAIN_SPECIALIST",
    "WATCHLIST",
    "LOW_SIGNAL_OR_POOR_VISIBILITY",
}
PERSON_CLASS_WEIGHT = {
    "CORE_HIGH_SIGNAL": 1.00,
    "EXTENDED_SIGNAL": 0.70,
    "DOMAIN_SPECIALIST": 0.60,
    "WATCHLIST": 0.35,
    "LOW_SIGNAL_OR_POOR_VISIBILITY": 0.15,
}

DOMAINS = {
    "AI_SOFTWARE", "SEMICONDUCTORS", "ENERGY_CLIMATE", "INDUSTRIAL_DEEPTECH",
    "BIOTECH_LIFESCIENCES", "SPACE", "DEFENCE", "ROBOTICS", "FINTECH",
    "CONSUMER_INTERNET", "CRYPTO", "MATERIALS", "QUANTUM", "HEALTHCARE_SERVICES",
    "AGRICULTURE_FOOD", "TRANSPORT_MOBILITY", "GENERALIST",
}

PERSON_ARCHETYPES = {
    "FOUNDER_OPERATOR", "RESEARCH_SCIENTIST", "PROFESSIONAL_INVESTOR",
    "SUPER_ANGEL", "CORPORATE_EXECUTIVE", "FAMILY_OFFICE_PRINCIPAL",
    "ACADEMIC", "POLICY_OR_GOVERNMENT",
}

# Ordinal 0-5 score components. Anchors are documented in METHODOLOGY.md.
SCORE_COMPONENTS_ASSERTED = [
    "access_score",
    "technical_intelligence_score",
    "early_stage_track_record",
    "founder_network_score",
    "capital_flexibility",
    "independence_score",
]
SCORE_COMPONENTS_DERIVED = [
    "investment_visibility",   # from edge count + source tier mix in THIS graph
    "herding_risk",            # from co-investment concentration in THIS graph
]
SCORE_MIN, SCORE_MAX = 0, 5

# --------------------------------------------------------------------------
# Investor correlation (CRITICAL: CORRELATED NETWORKS)
# --------------------------------------------------------------------------
CORRELATION_TYPES = {
    "SAME_FIRM",
    "SAME_FORMER_EMPLOYER",
    "SAME_BOARD",
    "CO_FOUNDED_COMPANY",
    "FAMILY_RELATIONSHIP",
    "SAME_ACCELERATOR",
    "SAME_SYNDICATE",
    "FREQUENT_CO_INVESTMENT",
    "SAME_FOUNDER_ECOSYSTEM",
    "SAME_INSTITUTIONAL_SOURCE",
}
# Strength of the correlation link, 0-1. Used to build clusters.
CORRELATION_STRENGTH_DEFAULT = {
    "SAME_FIRM": 0.90,
    "CO_FOUNDED_COMPANY": 0.85,
    "FAMILY_RELATIONSHIP": 0.85,
    "SAME_SYNDICATE": 0.70,
    "SAME_FORMER_EMPLOYER": 0.55,
    "SAME_FOUNDER_ECOSYSTEM": 0.50,
    "SAME_ACCELERATOR": 0.50,
    "SAME_BOARD": 0.45,
    "FREQUENT_CO_INVESTMENT": 0.45,
    "SAME_INSTITUTIONAL_SOURCE": 0.40,
}

COMPANY_STATUSES = {
    "OPERATING_PRIVATE", "OPERATING_PUBLIC", "ACQUIRED", "MERGED",
    "SHUT_DOWN", "BANKRUPT", "UNKNOWN",
}
