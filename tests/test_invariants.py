"""Invariant tests for the Greensnake pipeline.

Run with:  python3 tests/test_invariants.py
(No pytest dependency -- the whole project runs on the standard library.)
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from greensnake.core import enums                                   # noqa: E402
from greensnake.core.schema import validate_edge, validate_valuation  # noqa: E402
from greensnake.entity_resolution.dedupe import (                   # noqa: E402
    AliasMap, CompanyResolver, tight_key)
from greensnake.graph.correlation import independence_adjusted      # noqa: E402
from greensnake.scoring.people import is_technical_elite            # noqa: E402
from greensnake.valuation.current import assign_tier, staleness     # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        FAILURES.append(f"{name}: {detail}")
        print(f"  FAIL {name}  {detail}")


def src(tier_type="company_press_release", **kw):
    s = {"url": "https://example.com/a", "source_type": tier_type,
         "tier": enums.TIER_OF_SOURCE_TYPE[tier_type], "accessed_date": "2026-09-16",
         "evidence_summary": "The release names the individual among participating "
                             "investors, separately from the institutional leads."}
    s.update(kw)
    return s


def edge(**kw):
    e = {"person_key": "a_b", "company_name": "Example Co",
         "relationship_type": "PERSONAL_ANGEL_INVESTMENT", "investment_vehicle": "personal",
         "verification_status": "CONFIRMED_PRIMARY", "date_verified": "2026-09-16",
         "collected_by": "test", "sources": [src()]}
    e.update(kw)
    return e


print("\n-- enum partition --")
check("overlap classes partition the relationship enum",
      enums.STRICT_TYPES | enums.BROAD_EXTRA_TYPES | enums.INFO_NETWORK_EXTRA_TYPES
      == enums.RELATIONSHIP_TYPES)
check("strict is a subset of broad", enums.STRICT_TYPES < enums.BROAD_TYPES)
check("every relationship type has a weight",
      set(enums.RELATIONSHIP_WEIGHT) == enums.RELATIONSHIP_TYPES)
check("founder equity is weighted below a personal angel cheque",
      enums.RELATIONSHIP_WEIGHT["FOUNDER_EQUITY"]
      < enums.RELATIONSHIP_WEIGHT["PERSONAL_ANGEL_INVESTMENT"],
      "founding is not an act of selection")
check("fund-partner exposure is weighted below controlled-fund exposure",
      enums.RELATIONSHIP_WEIGHT["VC_FUND_PARTNER_INVESTMENT"]
      < enums.RELATIONSHIP_WEIGHT["CONTROLLED_FUND_INVESTMENT"])

print("\n-- the anti-hallucination gate --")
check("an edge with no sources is rejected", bool(validate_edge(edge(sources=[]))))
check("a database-only source cannot confirm an edge",
      any("database" in m for m in validate_edge(edge(sources=[src("crunchbase")]))))
check("CONFIRMED_PRIMARY requires a Tier-1 source",
      any("TIER_1_PRIMARY" in m for m in validate_edge(
          edge(verification_status="CONFIRMED_PRIMARY", sources=[src("techcrunch")]))))
check("CONFIRMED_MULTI_SOURCE requires two distinct URLs",
      any("2 distinct" in m for m in validate_edge(
          edge(verification_status="CONFIRMED_MULTI_SOURCE",
               sources=[src("techcrunch"), src("reuters")]))))
check("a personal investment may not name a fund as its vehicle",
      any("names a fund" in m for m in validate_edge(
          edge(investment_vehicle="Acme Ventures"))))
check("a controlled-fund edge may name a fund",
      not validate_edge(edge(relationship_type="CONTROLLED_FUND_INVESTMENT",
                             investment_vehicle="Acme Ventures")))
check("a well-formed edge passes", not validate_edge(edge()))
check("a guessed-looking date format is rejected",
      bool(validate_edge(edge(investment_date="March 2021"))))
check("a null investment date is accepted", not validate_edge(edge(investment_date=None)))
check("a thin evidence summary is rejected",
      bool(validate_edge(edge(sources=[src(evidence_summary="he invested")]))))
check("a valuation with no source is rejected",
      bool(validate_valuation({"company_name": "X", "valuation_usd": 1e9,
                               "valuation_type": "primary_round_post_money",
                               "valuation_date": "2026-01",
                               "valuation_confidence": "HIGH", "sources": []})))
check("a valuation with no date is rejected",
      bool(validate_valuation({"company_name": "X", "valuation_usd": 1e9,
                               "valuation_type": "primary_round_post_money",
                               "valuation_confidence": "HIGH", "sources": [src()]})))

print("\n-- valuation tiers --")
check("tier boundaries are half-open and disjoint",
      [assign_tier(v) for v in (0, 499e6, 500e6, 999.9e6, 1e9, 4.999e9, 5e9)]
      == ["TIER_A_UNDER_500M", "TIER_A_UNDER_500M", "TIER_B_500M_TO_1B",
          "TIER_B_500M_TO_1B", "TIER_C_1B_TO_5B", "TIER_C_1B_TO_5B", "TIER_D_5B_PLUS"])
check("an unknown valuation is never bucketed", assign_tier(None) == enums.TIER_UNKNOWN)
check("a partial date resolves stale, never fresh",
      staleness("2024", date(2026, 9, 16))[0] == "18_TO_36M")

print("\n-- entity resolution --")
r = CompanyResolver(AliasMap(ROOT / "data" / "company_aliases.yaml"))
ids = {n: r.resolve(n) for n in ["OpenAI", "Open AI", "OpenAI, Inc.", "OpenAI Group PBC"]}
check("OpenAI name variants resolve to one entity", len(set(ids.values())) == 1, str(ids))
check("DeepMind resolves to its canonical name",
      r.resolve("DeepMind") == r.resolve("Google DeepMind"))
check("do-not-merge keeps Figure and Figma distinct",
      r.resolve("Figure") != r.resolve("Figma"))
check("normalisation does not collapse Scale AI into Scale Computing",
      r.resolve("Scale AI") != r.resolve("Scale Computing"))
check("tight_key is whitespace and punctuation insensitive",
      tight_key("Open AI, Inc.") == tight_key("OpenAI"))
check("a leading article does not split an entity",
      r.resolve("Boring Company") == r.resolve("The Boring Company"))
check("a .com suffix does not split an entity",
      r.resolve("Zillow") == r.resolve("Zillow.com"))
check("an 'AI' suffix does not split an entity, in either order",
      r.resolve("Decart") == r.resolve("Decart AI")
      and r.resolve("Medra AI") == r.resolve("Medra"))
check("the AI suffix is a MATCH key, not the entity key",
      tight_key("Open AI") == "openai",
      "stripping it inside normalise_name would collide 'Open AI' with 'Open'")
check("do_not_merge is ENFORCED at resolve time, not merely documented",
      r.resolve("Brilliant") != r.resolve("Brilliant Labs"))
check("a guarded name is not collapsed by the AI match key",
      r.resolve("Hippo") != r.resolve("Hippocratic AI"))

print("\n-- independence adjustment --")
w = {"a": 1.0, "b": 1.0, "c": 1.0}
check("delta=1 reproduces the raw weighted sum",
      abs(independence_adjusted([["a", "b", "c"]], w, 1.0) - 3.0) < 1e-9)
check("delta=0 collapses a network to its strongest voice",
      abs(independence_adjusted([["a", "b", "c"]], w, 0.0) - 1.0) < 1e-9)
check("independent backers are never discounted",
      abs(independence_adjusted([["a"], ["b"], ["c"]], w, 0.35) - 3.0) < 1e-9)
check("a clustered company scores below an independent one with the same raw count",
      independence_adjusted([["a", "b", "c"]], w) < independence_adjusted([["a"], ["b"], ["c"]], w))

print("\n-- technical elite qualification --")
check("a Turing-award-class scientist qualifies",
      is_technical_elite(5, ["RESEARCH_SCIENTIST"]))
check("a band-5 engineer-founder qualifies", is_technical_elite(5, ["FOUNDER_OPERATOR"]))
check("a famous non-technical investor does not",
      not is_technical_elite(2, ["PROFESSIONAL_INVESTOR", "SUPER_ANGEL"]))
check("celebrity alone does not qualify at band 4 without a research archetype",
      not is_technical_elite(4, ["FOUNDER_OPERATOR", "PROFESSIONAL_INVESTOR"]))

print()
if FAILURES:
    print(f"{len(FAILURES)} FAILURE(S):")
    for f in FAILURES:
        print("  -", f)
    raise SystemExit(1)
print("all invariants hold")
