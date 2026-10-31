# Known coverage gaps

Compiled from what each research workstream reported it could **not** reach.
This file exists so the shape of the hole is documented rather than implied.

> **Absence of an edge is never evidence of absence of an investment.** Every gap
> below is a statement about the evidence available to this method, not about the
> people or companies concerned.

## 1. Structural gaps — whole categories the method cannot see

| gap | consequence |
|---|---|
| **Angel investing is under-disclosed by default.** Most personal cheques are never announced, and the ones that are tend to be into companies that later succeeded. | The graph systematically over-represents *winners* in every person's book, which biases every hit-rate figure upward. |
| **Losses are disclosed far less often than wins.** | The failure database understates true failure rates. `person_outcomes` therefore suppresses outcome counts unless company status is known for ≥80% of a person's confirmed companies. |
| **People who publish portfolios are over-represented.** A single personal investments page can yield 30+ Tier-1 edges; an equally active investor who publishes nothing yields none. | `investment_visibility` exists to keep this visible, and the classification review proposes demoting people whose books cannot be reconstructed — the method admitting its blind spot, not a judgement about them. |
| **Firm portfolio pages rarely attribute deals to partners.** | Partner-level selection signal is lost, and firm-founder signal is overstated relative to it. Reported explicitly for Founders Fund (Trae Stephens) and USV (Wilson/Wenger have identical edge sets by construction). |

## 2. Specific named gaps

### Sources that could not be read
- **Paywalled**: Newcomer's 13-founder-angel list (the single highest-value unread source for AI angels); the Financial Times on Anthropic's Series A; Axios Pro, Bloomberg, WSJ, The Information, STAT, Business Insider, Boston Business Journal, Endpoints, BioCentury. An `archive.is` mirror of the FT piece exists and was **deliberately not used**.
- **Rendered but not extractable**: `future.ventures/investments` publishes its ~60-company portfolio as image logos with no text — the largest single recoverable gap in the climate workstream. CNBC's Hillspire article ends with a 22-company list inside an embedded table that does not extract. `archventure.com/portfolio` is JS-rendered and returns 0 bytes to a fetcher. `jobs.thrivecap.com/companies` lazy-loads and yielded 12 of roughly 200.
- **No public site at all**: `additionvc.com` (Lee Fixel) is a parked domain. Builders Vision (Lukas Walton, >$15bn) publishes no portfolio anywhere. Vida Ventures' team and about pages both 404 — resolving whether Belldegrun controls it would re-weight 32 edges.
- **Registry access**: Australian ASX Form 604 substantial-holder notices (Gina Rinehart's lithium and rare-earth positions), and UK Companies House filings that would settle several founder claims, were not reached.
- **Unofficial mirrors refused**: `startsmall.llc` carries a machine-readable record of 386 Jack Dorsey grants but states it is not affiliated with him. It cannot carry Tier-1 status, so **zero** Start Small edges were written.

### People whose portfolios could not be reconstructed
- **Corporate executives** — Jensen Huang, Lisa Su, Satya Nadella, Kevin Scott. No source names any of them as an individual investor; their capital moves through corporate arms (AMD Ventures, M12, NVentures), which is company-attributable, not personal. For these, **the absence is the finding**.
- **Deliberately private** — Sergey Brin's Bayshore Global does not appear as an EDGAR filer at all. Jan Koum and Brian Acton have near-total absence. Larry Page, Eric Yuan and Travis Kalanick likewise. These people were included **specifically to measure this floor**.
- **Founder-only graphs** — Alex Karp, Stephen Cohen, Will Marshall, Brian Schimpf, Tom Mueller, Gwynne Shotwell, Daniela Rus, Chris Urmson: large founder stakes, no evidenced outside investing.
- **Contested co-founder status** — Chris Olah and Jared Kaplan are universally described as Anthropic co-founders, but Anthropic's own release names only the Amodeis. No edge was written on aggregator authority. Shane Legg's DeepMind co-founding could not be sourced from DeepMind's own About page, which names only Hassabis.

### Deliberate volume limits
- Kima Ventures publishes **984** companies; 52 frontier-technology ones were written so one vehicle's €150k tickets do not swamp the graph. Point72 Ventures publishes **161**; the 22 non-US ones were written. Citadel's 13F carries **16,127** positions of market-making inventory and was deliberately **not** collected — writing it would have injected ~16,000 meaningless rows and inflated every overlap metric.
- Both limits are fully reproducible from the same pages, and both are judgement calls a reviewer may disagree with.

## 3. Sectors and geographies likely under-covered

- **Geography**: coverage skews heavily US. Workstream 6 deliberately pushed into France, Australia, Latin America, Israel, Turkey, Indonesia and Hong Kong, which is why those appear at all. China, Japan, Korea, India, the Gulf and Africa are thin to absent.
- **Sector**: AI, climate/energy and biotech are well covered because the people universe was built around them. Consumer, fintech outside the US, industrials, agriculture, materials and healthcare services are comparatively thin.
- **Company metadata**: most companies were discovered through a portfolio listing that names them without describing them, so a large share carry no sector or country label at all. Any sector-level or geography-level count in `DATA_QUALITY.md` understates every category by that amount.

## 4. Valuation coverage — the binding constraint

Valuations are the project's narrowest bottleneck. Portfolio pages and personal
investment lists essentially never state a valuation, so most companies reached
through them land in `TIER_U_UNKNOWN` and **cannot appear in any tier ranking**.

This is not a defect in the tier tables; it is a statement about which companies
have a defensible public valuation at all. The highest-overlap unknown-valuation
companies are listed in `SECONDARY_QUESTIONS.md` question 10 — they are
simultaneously the graph's biggest blind spot and its best leads.
