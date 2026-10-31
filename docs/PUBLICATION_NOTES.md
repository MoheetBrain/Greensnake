# Publication notes

**Research snapshot:** 16 September 2026

**Presentation preparation:** 31 October 2026

**Public release status: PUBLIC — clean independent research snapshot.**

**Canonical public URL:** https://github.com/MoheetBrain/Greensnake

## Historical privacy blocker and resolution

The earlier preparation was held because reachable original Git author metadata
contained the owner's personal email. During close-out the original was again
found public. It was made private before curation, completely backed up and
retained as `MoheetBrain/Greensnake-Private-Archive` under its original repository
identity. Its branches, tags, commits and research remain recoverable privately.

The canonical name now identifies a **new independent repository**, populated
from reviewed source files without copying the original Git object database,
branches or tags. Public commits use GitHub noreply identities. A mailmap or
profile change was not treated as removing historical metadata. No destructive
history rewrite, force push or deletion of the original repository was used.

Final verification checks anonymous cloning/downloads, the new repository's
immutable identity, all reachable release history and the inability to retrieve
original historical commit objects from this public repository. The private
archive denies anonymous access. Earlier public copies, cached pages or forks
cannot be recalled by making the original private; this is not a claim that
prior exposure has been reversed.

## Preservation and integration

- Original development branch: `claude/elite-capital-intelligence-graph-8t4v78`.
- Original head: `8a9a1db5c043d9fd346f247c6c9f7b14c01b41c4`.
- Original `main`: `5d22bad15e7afcd5e4ea0dec9e2501a6756b46e1`; it is an ancestor of the development head.
- Recoverable tag: `preservation/development-original-2026-10-31`, pointing to the original development head. A full original-ref Git bundle was also saved locally before editing.
- The fresh checkout had no uncommitted changes. No branch or commit was deleted, rebased or force-pushed.
- Earlier presentation changes were integrated into the original main by a normal fast-forward, reaching `fcca80082c6480ade70bd8d3c110569c4e9188c9`. The archived development and publication branches remain intact. That prepared source snapshot is the basis of this clean public release.
- [SNAPSHOT_MANIFEST.json](SNAPSHOT_MANIFEST.json) accounts for **138 original files**: **137 remain byte-identical**, and `docs/COLLECTION_CONTRACT.md` has one explicitly recorded editorial change replacing a machine-specific `cd` path with a portable relative path. Its original and public hashes are both retained. The original README was previously replaced by the research presentation; close-out updates only its publication language and navigation. The source code, formulas, classification decisions, database, raw evidence, exports, reports and validation outputs are preserved.

## Audit scope and results

All remote branches and reachable history were cloned and inspected: **24 original commits, 517 distinct file blobs and 17 historical SQLite blobs**. Every reachable blob was scanned for common token/private-key formats, credential assignments, authentication URLs, email/phone patterns and confidentiality labels. Historical SQLite blobs were also opened and their table values scanned. Commit messages and author/committer metadata were inspected. No credential match or private contact detail in tracked file contents was identified; the personal author metadata was the historical blocker and is excluded from the new public Git history. The close-out audit additionally covered 25 reachable original commits, 527 blobs and all 17 historical SQLite versions. Pattern scanning is not a guarantee that no undisclosed secret can exist.

The CSV/JSONL/YAML/Markdown records and database schema contain public profiles, company relationships, valuation observations, short source summaries and original research annotations. Provenance notes identify public portfolio pages, filings, original reporting and public source URLs; inaccessible sources and rejected claims are retained. No full article archive or proprietary vendor database dump was identified. The one PitchBook source is an attributed newsletter summary of a historical valuation. Source text, quotations and provider rights are excluded from the project's licensing grant; see [DATA_LICENSE.md](DATA_LICENSE.md).

Only `MoheetBrain` had collaborator access at inspection, with the owner/admin role. No collaborator was added and no visitor was granted write access. The wiki is disabled. The default remains `main`. Branch protection requires pull requests with **zero mandatory approvals**, allowing a sole maintainer to merge their own proposals. Force pushes and deletion are prohibited, conversation resolution is required, and protections apply to administrators after the initial fast-forward integration. Outside users cannot write directly to the repository; while private, they also cannot read or fork it without access.

## Validation

| Check | Result |
|---|---|
| SQLite integrity and foreign keys | Pass |
| Original-file preservation | All 138 original-file dispositions verified: 137 byte-identical and one documented portable-path edition |
| Headline database totals | 190 people; 2,188 companies; 3,205 confirmed edge records; 4,694 source records |
| Complete ownership ranking | All 1,814 rows reconcile to distinct confirmed qualifying people, including direct/controlled splits and deterministic ordering |
| Original invariant suite | All invariants hold |
| Existing database validation | **8 PASS, 3 WARN, 0 FAIL** |
| Original warnings | T03: 8 near-match entity pairs; T09: 7 founder-equity/round labels; T11: 24 confirmed edges with no recorded resolving citation |
| Saved outputs and negative results | Preserved, including unresolved/rejected claims and historical backtest limitations |
| Full pipeline | Completed only in a disposable copy with `--as-of 2026-09-16`; no rebuilt output substituted into this release |
| Public anonymous downloads | Verified for SQLite, all CSV exports and the complete release archive |

The build script's summary prints “11/11 passing” when there are no failures, but that includes warnings. This presentation uses the precise **8 PASS / 3 WARN** breakdown.

## Rebuild limitations

Publication checks used Python **3.12**, PyYAML **6.0.3** and requests **2.34.2**. The documented minimum remains Python 3.11. These are the verification environment versions, not a claim about the original author's runtime.

The disposable rebuild reproduced canonical people/company/relationship/source totals, valuations, the queue, rejections and all economic-intersection counts and ordering, and the economic-intersection report. A full byte-identical build was **not** achieved:

- `companies.date_added` and `run_metadata.built_at` use the execution date even when `--as-of` pins the analysis date.
- `people_scores.domain_information_signal` JSON key ordering differed for 91 people, with the same values.
- Fourteen company-score rows differed in small derived-score values: weighted score in 10 rows, technical score in 2, technical density in 1 and cross-domain score in 3 (some rows overlap). Different iteration/summation order is a plausible cause; it has not been established as the sole cause. No formula was changed to hide these differences.
- Regenerating the ownership CSV preserved all 1,814 ranks, ownership counts and direct/controlled splits, but changed `weighted_score_secondary` in 10 rows. The ownership Markdown report remained byte-identical.
- Other report and CSV orderings changed as a consequence. The original snapshot and all its scores remain the publication reference.

Always rebuild in a separate worktree and compare outputs. The legacy README's byte-identical-rebuild claim is not repeated. The new [verify_snapshot.py](../scripts/verify_snapshot.py) is read-only and checks preserved bytes, all ownership rows and existing validation without rebuilding.

## Licensing, attribution and scope

The owner-authorised presentation adds MIT for original software and CC BY 4.0 for original research annotations and compilation, limited to rights held by the contributors. Third-party source content is excluded. [CITATION.cff](../CITATION.cff) identifies the maintainer without adding the personal email. Historical research-workstream attribution remains intact; original Git authorship is retained in the private archive, with noreply attribution on the independent public history.

This preparation adds presentation and verification only: no investment research, new investment observations, valuation refresh, scoring model or changed result. Historical statuses and valuations are not represented as present-day values. Highest-overlap companies are not investment recommendations. The historical metadata blocker is resolved for the clean public snapshot. No scientific result, ranking or valuation was recalculated during close-out.
