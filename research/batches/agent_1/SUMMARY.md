# agent_1 — WORKSTREAM 1: AI / Software / Semiconductors

Collected 2026-09-16. `python3 scripts/validate_batch.py research/batches/agent_1` → **OK**.

| file | records |
|---|---|
| `edges.jsonl` | 148 |
| `companies.jsonl` | 66 |
| `valuations.jsonl` | 8 |
| `correlations.jsonl` | 27 |
| `rejected.jsonl` | 3 |
| `queue.jsonl` | 22 |
| `people.jsonl` | 0 (no people added beyond the assigned list) |

## Edge counts

**By verification status**

| status | n |
|---|---|
| `CONFIRMED_PRIMARY` | 101 |
| `CONFIRMED_REPUTABLE_SECONDARY` | 24 |
| `CONFIRMED_MULTI_SOURCE` | 21 |
| `PROBABLE_BUT_NOT_CONFIRMED` | 2 |

146 of 148 edges are confirmed; 2 are deliberately held below the line (Hillspire→Hooglee, which CNBC
relays from Forbes rather than from its own dataset, and Bengio→LawZero, where the site stops short of
naming his role).

**By relationship type**

`PERSONAL_ANGEL_INVESTMENT` 65 · `FOUNDER_EQUITY` 26 · `CONTROLLED_FUND_INVESTMENT` 16 ·
`OTHER_VERIFIED` 15 · `PERSONAL_EQUITY_INVESTMENT` 7 · `FAMILY_OFFICE_INVESTMENT` 7 · `BOARD_ONLY` 5 ·
`PHILANTHROPIC_FUNDING` 4 · `LP_INDIRECT` 1 · `VC_FUND_PARTNER_INVESTMENT` 1 · `ADVISOR_ONLY` 1

**89 distinct companies. 37 of the 44 assigned people carry at least one edge.**

## Where the type discipline mattered

The contract's warning about collapsing relationship types bit repeatedly, and the split is load-bearing:

- **NFDG vs. personal.** Friedman and Gross appear constantly. Where the source says "of NFDG" or "from
  NFDG" (Composite, Granola) the edge is `CONTROLLED_FUND_INVESTMENT`; where it names them as individuals
  (ElevenLabs, Weights & Biases, EvolutionaryScale) it is `PERSONAL_ANGEL_INVESTMENT` with the vehicle
  recorded as unspecified. Chroma's pre-seed is attributed to **AI Grant**, their accelerator, so that is a
  controlled-fund edge too. Downstream analysis should treat these as one economic node.
- **Eric Schmidt has three distinct capital channels** and they are kept apart: Innovation Endeavors (the
  firm he co-founded and solely funded through Funds I and II) → `CONTROLLED_FUND_INVESTMENT`; Hillspire,
  his family office → `FAMILY_OFFICE_INVESTMENT`; and direct named participation (Anthropic's own Series A
  release, AMI Labs) → personal. Schmidt Sciences and the Special Competitive Studies Project are
  `PHILANTHROPIC_FUNDING`, not investments.
- **Non-profits do not get founder equity.** Mila, AI4ALL, the Vector Institute and the 2015 OpenAI
  non-profit are recorded as `OTHER_VERIFIED` founding relationships, never `FOUNDER_EQUITY`, because no
  shares exist. Sam Altman's and Greg Brockman's documented OpenAI donations are `PHILANTHROPIC_FUNDING`.
- **Employment and praise are not edges.** Jim Keller is CEO of Tenstorrent but *not* a founder; the
  economic edge is EE Times' statement that he "became the company's first investor", recorded separately
  from his board seat. Geoffrey Hinton's endorsement quote on Cohere's own About page is in
  `rejected.jsonl`, not in `edges.jsonl`.

## People covered, and how well

**Deep (5+ edges):** eric_schmidt (22), daniel_gross (18), nat_friedman (10), sam_altman (10),
guillermo_rauch (9), andrej_karpathy (8), amjad_masad (7), fei_fei_li (6), clem_delangue (5).

**Partial (2–4):** jeff_dean, aidan_gomez, greg_brockman, ilya_sutskever, yoshua_bengio, scott_wu,
geoffrey_hinton, tobi_lutke, dylan_field, mike_krieger, arthur_mensch, alexandr_wang, jim_keller,
emad_mostaque, mustafa_suleyman, john_schulman.

**Founder or single edge only:** aaron_levie, patrick_collison, john_collison, demis_hassabis,
kevin_systrom, dario_amodei, daniela_amodei, david_luan, noam_shazeer, yann_lecun, drew_houston,
mira_murati.

### Portfolios that could NOT be reconstructed, and why

These are documented absences, not abandoned searches. Each has a `queue.jsonl` row.

- **lisa_su, satya_nadella, kevin_scott** — no source anywhere names any of them as an individual investor
  in a private company. Their institutions invest through corporate arms (AMD Ventures, M12) which are
  `CORPORATE_STRATEGIC_INVESTMENT` attributable to the company, not the person. For these WATCHLIST /
  DOMAIN_SPECIALIST executives the absence is itself the finding: they are information nodes with no
  personal capital footprint.
- **jensen_huang** — same pattern. Nvidia's startup capital runs through NVentures; Nvidia's own About page
  does not state his co-founder status in retrievable text, so even the founder edge was not written.
- **shane_legg** — the hardest failure. Google DeepMind's own About page names only Hassabis as co-founder,
  so I could not write even the DeepMind founder edge for him from a source I opened. Companies House
  filings for DeepMind Technologies Ltd are the right next step and would show his original shareholding.
- **chris_olah, jared_kaplan** — universally described as Anthropic co-founders, but Anthropic's own Series
  A release names only Dario and Daniela Amodei. Olah's personal site carries research writing with no bio
  section; Kaplan's Johns Hopkins page has been archived and returns nothing. I refused to promote the
  widely-repeated claim on aggregator authority.

## Most interesting small / obscure companies with multiple elite backers

This is the signal the exercise is looking for. Ranked by how far below the radar the company sits:

1. **SkyPilot** (Berkeley spinout, unified AI compute, $20M seed July 2026) — **Jeff Dean, Guillermo
   Rauch, Amjad Masad and Clem Delangue all four named individually** in the company's own launch release.
   Four assigned principals on one seed cap table in a company most people have never heard of.
2. **Letta** (MemGPT commercial entity, stateful agent memory, $10M seed at $70M post) — **Jeff Dean and
   Clem Delangue**, named in both the company release and TechCrunch. The same pair recur in **Sophont**
   (open multimodal *medical* foundation models, $9.215M seed) — a two-deal overlap in a corner of the
   market nobody is watching.
3. **Chroma** (embeddings database) — **Rauch and Masad** in the seed, **Friedman and Gross via AI Grant**
   in the pre-seed. An unusually complete elite cap table for an open-source infra company.
4. **Mastra** (TypeScript agent framework, $13M) and **Granola** (AI notepad) — the Rauch / Masad / Lutke
   developer-tools cluster, with NFDG leading Granola's Series B and Mike Krieger on the angel list.
5. **Helical** (bio foundation models for pharma, London) — **Aidan Gomez and Clem Delangue**, twice: the
   2024 round and the 2026 seed. Two frontier-lab CEOs quietly repeat-backing a pharma infrastructure
   company.
6. **Composite** and **Pulse** — tiny ($5.6M and $3.9M) NFDG-led rounds in browser automation and
   unstructured-data prep. NFDG *leading* at this size is a stronger signal than their large holdings.
7. **UPower** — a nuclear-fission YC company Sam Altman chaired and seeded, documented only on his own
   blog. Almost invisible elsewhere; the most obscure company in this batch.
8. **tldraw** ($2.7M seed, infinite-canvas SDK) and **Substrate** ($8M, modular inference API) — Rauch
   alone, but both pure infrastructure primitives.
9. **Etched** — no longer small at $10.3B, but its individual cap table (**Karpathy, Dylan Field, Masad**,
   plus Thiel) formed when it was, and it is the only semiconductor company in the batch with that profile.

## Correlation structure worth flagging to the orchestrator

27 correlation rows. The one that most threatens naive overlap counting: **Friedman ↔ Gross** co-appear in
seven companies in this batch alone (ElevenLabs, Weights & Biases, Pulse, Composite, EvolutionaryScale,
Chroma, Granola) and share a firm. Treating them as independent signals would roughly double-count NFDG.
**Rauch ↔ Masad** co-appear in four (Chroma, Mastra, Granola, SkyPilot). **Dean ↔ Delangue** in three
(Letta, Sophont, SkyPilot). The Instagram pair (Systrom / Krieger) syndicate together too — they appear
back-to-back in Airtime's investor list.

## Sources that were paywalled or otherwise inaccessible

- **Newcomer** — "The Founders Writing Checks into Silicon Valley's Top AI Startups" (Oct 2024) is the
  single highest-value unread source for this workstream: a 13-name list of founder-angels with their
  portfolios. Only the free introduction was readable, which is where the Rauch → Scale AI edge came from.
- **Reuters** — the AMI Labs report is subscriber-only below the standfirst; I used the headline
  attribution only and took the detail from The Next Web instead.
- **Financial Times** — the Anthropic Series A piece (including an $845M valuation from a company filing)
  is paywalled. An `archive.is` mirror exists and I deliberately did **not** use it; no valuation record was
  written. Same decision for the NYT AMI Labs piece.
- **CNBC's Hillspire article** ends with "Here's the list of Hillspire's AI startup investments:" followed
  by an embedded table that does not render in text extraction. Only the six companies named in the prose
  were recorded — the other ~16 are queued and are probably the richest single unresolved lead here.
- **WSJ, Forbes, STAT** on Sam Altman's court-disclosed holdings (Helion stake, net worth) — paywalled.
- **cursor.com/blog/series-b** and **Sparrow's Series B release** are accessible but simply do not name
  individuals, which is itself recorded in `queue.jsonl`.

## What I would do next, in priority order

1. **Companies House and SEC Form D.** The biggest structural gap. DeepMind Technologies Ltd would settle
   Shane Legg. Form D signatory and investor pages would settle Anysphere/Cursor (the Collisons),
   Anthropic's early cap table, and Hillspire's portfolio without relying on Fintrx.
2. **Render the CNBC Hillspire table** in a real browser to recover the full 22-company list.
3. **Resolve Factorial Capital.** Delangue's deals are repeatedly attributed to it (Sophont, and reportedly
   Flower.dev and Nomic AI). Until it is known whether he founded, controls or merely partners in it, his
   edges are typed conservatively and are under-weighted in the graph.
4. **Work the co-investor lists of the five small companies above outward.** SkyPilot, Letta, Sophont,
   Chroma and Helical each name adjacent operator-angels (Ali Ghodsi, Lukas Biewald, Tristan Handy, Logan
   Kilpatrick, Robert Nishihara). Those people are the natural next ring of the universe and would convert
   single-backer companies into multi-backer ones.
5. **Systematically mine the personal blogs.** `blog.samaltman.com` yielded four first-person investment
   posts (Helion, UPower, reddit, Quora) in one pass; its full index almost certainly holds more. Karpathy,
   Levie and Field may have equivalents that were not exhausted.
6. **Public-company founder edges via filings** (Nvidia, AMD, Box, Figma, Shopify, Stripe S-1 / 10-K
   beneficial-ownership tables) would close the remaining founder gaps with Tier-1 evidence and supply
   dated market-cap valuations at the same time.

## Self-audit performed before hand-off

I re-opened every source URL that appeared in `edges.jsonl` and checked that I had actually read the
passage each `evidence_summary` describes. Two problems surfaced and both were fixed:

1. **Geoffrey Hinton's Toronto CV (`fullcv2024.pdf`) was cited but is not machine-readable.** On
   re-fetch it returns an unparseable binary stream. The source was removed from the Hinton → Vector
   Institute edge and the edge was **downgraded** from `CONFIRMED_MULTI_SOURCE` to `CONFIRMED_PRIMARY`,
   which the Vector Institute's own post still supports on its own.
2. **Etched's own site carries a much longer investor block than my first fetch returned.** Re-fetching at
   a higher character limit exposed a list headed "We're grateful for the support of our investors, angels,
   and advisors, including:" which names, among others, **Geoffrey Hinton, Aidan Gomez, Arthur Mensch,
   Scott Wu and Fei-Fei Li** — none of whom appear in TechCrunch's separate enumeration of Etched's
   individual *backers*. Because the heading merges investors with advisors, these five were added as
   `OTHER_VERIFIED`, **not** as investments, with a HIGH-priority queue row. This also partially supersedes
   my earlier rejection of Hinton → Etched, which addressed only the narrower investor claim; the rejection
   row is left in place and the queue row cross-references it.

The second finding is the more interesting one for the orchestrator: Etched has assembled what may be the
densest single concentration of assigned-person relationships in this batch — eight of the 44 appear on
that one page — but the company's own phrasing makes it impossible to tell investment from advice, so most
of it cannot be counted as capital.

## Note on valuations

Only 8 valuation records, all with a dated source: Weights & Biases $1.25B, /dev/agents $500M, Lamini
$325M, Etched $10.3B, Letta $70M, Character.AI $1B, AMI Labs $3.5B pre-money, Thinking Machines Lab $12B.
Everything else lands in `TIER_U_UNKNOWN` on purpose. Granola's $1.5bn and Chroma's $75M were both left out
because the only sources gave a figure without a date I could verify — per the contract, a valuation
without a date is unusable and a guessed one is worse than none.
