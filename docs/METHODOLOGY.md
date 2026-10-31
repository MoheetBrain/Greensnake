# Greensnake Methodology

Every number this project publishes falls into exactly one of four layers, and
they are never blurred:

| layer | what it is | example |
|---|---|---|
| **FACT** | a relationship or valuation supported by a source you can open | "Three tracked people have confirmed investment relationships with Company X." |
| **DERIVED METRIC** | arithmetic over facts, with a published formula | "Its independence-adjusted overlap is 2.1." |
| **ANALYTICAL INTERPRETATION** | judgement — clearly labelled as such | "Those three signals look partially correlated." |
| **UNKNOWN** | absent evidence, preserved as absent | "Exact ownership stakes are undisclosed." |

`NULL IS SUPERIOR TO FICTION.` No field is ever filled to make a table look complete.

---

## 1. The people universe

`research/people/people_universe.yaml` — 190 candidates across six workstreams.

Selection favours **information access and technical intelligence over wealth**.
A person is in the universe if they plausibly encounter frontier companies before
the general market, whether through research, operating position, founder
networks or capital. Some are included specifically as **negative controls** and
**visibility floors** — people with enormous capital and almost no reconstructable
private portfolio (Jan Koum, Brian Acton, Larry Page) — because knowing what the
graph *cannot* see is part of knowing what it can.

The file contains **no investment claims**. `affiliation` is a widely documented
public role. Every investment claim lives in `person_company_edges`, with sources.

### Score anchors (ordinal 0–5, ASSERTED)

These are the orchestrator's assessments from the public record. They are
deliberately coarse: the evidence does not justify decimals, and inventing them
would be false precision. Each carries a written `rationale`.

| band | `access` | `technical` | `early_stage` |
|---|---|---|---|
| 5 | sees essentially every frontier deal | world-class documented scientific/engineering record | repeatedly seeded eventual majors at formation |
| 4 | very strong cross-sector flow | deeply technical founder or operator | several such bets |
| 3 | strong within one domain | technical background, now mostly allocating | some early record |
| 2 | moderate | numerate generalist | thin public record |
| 1 | limited | non-technical | none documented |
| `null` | — | — | **no public investing record to judge** (≠ zero) |

`network`, `capital` and `independence` use the same 0–5 shape:
`independence` 5 means the person's information source is largely orthogonal to
the rest of the pool; 1 means heavily overlapping.

### DERIVED components (computed from the graph, never hand-set)

- **`investment_visibility`** — 0–5, from the number of confirmed companies plus
  the fraction of their evidence that is Tier-1. Answers "how well can this
  person's portfolio actually be reconstructed?", which bounds how much any
  conclusion about them is worth.
- **`herding_risk`** — 0–1, blending the share of their book that is crowded
  (≥3 tracked holders) with how strongly they link to the rest of the pool.

### From scores to `person_weight`

```
composite   = 0.30·access + 0.25·technical + 0.25·early_stage + 0.20·network   # 0–5
person_weight = (composite / 5) · class_multiplier
class_multiplier: CORE 1.00 · EXTENDED 0.90 · DOMAIN_SPECIALIST 0.90
                  WATCHLIST 0.70 · LOW_SIGNAL 0.50
```
A `null` component is replaced by the **pool median**, not zero, and the
substitution is recorded in `imputed_components` — so "no public record" is not
silently punished as "no ability".

`general_investment_signal` and `domain_information_signal` are kept **separate**
on purpose. A world-class researcher with two investments has a weak general
signal and a very strong domain one, and collapsing them would destroy exactly
the signal this project exists to find.

---

## 2. Relationship types — the distinction that matters most

The single largest source of false facts in this domain is treating *a fund a
person is associated with* as *that person*. The enum refuses to let that happen:

| overlap class | relationship types | meaning |
|---|---|---|
| **STRICT** | `PERSONAL_ANGEL_INVESTMENT`, `PERSONAL_EQUITY_INVESTMENT`, `FOUNDER_EQUITY`, `SPV_INVESTMENT` | direct personal economic exposure |
| **BROAD** (adds) | `FAMILY_OFFICE_INVESTMENT`, `CONTROLLED_FUND_INVESTMENT`, `CORPORATE_STRATEGIC_INVESTMENT`, `DEBT_FINANCING` | clearly attributable controlled vehicles |
| **INFORMATION-NETWORK** (adds) | `VC_FUND_PARTNER_INVESTMENT`, `BOARD_ONLY`, `ADVISOR_ONLY`, `LP_INDIRECT`, `GRANT_FUNDING`, `PHILANTHROPIC_FUNDING`, `OTHER_VERIFIED` | informational exposure without personal economic exposure |

The three sets are nested, and every published count says which one it uses.

A partner at a firm they do **not** control is `VC_FUND_PARTNER_INVESTMENT`.
A founder of their own firm is `CONTROLLED_FUND_INVESTMENT`. Test **T10** fails
the build if a `PERSONAL_*` edge names a fund as its vehicle.

`FOUNDER_EQUITY` is deliberately weighted *below* a personal angel cheque (0.90
vs 1.00): founding a company is not an act of selecting it, and this project is
looking for selection signal. Test **T09** keeps the two separable.

---

## 3. Evidence standard

| status | requirement (enforced at ingest) |
|---|---|
| `CONFIRMED_PRIMARY` | ≥1 Tier-1 source |
| `CONFIRMED_MULTI_SOURCE` | ≥2 distinct URLs, ≥2 non-database sources |
| `CONFIRMED_REPUTABLE_SECONDARY` | ≥1 Tier-2 source |
| `PROBABLE_BUT_NOT_CONFIRMED` / `CONFLICTING_EVIDENCE` / `UNVERIFIED` | excluded from all principal overlap calculations |

**A Tier-3 database listing can never confirm an edge on its own.** It generates
leads; something else confirms them. `src/greensnake/core/schema.py` rejects any
`CONFIRMED_*` record whose sources are all Tier-3.

Source URLs are HTTP-checked (`--check-urls`). A fabricated citation almost
always fails to resolve, so this doubles as an anti-hallucination control — but
401/403/405/429 are recorded as *resolving*, because a paywalled or bot-blocked
page is a real page.

---

## 4. Valuation and tiers

Best **current defensible** valuation per company, chosen by
`(freshness band, type preference, confidence, recency)` — recency beats type, so
a 2026 secondary outranks a 2022 priced round as a read on *today*.

Partial dates resolve to the **start** of the period, which can only make a
valuation look older. Erring stale is the safe direction.

| tier | bounds (USD) |
|---|---|
| `TIER_A_UNDER_500M` | `0 ≤ v < 500,000,000` |
| `TIER_B_500M_TO_1B` | `500,000,000 ≤ v < 1,000,000,000` |
| `TIER_C_1B_TO_5B` | `1,000,000,000 ≤ v < 5,000,000,000` |
| `TIER_D_5B_PLUS` | `v ≥ 5,000,000,000` |
| `TIER_U_UNKNOWN` | no sourced valuation |

Half-open intervals, so the tiers are provably disjoint (test **T05**).
Staleness bands: `<6m`, `6–12m`, `12–18m`, `18–36m`, `>36m`, always displayed.
**A company is never moved into a tier to avoid an empty cell** (test **T06**).

---

## 5. Overlap metrics

A person contributes **once per company**, via their single strongest edge,
regardless of how many rounds they joined. Multiple rounds are kept as separate
edge rows for temporal analysis but can never inflate a count (test **T08**).

```
raw_overlap_count   = distinct people with ≥1 CONFIRMED edge of any type
strict_count        = distinct people with ≥1 CONFIRMED STRICT edge
broad_count         = distinct people with ≥1 CONFIRMED STRICT or BROAD edge
information_network = raw_overlap_count          (equal by construction)

contribution(p)     = person_weight(p) · max(edge_weight over p's edges to C)
weighted_score      = Σ_p contribution(p)
```

`edge_weight = relationship_weight × verification_weight`, keeping "how much
signal does this kind of relationship carry" separate from "how sure are we it
is true".

### Independence adjustment

Ten investors from one network are not ten independent signals.

```
IA(δ) = Σ_clusters [ max_{p∈c} contribution(p) + δ · Σ_{p∈c, p≠argmax} contribution(p) ]
```

The strongest voice in each information network counts in full; every additional
member of that same network counts at δ. Published at **δ = 0.35** (default),
**δ = 0** (each network collapses to one voice) and **δ = 1.0** (identical to the
raw weighted score). Showing all three makes the adjustment's effect visible
rather than hidden.

**Circularity guard.** Co-investment correlation is derived from this same graph.
Scoring company X using a correlation link that exists *because of* company X
would double-count. So clusters for company X are computed with X removed from
the co-investment evidence (leave-one-out).

Clusters come from connected components of the person↔person graph at strength
≥ 0.50, over asserted links (same firm, co-founded, family, shared employer,
accelerator, syndicate) and derived ones (≥3 shared confirmed companies).

**Co-founders of the scored company are always one cluster.** Founding a company
together is a single joint decision, not N independent judgements about it. This
rule is applied directly rather than being left to whether some correlation
record happens to mention the company — which would be correct by accident and
wrong the moment the evidence were worded differently. Editas Medicine is the
worked example: four world-class gene-editing scientists, raw overlap 4, but one
founding act and therefore **one** information cluster.

### Two different "cluster" ideas

- **`distinct_information_clusters`** — network-correlation components. Drives independence.
- **`distinct_domains_represented`** — how many *domains* the backers read the world from
  (AI, semiconductors, fusion, bio, defence…). Drives cross-domain analysis.

`cross_domain_score = Σ_domains max contribution within that domain`, so five
backers from five domains outrank five from one.

### Technical elite

Qualifies at technical band ≥4 **and** either a research/academic archetype, or
band 5 with a founder-operator archetype — an engineer who built the thing, not a
famous name attached to it. **Celebrity is never evidence of technical capability.**

`number_of_billionaire_founders` is an explicit **PROXY**: founder-operators at
capital-flexibility band 5. It is not a sourced net-worth claim.

### Exploratory density metrics

```
ELITE_DENSITY             = weighted_score              / log(1 + valuation_usd)
TECHNICAL_ELITE_DENSITY   = technical_elite_score       / log(1 + valuation_usd)
INDEPENDENT_SIGNAL_DENSITY= independence_adjusted_score / log(1 + valuation_usd)
```
**Exploratory only — not proven predictors.** Inputs are preserved so the
formulas can be changed later without re-collecting anything.

### Temporal

Computed **only** from edges carrying a real `investment_date`. Undated edges are
excluded rather than imputed, and `dated_edge_person_count` shows how much of
each company's overlap the temporal view actually covers.

---

## 6. Provenance chain

```
ranking row → company_id → people_list[].edge_ids → sources(parent_id) → original URL
```
Every exported ranking carries `edge_ids`, so any published figure can be walked
back to the document behind it.

---

## 7. What this method cannot do

- **Angel and family-office investing is structurally under-disclosed.** Absence
  of an edge is never evidence of absence of an investment.
- **Losses are disclosed far less than wins.** Every hit-rate figure is biased
  upward, which is why outcome counts are suppressed unless company status is
  known for ≥80% of a person's confirmed companies.
- **Coverage is uneven by construction.** People who publish portfolios are
  over-represented relative to equally important people who do not. That is a
  property of the evidence, not of the people — and `investment_visibility`
  exists to keep it visible.
- **Overlap is not a recommendation.** A company surfaced here still needs
  diligence on valuation, dilution, access, liquidity, unit economics, burn,
  competition, feasibility, regulation and downside. The graph is a
  **discovery and prioritisation** instrument, nothing more.
