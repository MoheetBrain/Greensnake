# Human review log

Integrity tests raise `WARN` when something needs a judgement a script should not
make. This file records the judgements, so a reviewer can see what was decided
and on what basis, and so a re-raised warning means something new.

## T09 — FOUNDER_EQUITY edges carrying a priced-round name (reviewed 2026-09-16)

Six edges flagged. **All six are correct as recorded.** Every one is a scientific
or operating founder whose founding was *announced alongside* a financing, so the
company's own launch release states both facts at once and the collector recorded
the round in which the founding was disclosed:

| person | company | round field | basis |
|---|---|---|---|
| Feng Zhang | Moonwalk Biosciences | Seed and Series A | launch release names him scientific co-founder |
| Jennifer Doudna | Scribe Therapeutics | Series A | launch release names her a founder and quotes her as co-founder |
| Carl June | Capstan Therapeutics | Seed and Series A | launch release lists him among founding scientists; Penn disclosure corroborates |
| Patrick Hsu | Stylus Medicine | Series A + extension | launch release lists him as Scientific Founder |
| Feng Zhang | Aera Therapeutics | Series A and Series B | release headed "Founded by ... Feng Zhang" |
| Brett Adcock | Hark | Series A | reported as the founder of the company raising the round |

**Conclusion: no data change.** These are `FOUNDER_EQUITY`, not later purchases.
The test stays as written — it is asking the right question, and the answer
happened to be clean this time.

## T03 — near-miss company names (reviewed 2026-09-16)

122 candidate pairs from the orchestrator's similarity scan, plus the pairs T03
itself flags. Each was resolved by reading the **edge evidence on both sides**,
never by name similarity.

- **24 merged** — recorded in `data/company_aliases.yaml` with a `basis` field.
- **26 guarded as genuinely different** — e.g. Vicarious (AI robotics) vs
  Vicarious Surgical; Lowercarbon's climate "Arbor" vs Feng Zhang's Arbor
  Biotechnologies; USV's "Odyssey" vs the biotech Odyssey Therapeutics held in
  EcoR1's 13F; Balaji's crypto "Paradigm" vs ARCH's Paradigm Health.
- **3 left unresolved** and raised in the research queue rather than guessed,
  including a bare "Radiant" listing that is probably, but not provably, the
  portable-microreactor company.
- **Uber / Uber Freight** kept separate with a parent link, so a financing into
  the subsidiary is never counted as one into the parent.

T03 no longer re-raises a pair once it is in `do_not_merge`: a warning a human has
already answered should stop nagging, or reviewers learn to ignore the test.

## Orchestrator edge audit (2026-09-16)

An independent audit by the orchestrator, separate from the verification
workstream's own sample. Edges were drawn **stratified by workstream** so no
single collector's habits could pass or fail the whole check, and each cited
page was opened and read against what the edge claims.

| edge | claim | source checked | verdict |
|---|---|---|---|
| Nat Friedman → ElevenLabs | `PERSONAL_ANGEL_INVESTMENT` | `elevenlabs.io/blog/series-b` | **CONFIRMED.** The company's own post reads "co-led by Andreessen Horowitz, Nat Friedman, Daniel Gross" — he is named as an individual alongside the firm, which is exactly what a personal angel edge requires. |
| Crystal Sacca → Mill | `CONTROLLED_FUND_INVESTMENT` | `lowercarboncapital.com/companies` + `lowercarbon.com/team/crystal-sacca` | **CONFIRMED.** Initially looked wrong: a partner bio cannot establish an investment. It carries **two** sources — one showing the fund holds Mill, one showing she co-founded the fund — and only together do they support the claim. The two-source construction is correct and the single-source view was misleading. |
| Paul Graham → Viaweb | `FOUNDER_EQUITY` | `paulgraham.com/bio.html` | **CONFIRMED.** "In 1995, he and Robert Morris started Viaweb." |
| Trae Stephens → Netic | `VC_FUND_PARTNER_INVESTMENT` | `foundersfund.com/portfolio/` | **CONFIRMED, and correctly typed.** Netic is listed, and the page attributes nothing to individual partners. The evidence summary says so in terms — "used here only as evidence that the firm invested, never that an individual partner wrote a personal cheque." This is the single distinction the project most depends on, and it held. |

**4 of 4 sampled edges are supported by the sources cited, and each is typed at
the correct strength.** A sample this size bounds nothing tightly; it is a check
that the collection discipline held across workstreams, not a measured error
rate. The verification workstream's independent 15-edge audit is reported
separately.

## Verification-workstream findings, adjudicated (2026-09-16)

The verification workstream reported eight issues. Each was checked by the
orchestrator rather than accepted on report.

### Corrected — the workstream was right

| finding | action |
|---|---|
| `Boring Company` and `The Boring Company` were two entities with **disjoint** backer sets | Leading articles are now stripped in normalisation. Merged, the company carries both sets. This was the single largest distortion in the graph. |
| `Zillow` / `Zillow.com` split, with the **same person on both sides** — one investor counted twice | `.com` is now a strippable suffix. |
| `Decart`/`Decart AI`, `Medra`/`Medra AI`, `Olive`/`Olive AI` split | The "AI" suffix is now a **secondary match key**, deliberately not part of the canonical key — stripping it inside normalisation would turn "Open AI" into "open" and collide it with anything called Open. Both orderings now resolve together. |
| `Radiant` / `Radiant Nuclear` / `Radiant Industries` | Merged. This was raised in the research queue as unprovable earlier; the workstream established it (a16z's post describes Radiant as building 1 MW portable nuclear reactors). The queue item is closed by evidence, which is how it was supposed to work. |
| `c_brilliant` wrongly merged **Brilliant Labs** (AR glasses) with **Brilliant** (smart home) | Guarded. This exposed a worse bug: `do_not_merge` was documented as preventing collapse but **was never consulted during resolution**. It is now enforced — a guarded name resolves on its exact spelling. |
| **Bloom Energy labelled MEDIOCRE** while now worth ~$80bn against ~$1.6bn at its 2018 IPO | Relabelled **WINNER**. Leaving a ~50x outcome in the negative-control arm would have biased the backtest *against* finding signal — the most dangerous direction for a test whose purpose is to check whether signal exists. |
| **Bird labelled MEDIOCRE** | Relabelled **FAILURE**. Chapter 11, assets sold to a lender-owned vehicle, listed equity did not survive. |

### Not corrected — the workstream was wrong

**Claim: the Breakthrough Energy portfolio page "returns only a newsletter signup
form to any fetcher", making it unverifiable evidence for 309 confirmed edges
(~10% of the confirmed base).**

Checked directly. The page returns **HTTP 200 with 925KB of content** and
contains every company name spot-checked against it — Fleetzero, VEIR, Albedo,
Heirloom, Antora, TerraCO2, Form Energy. The failure was in that workstream's
fetching tool, not in the citation.

This mattered enough to check rather than repeat: propagating it would have put
a false provenance warning on a tenth of the graph's confirmed edges. Subagent
reports are evidence, not verdicts.

### Noted, not actioned

- **`X (formerly Twitter)`** legitimately spans a 2007 angel entry and a 2025
  position under one id. Correct as entity resolution, unhelpful for
  entry→outcome multiples. Left as is and recorded here.
- **Concentrated evidence**: the top eight source URLs account for roughly 1,100
  of 3,205 confirmed edges. That is inherent to the highest-yield strategy —
  a single portfolio page legitimately evidences many relationships — but it
  means a handful of pages going dark would affect a large share of the graph.
  `T11` and the liveness cache exist for exactly this.
