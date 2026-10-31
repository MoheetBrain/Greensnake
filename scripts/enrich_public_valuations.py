#!/usr/bin/env python3
"""Turn verified ticker->market-cap lookups into sourced valuation records.

Market data arrives through an MCP financial-data tool, which only the
orchestrating agent can call, so this script is the deterministic half: it takes
a JSON file of already-verified lookups and emits contract-conforming
valuation + company records.

    python3 scripts/enrich_public_valuations.py data/processed/market_caps.json

SAFETY. Attaching a market cap to the wrong company is exactly the kind of
silent error this project exists to prevent, so a lookup is only accepted when
the provider's company name normalises to the SAME tight key as our canonical
name (or the caller explicitly set "name_match_override" with a reason).
Rejected lookups are reported, never quietly dropped.

Input format:
[{"company_name": "Editas Medicine", "provider_name": "Editas Medicine, Inc.",
  "symbol": "EDIT", "exchange": "NASDAQ", "market_cap": 123456789,
  "as_of": "2026-09-16", "share_price": 1.23, "shares_outstanding": 1000000,
  "provider": "Financial Modeling Prep"}]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from greensnake.entity_resolution.dedupe import tight_key  # noqa: E402

OUT_DIR = ROOT / "research" / "batches" / "orchestrator"
PROVIDER_URL = "https://site.financialmodelingprep.com/financial-summary/{symbol}"


def main(path: str) -> int:
    rows = json.loads(Path(path).read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    vals, comps, rejected = [], [], []

    for r in rows:
        ours, theirs = r["company_name"], r.get("provider_name") or ""
        if tight_key(ours) != tight_key(theirs) and not r.get("name_match_override"):
            rejected.append({**r, "why": f"provider name {theirs!r} does not normalise to "
                                         f"our canonical name {ours!r}"})
            continue
        mc = r.get("market_cap")
        if not mc or mc <= 0:
            rejected.append({**r, "why": "no positive market cap returned"})
            continue
        sym, prov = r["symbol"], r.get("provider", "Financial Modeling Prep")
        vals.append({
            "company_name": ours, "valuation_usd": float(mc),
            "valuation_type": "public_market_cap", "valuation_date": r["as_of"],
            "valuation_confidence": "HIGH",
            "share_price": r.get("share_price"),
            "shares_outstanding": r.get("shares_outstanding"),
            "notes": f"Market capitalisation for {sym} on {r.get('exchange', '?')} "
                     f"as of {r['as_of']}, via {prov}.",
            "collected_by": "orchestrator",
            "sources": [{
                "url": PROVIDER_URL.format(symbol=sym),
                "source_type": "market_data_provider", "tier": "TIER_2_SECONDARY",
                "publisher": prov, "title": f"{theirs} ({sym}) market data",
                "published_date": r["as_of"], "accessed_date": r["as_of"],
                "evidence_summary": (
                    f"{prov} reports a market capitalisation of {float(mc):,.0f} USD for "
                    f"{theirs} ({sym}, {r.get('exchange', '?')}) as of {r['as_of']}. Market "
                    f"cap is price x shares outstanding and is reproducible from the "
                    f"quote and share count on that date."),
            }],
        })
        comps.append({"canonical_name": ours, "aliases": [theirs] if theirs != ours else [],
                      "public_or_private": "PUBLIC", "ticker": sym,
                      "exchange": r.get("exchange"), "current_status": "OPERATING_PUBLIC",
                      "collected_by": "orchestrator"})

    with (OUT_DIR / "valuations.jsonl").open("a") as fh:
        for v in vals:
            fh.write(json.dumps(v) + "\n")
    with (OUT_DIR / "companies.jsonl").open("a") as fh:
        for c in comps:
            fh.write(json.dumps(c) + "\n")
    if rejected:
        with (OUT_DIR / "market_cap_rejects.jsonl").open("a") as fh:
            for x in rejected:
                fh.write(json.dumps(x) + "\n")

    print(f"accepted {len(vals)} valuations, rejected {len(rejected)}")
    for x in rejected:
        print(f"  REJECT {x.get('company_name')!r}: {x['why']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1
                          else str(ROOT / "data/processed/market_caps.json")))
