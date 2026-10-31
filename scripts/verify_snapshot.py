#!/usr/bin/env python3
"""Verify the preserved 2026-09-16 snapshot without changing any output.

Checks original-file SHA-256 hashes, all economic-intersection rows, stored
quality totals, SQLite integrity and the existing database validation suite.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECT = ('PERSONAL_ANGEL_INVESTMENT', 'PERSONAL_EQUITY_INVESTMENT',
          'SPV_INVESTMENT', 'FOUNDER_EQUITY')
CONTROLLED = ('FAMILY_OFFICE_INVESTMENT', 'CONTROLLED_FUND_INVESTMENT')


def main() -> int:
    failures = []
    manifest = json.loads((ROOT / 'docs/SNAPSHOT_MANIFEST.json').read_text())
    for path, expected in manifest['files'].items():
        edition = manifest.get('editorial_editions', {}).get(path)
        if edition:
            assert edition['original_sha256'] == expected, path
            expected = edition['public_sha256']
        target = ROOT / path
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            failures.append(f'Snapshot file missing or changed: {path}')
    print(f"Snapshot hashes: {len(manifest['files'])} original-file dispositions checked")

    con = sqlite3.connect((ROOT / 'database/elite_graph.sqlite').as_uri() + '?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    if con.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
        failures.append('SQLite integrity check failed')
    if con.execute('PRAGMA foreign_key_check').fetchall():
        failures.append('SQLite foreign-key check failed')

    quality = json.loads((ROOT / 'reports/data_quality.json').read_text())
    totals = {
        'people_total_in_universe': ('SELECT COUNT(*) FROM people', 190),
        'companies_canonical_total': ('SELECT COUNT(*) FROM companies', 2188),
        'edges_confirmed': ('SELECT COUNT(*) FROM person_company_edges WHERE is_confirmed=1', 3205),
        'sources_total': ('SELECT COUNT(*) FROM sources', 4694),
    }
    for key, (sql, expected) in totals.items():
        actual = con.execute(sql).fetchone()[0]
        if actual != expected or quality[key] != actual:
            failures.append(f'Quality total does not reconcile: {key}')
    print('Headline totals: 190 people / 2,188 companies / 3,205 confirmed edges / 4,694 sources')

    # Group by person first so repeated rounds and direct+controlled exposure
    # never count a person twice. This is a verification of the saved metric.
    direct_args = ','.join('?' for _ in DIRECT)
    econ_args = ','.join('?' for _ in DIRECT + CONTROLLED)
    sql = f'''
        WITH members AS (
            SELECT company_id, person_key,
                   MAX(CASE WHEN relationship_type IN ({direct_args}) THEN 1 ELSE 0 END) AS direct
            FROM person_company_edges
            WHERE is_confirmed=1 AND relationship_type IN ({econ_args})
            GROUP BY company_id, person_key
        )
        SELECT company_id, c.canonical_name AS company, COUNT(*) AS economic,
               SUM(direct) AS direct, COUNT(*)-SUM(direct) AS controlled
        FROM members JOIN companies c USING(company_id)
        GROUP BY company_id
    '''
    computed = [dict(r) for r in con.execute(sql, DIRECT + DIRECT + CONTROLLED)]
    computed.sort(key=lambda r: (-r['economic'], -r['direct'], r['company']))
    with (ROOT / 'data/exports/portfolio_intersections.csv').open(newline='') as handle:
        saved = list(csv.DictReader(handle))
    if len(saved) != len(computed) or len(saved) != 1814:
        failures.append('Ownership-ranking population differs from snapshot')
    for rank, (actual, expected) in enumerate(zip(computed, saved), 1):
        comparisons = {
            'rank': str(rank), 'company_id': actual['company_id'], 'company': actual['company'],
            'number_of_elite_people': str(actual['economic']),
            'direct_personal_or_founder_count': str(actual['direct']),
            'controlled_family_office_or_fund_count': str(actual['controlled']),
        }
        if any(expected[key] != value for key, value in comparisons.items()):
            failures.append(f'Ownership count/order mismatch at row {rank}')
    print(f'Ownership ranking: {len(computed):,} rows reconciled to confirmed edges')

    sys.path.insert(0, str(ROOT / 'src'))
    from greensnake.verification.validate import run_all
    results = run_all(con)
    for result in results:
        print(f"{result['test_id']} {result['status']}: {result['detail']}")
        if result['status'] == 'FAIL':
            failures.append(f"Existing validation failed: {result['test_id']}")
    con.close()
    if failures:
        for failure in failures:
            print('FAIL:', failure)
        return 1
    print('Snapshot verified. Existing warnings are retained; no files were modified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
