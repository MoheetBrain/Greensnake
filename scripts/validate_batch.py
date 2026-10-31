#!/usr/bin/env python3
"""Validate a research batch directory against the Greensnake collection contract.

    python3 scripts/validate_batch.py research/batches/agent_1

Exit code 0 = batch is accepted. Non-zero = fix the reported errors.
Research workers MUST run this before reporting completion.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from greensnake.core.schema import validate_record  # noqa: E402

FILES = {
    "edges.jsonl": "edge",
    "companies.jsonl": "company",
    "valuations.jsonl": "valuation",
    "people.jsonl": "person",
    "correlations.jsonl": "correlation",
}
FREEFORM = {
    "rejected.jsonl": ("person_key", "company_name", "reason_rejected", "date_checked"),
    "queue.jsonl": ("claim", "reason_unresolved", "date_raised"),
}


def check_dir(d: Path) -> int:
    errors: list[str] = []
    counts: dict[str, int] = {}
    if not d.exists():
        print(f"FAIL: {d} does not exist")
        return 2

    for fname, kind in FILES.items():
        f = d / fname
        if not f.exists():
            counts[fname] = 0
            continue
        n = 0
        for lineno, line in enumerate(f.read_text().splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            n += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{fname}:{lineno}: invalid JSON ({e})")
                continue
            for msg in validate_record(rec, kind):
                errors.append(f"{fname}:{lineno}: {msg}")
        counts[fname] = n

    for fname, required in FREEFORM.items():
        f = d / fname
        if not f.exists():
            counts[fname] = 0
            continue
        n = 0
        for lineno, line in enumerate(f.read_text().splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            n += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{fname}:{lineno}: invalid JSON ({e})")
                continue
            for k in required:
                if not rec.get(k):
                    errors.append(f"{fname}:{lineno}: missing required field {k!r}")
        counts[fname] = n

    print(f"=== batch: {d.name} ===")
    for k, v in counts.items():
        print(f"  {k:22s} {v:5d} records")
    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors[:200]:
            print("  -", e)
        if len(errors) > 200:
            print(f"  ... and {len(errors) - 200} more")
        return 1
    print("\nOK: batch conforms to the collection contract.")
    return 0


if __name__ == "__main__":
    targets = sys.argv[1:] or [str(ROOT / "research" / "batches")]
    rc = 0
    for t in targets:
        p = Path(t)
        if p.is_dir() and not any((p / f).exists() for f in FILES):
            subs = sorted(x for x in p.iterdir() if x.is_dir())
            if subs:
                for s in subs:
                    rc |= check_dir(s)
                sys.exit(rc)
        rc |= check_dir(p)
    sys.exit(rc)
