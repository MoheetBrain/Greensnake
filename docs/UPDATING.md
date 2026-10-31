# Updating the database

The database is disposable; the evidence is not. Everything below adds evidence
and then rebuilds.

## Add new research

1. Create a batch directory: `research/batches/<name>/`.
2. Write JSONL files following `docs/COLLECTION_CONTRACT.md`.
3. Validate — **this gate is not optional**:
   ```bash
   python3 scripts/validate_batch.py research/batches/<name>
   ```
4. Rebuild: `python3 scripts/build_graph.py`
5. Check `reports/validation_results.json` — any `FAIL` must be resolved before
   the output is trusted.
6. Commit the **batch files**, not the database.

Batches are append-only and independent, so several researchers can work at once
without conflicts. Re-running is safe: every id is a hash of the record's
natural key, so re-ingesting the same evidence updates rather than duplicates.

## Add people

Append to `research/people/people_universe.yaml`. Required: `key` (lower_snake,
unique), `name`, `affiliation`, `archetypes`, `domains`, `signal_class`,
`scores` and a `rationale` of at least 30 characters.

Use `early_stage: null` when there is no public investing record to judge — the
pipeline substitutes the pool median and records the substitution, rather than
scoring the person as a zero.

## Fix a bad entity merge

Edit `data/company_aliases.yaml`:
- `merges:` — force raw strings to one canonical entity.
- `do_not_merge:` — stop normalisation collapsing two genuinely different
  companies (it strips `Technologies`, `Labs`, `Group`, so `Figure`/`Figma`-type
  pairs need an explicit guard).

Then rebuild and check test `T03`.

## Retire a bad claim

Move it to the batch's `rejected.jsonl` with a `reason_rejected`. It will be
recorded in `rejected_edges` and excluded from every calculation. **Do not
delete it** — the rejected table is what stops a bad claim being rediscovered
and promoted months later.

## Re-test the people classification

```bash
python3 scripts/review_people_classification.py
```
Rewrites `docs/PEOPLE_CLASSIFICATION.md`, comparing each person's prior
`signal_class` against the visibility and herding the graph actually produced.
It proposes, never applies — accept a revision by editing
`research/people/people_universe.yaml` yourself.

## Re-verify sources

```bash
python3 scripts/build_graph.py --check-urls
```
Records an HTTP status per source. 401/403/405/429 count as *resolving* — a
paywalled or bot-blocked page is a real page. A URL that resolves to nothing is
either link rot or a fabricated citation; both need a human.

## Change the scoring model

- Score anchors and composite weights: `src/greensnake/scoring/people.py`
- Relationship weights: `src/greensnake/core/enums.py` (`RELATIONSHIP_WEIGHT`)
- Independence discount: `--delta`, or `DELTA_DEFAULT` in `scoring/company.py`
- Cluster threshold / co-investment rule: `src/greensnake/graph/correlation.py`

Bump `METHOD_VERSION` when you change a formula — it is stored per row, so old
and new scores stay distinguishable.

## Extend the backtest

Add companies to `research/companies/backtest_cohort.yaml`. **Add failures at
least as eagerly as winners** — the test only discriminates if both arms are
populated, and failures are the arm that collection naturally neglects.

## Resume after an interruption

`research/state.json` tracks phase status and workstream progress. The raw
batches are the checkpoint: rebuilding from them restores the full graph without
repeating any research.
