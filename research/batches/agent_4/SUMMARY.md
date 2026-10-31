# agent_4 — Space / Defence / Robotics — collection summary

Collected 2026-09-16. Validator: `python3 scripts/validate_batch.py research/batches/agent_4` → **OK**.

## Counts

| file | records |
|---|---|
| `edges.jsonl` | 204 |
| `companies.jsonl` | 41 |
| `valuations.jsonl` | 3 |
| `people.jsonl` | 0 (no person outside the assigned 23 needed an edge) |
| `correlations.jsonl` | 20 |
| `rejected.jsonl` | 10 |
| `queue.jsonl` | 13 |

204 edges across **140 distinct companies**, drawn from **67 distinct source URLs**, every one of
which was opened and read. No edge cites a page that was not fetched.

### By verification status
| status | edges |
|---|---|
| `CONFIRMED_PRIMARY` | 183 |
| `CONFIRMED_MULTI_SOURCE` | 9 |
| `CONFIRMED_REPUTABLE_SECONDARY` | 11 |
| `PROBABLE_BUT_NOT_CONFIRMED` | 1 |

### By relationship type
| type | edges |
|---|---|
| `CONTROLLED_FUND_INVESTMENT` | 70 |
| `VC_FUND_PARTNER_INVESTMENT` | 57 |
| `FOUNDER_EQUITY` | 44 |
| `PERSONAL_EQUITY_INVESTMENT` | 19 |
| `PERSONAL_ANGEL_INVESTMENT` | 9 |
| `PHILANTHROPIC_FUNDING` | 2 |
| `OTHER_VERIFIED` | 2 |
| `BOARD_ONLY` | 1 |

### By person (all 23 assigned covered)
peter_thiel 46 · trae_stephens 40 · joe_lonsdale 32 · raj_shah 18 · david_ulevitch 12 ·
katherine_boyle 7 · elon_musk 7 · brett_adcock 6 · palmer_luckey 5 · peter_beck 5 ·
marc_raibert 3 · rodney_brooks 3 · eric_migicovsky 3 · jared_isaacman 3 · sebastian_thrun 3 ·
chris_urmson 2 · gwynne_shotwell 2 · alex_karp 1 · stephen_cohen 1 · brian_schimpf 1 ·
daniela_rus 1 · tom_mueller 1 · will_marshall 1.

## Typing discipline applied

- **Founders Fund ≠ Peter Thiel personally.** Every Founders Fund portfolio company is recorded as
  `CONTROLLED_FUND_INVESTMENT` for Thiel (Impulse Space's own release calls FF "the firm founded by
  Peter Thiel") and as `VC_FUND_PARTNER_INVESTMENT` for Trae Stephens, who is a partner but does not
  control the firm. Thiel's *personal* vehicles are recorded separately where evidenced:
  his 2015 OpenAI **donation** (`PHILANTHROPIC_FUNDING`), his personal cheque into Vicarious'
  $15M round, and his Palantir/PayPal founder shares.
- **8VC = Lonsdale's controlled fund**, a16z = a firm Boyle and Ulevitch do *not* control.
  Shield Capital = Raj Shah's controlled fund (Shield's own page: "Founder and Managing Partner").
- **Founding is not selection.** Elon Musk's graph here is deliberately dominated by
  `FOUNDER_EQUITY` (SpaceX 85.1% of combined voting power per the S-1, Neuralink, The Boring
  Company, xAI) plus `PERSONAL_EQUITY_INVESTMENT` for Tesla (19.8% per the proxy) and Vicarious.
  Same treatment for the Anduril, Palantir and Figure founders.
- **No government contract was treated as an investment.** DoD/NASA/DARPA awards appear only as
  context inside `companies.jsonl` notes.
- **No date was guessed.** Most edges carry `investment_date: null` because the source did not
  state one — mostly fund portfolio pages, which publish holdings without dates.

## Highest-value finds: small/obscure companies with elite backers

- **Valar Atomics** (El Segundo; helium-cooled mass-manufactured fission microreactors, suing the
  NRC). **Palmer Luckey personally** in the $130M Series A, alongside Palantir CTO Shyam Sankar —
  named individually by CNBC *and* the LA Times, not via Anduril.
- **Dynamic Creatures** (Boston; mobile character robots; Boston Dynamics' official entertainment
  partner, founded by BD's ex-CSO and an ex-RAI Institute lead). **Marc Raibert** as a named angel
  in the seed, per lead investor Kindred Ventures' own post. Amount undisclosed. The only angel
  cheque from Raibert evidenced anywhere.
- **Terra Industries** (Abuja, Nigeria; "Africa's first modern defence prime", 15,000 sq ft factory).
  $11.75M seed **led by Lonsdale's 8VC**, with Lonsdale co-bylining the announcement; Valor, Lux,
  SV Angel alongside.
- **Star Catcher** (Jacksonville; space-to-space optical power beaming — beat DARPA's world record).
  **Shield Capital co-led the $65M Series A** (May 2026).
- **UFORCE** (Ukrainian combat-proven autonomous systems expanding into NATO). **Shield co-led the
  seed**, in a post personally bylined by **Raj Shah**.
- **Autonomous Cyber** (FUZZ-E, AI-native offensive cyber for US forces; USAF TACFI award).
  Shield led the seed, May 2026.
- **CX2** (electronic warfare / spectrum dominance, seed stage) — sits in **both** 8VC's portfolio
  **and** a16z's, where a16z's own page names **David Ulevitch** as having led it.
- **Northwood** (phased-array satellite ground stations) — a16z seed then Series A, both announced by
  **Katherine Boyle** personally.
- **Foundry Lab** (Wellington NZ; microwave metal casting, parts in <8 hours) — **Peter Beck** named
  in the company's own Series A release next to Karl Iagnemma and Carl Bass.
- **Brilliant Labs** (Singapore AR wearables) and **Mentra** (smart-glasses OS) — **Eric Migicovsky**
  named by the companies themselves; he *led* the Brilliant Labs seed with Brendan Iribe and Adam Cheyer.
- **Heartlab** (Auckland, AI cardiac imaging) — Peter Beck co-invested with Dylan Field; only a single
  passing NZ Herald mention exists, so it is flagged as thinly evidenced in `companies.jsonl`.

Companies attracting the most distinct people (excluding the obvious SpaceX/Palantir/Anduril
clusters): **Hadrian** (Boyle + Founders Fund), **Apex** (Boyle + Raj Shah — a16z *and* Shield in the
same satellite-bus company), **Saronic** (Boyle + 8VC), **CX2** (Ulevitch + 8VC), **Erebor** (Luckey
personally + 8VC + Founders Fund), **Halter** (Beck + Thiel/Founders Fund).

## Whose portfolios could not be reconstructed, and why

- **Alexander Karp** and **Stephen Cohen** — nothing beyond Palantir. Both hold very large Palantir
  stakes (11.4% and 3.0% of the vote) and neither appears as an individual investor in any funding
  announcement, filing or interview I could open. Their capital appears to run through Palantir
  itself. A documented *absence*, not a research gap.
- **Will Marshall** — same. Extensive searching produced only Planet's own funding history.
- **Brian Schimpf** — one edge (Anduril founder equity). Anduril's own leadership page says he
  "serves as a senior advisor and board member for several government technology companies" but
  names none of them. That sentence is the whole public trail.
- **Tom Mueller** — one edge (Impulse Space founder equity, corroborated by the company's Form D).
  No personal angel investment in another space company could be verified.
- **Gwynne Shotwell** — deliberately low-visibility. Fortune noted in 2022 that she "hasn't publicly
  announced many personal investments". Only Evernow is confirmed; her SpaceX holding is recorded as
  `OTHER_VERIFIED` because the S-1 does not distinguish purchased equity from compensation equity.
- **Daniela Rus** — one edge (Liquid AI co-founder). Her role is academic; no investing record exists.
- **Chris Urmson** — Aurora founder equity (29.9% of voting power) plus an Edge Case board seat
  disclosed in Aurora's proxy. No investments.
- **Trae Stephens' *personal* selection record is not reconstructable.** Founders Fund publishes a
  firm-level portfolio and partner bios but — unlike a16z — does not attribute individual deals to
  partners. Every Founders Fund edge here is therefore firm-level, which understates Stephens and
  overstates the breadth of Thiel's personal conviction. Biggest structural gap in this batch;
  queued HIGH.
- **Jared Isaacman** — his OGE/ProPublica financial disclosure was opened, but "Roles Outside
  Government" lists only his own holding entities (Rook Holdings, Rook Space Investments, PolarisX,
  Rook SPV I–IV, Black Diamond Jet HoldCo) and the asset schedule is dominated by public equities and
  Blackstone funds. No third-party startup holdings are individually named.

## Paywalled / blocked sources

- **Axios Pro** — the May 2025 scoop that Palmer Luckey would lead a round in stablecoin bank
  **Atticus** at a $1.5–2bn valuation. Queued, not recorded.
- **Financial Times** — the March 2026 report that **ModRetro** is raising at ~$1bn is FT-original.
  Luckey's ModRetro founder equity is recorded from ModRetro's own site; the valuation is not.
- **Bloomberg** — the $6bn Valar Atomics Series B valuation (Aug 2026) and the $2bn+ Liquid AI
  Series A valuation are Bloomberg-original. Not recorded as valuations.
- **Stuff.co.nz** (Foundry Lab) returned an empty body; the PR Newswire release carried the same fact.
- **NBR** and **NZ Herald** are subscription titles but served enough of the article body to read the
  investor sentences directly; both were opened, not snippet-scraped.

## Notes on judgement calls

- `joe_lonsdale`'s "early investor in Oculus, Guardant Health, Oscar, Illumio, Wish, JoyTunes, Blend,
  Flexport, Orca Bio, Qualia, Synthego, RelateIQ, Yugabyte" comes from 8VC's own bio, which
  attributes them to him as an individual but **never names a vehicle**. Several predate 8VC
  (founded 2015) and fall in the Formation 8 era. Recorded as `PERSONAL_EQUITY_INVESTMENT` with
  `investment_vehicle` spelling the ambiguity out, and queued.
- `peter_thiel` → **Halter** is the batch's only `PROBABLE_BUT_NOT_CONFIRMED` edge. The NZ Herald
  says Halter was "bankrolled by Rocket Lab's Peter Beck, Peter Thiel and Sir Stephen Tindall", but
  Founders Fund is separately a long-standing Halter backer, so "Peter Thiel" is probably shorthand
  for the firm. Left short of confirmed and queued.
- Two provisional rows were replaced during collection rather than left contradictory: a
  `BOARD_ONLY` row for Boyle/Castelion (upgraded once Castelion's own release confirmed a16z's
  participation) and a `BOARD_ONLY` row for Rus/Liquid AI (superseded by the company's own
  statement that she co-founded it).

## Next steps

1. **Founders Fund partner attribution.** Chase portfolio-company press releases and Form D
   related-person listings for FF's defence book (Anduril, Varda, Impulse, Hadrian, General Matter,
   Nominal, Fortell, ARQ, Until, Enter, Netic, Mnzil, EnduroSat) to find where Trae Stephens is
   personally named as a board member or lead. Converts ~40 low-weight firm edges into person-level
   signal.
2. **Traysar.** Get the company's own $25M announcement or Israeli registrar filings to settle
   whether Luckey / Schimpf / Stephens invested personally.
3. **Isaacman's Rook SPV I–IV and Rook Space Investments LLC.** SEC Form D filings by those entities
   would reveal what the NASA Administrator's SPVs actually hold.
4. **New Zealand angle.** Beck's NZ portfolio (Astrix Astronautics, Dotterel Technologies, Heartlab)
   is best resolved through the NZ Companies Office share register rather than press.
5. **Shield Capital and 8VC portfolio depth.** Several named portfolio companies (mPower Technology,
   Pillar Security, Distributed Spectrum, Reveal Technology, Obviant, Danti, Chariot Defense) appear
   only in newsroom items and deserve direct confirmation.
