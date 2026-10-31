# SECONDARY INVESTIGATIVE QUESTIONS

Every answer below is a query over the confirmed graph. `FACT` rows are counts of sourced edges; `DERIVED` rows are formulas from `docs/METHODOLOGY.md`; anything interpretive is labelled `ANALYSIS`.

## 1. Which people historically entered exceptional companies earliest?

`FACT` — confirmed edges with a real `investment_date`, into companies now valued at $1B+. Undated edges are excluded, so this understates everyone whose early deals are simply undated.

| person | company | entered | entry_val | now_val | mult | rel |
|---|---|---|---|---|---|---|
| John Doerr | Netscape | 1994 | — | $2.90B | — | VC_FUND_PARTNER_INVESTMENT |
| John Doerr | Bloom Energy | 2002 | — | $79.93B | — | VC_FUND_PARTNER_INVESTMENT |
| John Maraganore | Alnylam Pharmaceuticals | 2002 | — | $42.63B | — | OTHER_VERIFIED |
| Elon Musk | SpaceX | 2002 | — | $2.06T | — | FOUNDER_EQUITY |
| Sean Parker | Meta Platforms | 2004 | — | $1.73T | — | FOUNDER_EQUITY |
| Peter Beck | Rocket Lab | 2006 | — | $38.21B | — | FOUNDER_EQUITY |
| Drew Houston | Dropbox | 2007 | — | $8.24B | — | FOUNDER_EQUITY |
| Li Ka-shing | Meta Platforms | 2007 | — | $1.73T | — | FAMILY_OFFICE_INVESTMENT |
| Li Ka-shing | Spotify | 2009 | — | $114.89B | — | FAMILY_OFFICE_INVESTMENT |
| John Doerr | QuantumScape | 2010 | — | $3.10B | — | VC_FUND_PARTNER_INVESTMENT |
| Robert Langer | Moderna, Inc. | 2010 | — | $57.16B | — | FOUNDER_EQUITY |
| Noubar Afeyan | Moderna, Inc. | 2010 | — | $57.16B | — | FOUNDER_EQUITY |
| Will Marshall | Planet Labs | 2010 | — | $5.81B | — | FOUNDER_EQUITY |
| Mike Speiser | Snowflake | 2012 | — | $81.00B | — | VC_FUND_PARTNER_INVESTMENT |
| John Doerr | Uber | 2014 | — | $145.14B | — | VC_FUND_PARTNER_INVESTMENT |
| Jan Koum | WhatsApp | 2014-02-19 | — | $16.00B | — | FOUNDER_EQUITY |
| John Doerr | DoorDash | 2015 | — | $84.52B | — | VC_FUND_PARTNER_INVESTMENT |
| Ilya Sutskever | OpenAI | 2015-12 | — | $852.00B | — | OTHER_VERIFIED |
| Greg Brockman | OpenAI | 2015-12 | — | $852.00B | — | OTHER_VERIFIED |
| Andrej Karpathy | OpenAI | 2015-12 | — | $852.00B | — | OTHER_VERIFIED |
| John Schulman | OpenAI | 2015-12 | — | $852.00B | — | OTHER_VERIFIED |
| Sam Altman | OpenAI | 2015-12 | — | $852.00B | — | OTHER_VERIFIED |
| Sam Altman | OpenAI | 2015-12 | — | $852.00B | — | PHILANTHROPIC_FUNDING |
| Greg Brockman | OpenAI | 2015-12 | — | $852.00B | — | PHILANTHROPIC_FUNDING |
| Yoshua Bengio | OpenAI | 2015-12 | — | $852.00B | — | ADVISOR_ONLY |
| Elon Musk | OpenAI | 2015-12 | — | $852.00B | — | PHILANTHROPIC_FUNDING |
| Peter Thiel | OpenAI | 2015-12 | — | $852.00B | — | PHILANTHROPIC_FUNDING |
| Alexandr Wang | Scale AI | 2016 | — | $29.00B | — | FOUNDER_EQUITY |
| Feng Zhang | Beam Therapeutics | 2017 | — | $2.34B | — | FOUNDER_EQUITY |
| David Liu | Beam Therapeutics | 2017 | — | $2.34B | — | FOUNDER_EQUITY |

## 2. Which people have the strongest domain-specific signal?

`DERIVED` — `domain_information_signal` blends technical band, access and independence. It is deliberately separate from general investing signal: a world-class researcher with two investments scores low on one and high on the other, and collapsing them would destroy the signal this project looks for.

| person | domain | signal | visibility | weight |
|---|---|---|---|---|
| Ilya Sutskever | AI | 5.00 | 2.6 | 0.774 |
| Yann LeCun | ROBOTICS | 5.00 | 1.0 | 0.765 |
| Steve Jurvetson | INDUSTRIAL | 5.00 | 4.0 | 1.000 |
| Noubar Afeyan | AGRIFOOD | 5.00 | 5.0 | 1.000 |
| Robert Langer | MATERIALS_MINING | 5.00 | 4.0 | 0.950 |
| Jennifer Doudna | BIO | 5.00 | 2.7 | 0.900 |
| Feng Zhang | BIO | 5.00 | 2.7 | 0.900 |
| David Liu | BIO | 5.00 | 4.0 | 0.900 |
| George Church | BIO | 5.00 | 5.0 | 0.950 |
| Daphne Koller | BIO | 5.00 | 3.0 | 0.900 |
| Richard Klausner | BIO | 5.00 | 3.0 | 0.950 |
| Eric Lander | BIO | 5.00 | 3.0 | 0.810 |
| Elon Musk | SPACE | 5.00 | 2.9 | 0.950 |
| Palmer Luckey | DEFENCE | 5.00 | 2.5 | 0.950 |
| Larry Page | MOBILITY | 5.00 | 1.5 | 0.774 |
| Sergey Brin | BIO | 5.00 | 2.0 | 0.774 |
| Demis Hassabis | BIO | 4.85 | 2.0 | 0.850 |
| Andrej Karpathy | MOBILITY | 4.85 | 3.3 | 0.765 |
| Dario Amodei | BIO | 4.85 | 1.5 | 0.850 |
| Fei-Fei Li | ROBOTICS | 4.85 | 3.0 | 0.850 |
| Jensen Huang | ROBOTICS | 4.85 | 0.0 | 0.900 |
| Lisa Su | SEMICONDUCTORS | 4.85 | 0.0 | 0.774 |
| Mira Murati | AI | 4.85 | 1.0 | 0.850 |
| Nat Friedman | AI | 4.85 | 3.8 | 1.000 |
| Patrick Collison | AI | 4.85 | 2.0 | 1.000 |

## 3. Which combinations of people appear together unusually often?

`FACT` — distinct companies where both people hold a confirmed edge.

| a | b | shared |
|---|---|---|
| Chris Sacca | Crystal Sacca | 105 |
| Bill Gates | Carmichael Roberts | 103 |
| Bill Gates | Eric Toone | 103 |
| Carmichael Roberts | Eric Toone | 103 |
| Ali Partovi | Hadi Partovi | 62 |
| Albert Wenger | Fred Wilson | 47 |
| Peter Thiel | Trae Stephens | 38 |
| Bill Gates | Chris Sacca | 14 |
| Bill Gates | Crystal Sacca | 14 |
| Carmichael Roberts | Chris Sacca | 14 |
| Carmichael Roberts | Crystal Sacca | 14 |
| Chris Sacca | Eric Toone | 14 |
| Crystal Sacca | Eric Toone | 14 |
| Daniel Gross | Nat Friedman | 9 |
| Robert Nelsen | Eli Casdin | 9 |
| Robert Nelsen | Kristina Burow | 9 |
| Elad Gil | Peter Thiel | 8 |
| Elad Gil | Trae Stephens | 8 |
| Maryanna Saenko | Steve Jurvetson | 8 |
| Daniel Gross | Elad Gil | 7 |
| Elad Gil | Hemant Taneja | 7 |
| Elad Gil | Ron Conway | 7 |
| Elad Gil | Vinod Khosla | 6 |
| Joe Lonsdale | Peter Thiel | 6 |
| Alfred Lin | Vinod Khosla | 5 |

## 4. Which combinations preceded enormous outcomes?

`FACT` — pairs co-occurring on cohort companies labelled WINNER.

| a | b | winners | companies |
|---|---|---|---|
| Peter Thiel | Trae Stephens | 9 | OpenAI,SpaceX,Anduril Industries,Stripe,Figma,Scale AI,Palantir Technologies,Google DeepMind,Nubank |
| Elad Gil | Peter Thiel | 6 | OpenAI,SpaceX,Anduril Industries,Stripe,Figma,Scale AI |
| Elad Gil | Trae Stephens | 6 | OpenAI,SpaceX,Anduril Industries,Stripe,Figma,Scale AI |
| Elad Gil | Hemant Taneja | 3 | Anthropic,Anduril Industries,Stripe |
| Alfred Lin | Elad Gil | 2 | OpenAI,Anthropic |
| Daniel Gross | Elad Gil | 2 | SpaceX,Figma |
| Daniel Gross | Peter Thiel | 2 | SpaceX,Figma |
| Daniel Gross | Trae Stephens | 2 | SpaceX,Figma |
| Elad Gil | Elon Musk | 2 | OpenAI,SpaceX |
| Elad Gil | Ron Conway | 2 | Anthropic,Anduril Industries |
| Elad Gil | Vinod Khosla | 2 | OpenAI,Stripe |
| Elon Musk | Peter Thiel | 2 | OpenAI,SpaceX |
| Elon Musk | Trae Stephens | 2 | OpenAI,SpaceX |
| Hemant Taneja | Peter Thiel | 2 | Anduril Industries,Stripe |
| Hemant Taneja | Ron Conway | 2 | Anthropic,Anduril Industries |
| Hemant Taneja | Trae Stephens | 2 | Anduril Industries,Stripe |
| Joe Lonsdale | Peter Thiel | 2 | Anduril Industries,Palantir Technologies |
| Joe Lonsdale | Trae Stephens | 2 | Anduril Industries,Palantir Technologies |
| Peter Thiel | Vinod Khosla | 2 | OpenAI,Stripe |
| Trae Stephens | Vinod Khosla | 2 | OpenAI,Stripe |

`ANALYSIS` — co-occurrence on winners is **not** evidence of predictive skill until the same pairs are checked against the failure cohort. Question 15 does that.

## 5. Which investor combinations are mostly explained by shared networks?

`DERIVED` — companies where many backers collapse into few independent networks. `collapse_ratio = raw_people_count / distinct_information_clusters`; higher means the apparent breadth is one network wearing several hats.

| company | raw | clusters | collapse_ratio | weighted | indep_adj |
|---|---|---|---|---|---|
| Airloom | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Dioxycle | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Heart Aerospace | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Lilac Solutions | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Pachama | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Verdox | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Xcimer | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Yard Stick | 5 | 1 | 5.0 | 2.27 | 1.2 |
| Editas Medicine | 4 | 1 | 4.0 | 3.29 | 1.71 |
| Oculus VR | 4 | 1 | 4.0 | 2.72 | 1.54 |
| Commonwealth Fusion Systems | 10 | 3 | 3.33 | 5.39 | 3.17 |
| Anduril Industries | 13 | 4 | 3.25 | 7.64 | 4.55 |
| Figma | 6 | 2 | 3.0 | 3.68 | 2.11 |
| Antora Energy | 6 | 2 | 3.0 | 2.84 | 1.78 |
| Electra | 6 | 2 | 3.0 | 2.91 | 1.85 |
| Mill | 6 | 2 | 3.0 | 2.92 | 1.85 |
| Zap Energy | 6 | 2 | 3.0 | 2.52 | 1.46 |
| Beam Therapeutics | 6 | 2 | 3.0 | 3.25 | 1.84 |
| Palantir Technologies | 6 | 2 | 3.0 | 3.37 | 1.86 |
| Safe Superintelligence | 3 | 1 | 3.0 | 1.88 | 1.22 |

## 6. Which companies have the most genuinely independent backers?

`DERIVED` — most distinct network clusters after leave-one-out correlation.

| company | raw | clusters | domains | indep_adj | tier |
|---|---|---|---|---|---|
| Uber | 12 | 10 | 5 | 6.14 | TIER_D_5B_PLUS |
| Airbnb | 10 | 7 | 5 | 4.72 | TIER_D_5B_PLUS |
| X (formerly Twitter) | 7 | 7 | 5 | 3.82 | TIER_U_UNKNOWN |
| Etched | 8 | 7 | 1 | 2.8 | TIER_D_5B_PLUS |
| Perplexity | 8 | 6 | 4 | 5.24 | TIER_D_5B_PLUS |
| Stripe | 10 | 6 | 6 | 3.89 | TIER_D_5B_PLUS |
| OpenAI | 12 | 6 | 5 | 2.73 | TIER_D_5B_PLUS |
| Cognition | 10 | 5 | 5 | 4.71 | TIER_D_5B_PLUS |
| SpaceX | 11 | 5 | 5 | 4.48 | TIER_D_5B_PLUS |
| Planet Labs | 6 | 5 | 5 | 2.97 | TIER_D_5B_PLUS |
| Meta Platforms | 6 | 5 | 3 | 2.81 | TIER_D_5B_PLUS |
| Anduril Industries | 13 | 4 | 5 | 4.55 | TIER_D_5B_PLUS |
| Granola | 6 | 4 | 2 | 3.43 | TIER_C_1B_TO_5B |
| Vercel | 4 | 4 | 3 | 3.36 | TIER_D_5B_PLUS |
| The Boring Company | 8 | 4 | 4 | 3.35 | TIER_D_5B_PLUS |
| Anthropic | 8 | 4 | 4 | 3.34 | TIER_D_5B_PLUS |
| Physical Intelligence | 5 | 4 | 3 | 2.92 | TIER_D_5B_PLUS |
| Applied Intuition | 7 | 4 | 4 | 2.91 | TIER_D_5B_PLUS |
| Guardant Health | 4 | 4 | 3 | 2.58 | TIER_D_5B_PLUS |
| Altos Labs | 5 | 4 | 3 | 2.52 | TIER_U_UNKNOWN |
| Polymarket | 5 | 4 | 4 | 2.33 | TIER_D_5B_PLUS |
| Tesla | 5 | 4 | 4 | 2.32 | TIER_D_5B_PLUS |
| Cursor | 4 | 4 | 1 | 2.19 | TIER_D_5B_PLUS |
| Factory AI | 4 | 4 | 4 | 2.04 | TIER_U_UNKNOWN |
| Flock Safety | 5 | 4 | 2 | 2.03 | TIER_D_5B_PLUS |

## 7. Which companies under $500M have surprising elite overlap?

`FACT` + `DERIVED` — high overlap relative to how small the company still is.

| company | val | raw | strict | tech | clusters | elite_density |
|---|---|---|---|---|---|---|
| Editas Medicine | $405.45M | 4 | 4 | 4 | 1 | 0.1657 |
| Letta | $70.00M | 2 | 2 | 1 | 1 | 0.0877 |
| Prime Medicine | $238.76M | 2 | 1 | 1 | 1 | 0.0765 |
| Sana Biotechnology | $295.10M | 2 | 0 | 1 | 2 | 0.07 |
| Chegg | $81.05M | 2 | 0 | 0 | 2 | 0.0571 |
| 23andMe | $305.00M | 2 | 1 | 0 | 2 | 0.0377 |
| Convoy | $0 | 2 | 2 | 0 | 1 | — |
| Allogene Therapeutics, Inc. | $184.00M | 1 | 1 | 1 | 1 | 0.0449 |
| Caribou Biosciences, Inc. | $112.50M | 1 | 1 | 1 | 1 | 0.0437 |
| Deep Longevity, Inc | $3.79M | 1 | 1 | 1 | 1 | 0.0348 |
| Lamini | $325.00M | 1 | 1 | 1 | 1 | 0.0332 |
| Zymergen | $300.00M | 1 | 0 | 0 | 1 | 0.0323 |
| Liquid AI | $303.00M | 1 | 1 | 1 | 1 | 0.0311 |
| Pebble | $23.00M | 1 | 1 | 0 | 1 | 0.0279 |
| Rethink Robotics | $0 | 1 | 1 | 1 | 1 | — |

## 8. Which companies $500M–$1B have surprising elite overlap?

`FACT` + `DERIVED` — high overlap relative to how small the company still is.

| company | val | raw | strict | tech | clusters | elite_density |
|---|---|---|---|---|---|---|
| Google DeepMind | $650.00M | 5 | 2 | 1 | 3 | 0.1436 |
| Inflection AI | $650.00M | 3 | 1 | 0 | 3 | 0.0796 |
| /dev/agents | $500.00M | 1 | 1 | 1 | 1 | 0.0325 |

## 9. Which companies $1B–$5B have surprising elite overlap?

`FACT` + `DERIVED` — high overlap relative to how small the company still is.

| company | val | raw | strict | tech | clusters | elite_density |
|---|---|---|---|---|---|---|
| Granola | $1.50B | 6 | 4 | 4 | 4 | 0.2052 |
| Beam Therapeutics | $2.34B | 6 | 2 | 3 | 2 | 0.1509 |
| QuantumScape | $3.10B | 6 | 0 | 4 | 3 | 0.1089 |
| Character.AI | $2.70B | 4 | 3 | 3 | 2 | 0.1519 |
| Solugen | $2.05B | 4 | 0 | 0 | 2 | 0.0963 |
| Form Energy | $2.27B | 4 | 0 | 2 | 2 | 0.0652 |
| Weights & Biases | $1.25B | 3 | 2 | 1 | 2 | 0.1172 |
| FieldAI | $2.00B | 3 | 0 | 1 | 3 | 0.0988 |
| Zappos | $1.20B | 3 | 2 | 0 | 2 | 0.0902 |
| AMI Labs | $3.50B | 3 | 2 | 1 | 3 | 0.0837 |
| Astranis | $2.80B | 3 | 0 | 1 | 3 | 0.0596 |
| Stubhub / Viagogo | $2.25B | 2 | 2 | 0 | 1 | 0.0744 |
| Thumbtack | $3.20B | 2 | 2 | 0 | 1 | 0.0732 |
| Adept | $1.00B | 2 | 2 | 2 | 1 | 0.0662 |
| Netscape | $2.90B | 2 | 1 | 0 | 2 | 0.0522 |

## 10. Which unknown-valuation companies most deserve valuation work?

`FACT` — highest confirmed overlap with no sourced current valuation. These are the graph's blind spots and its best leads simultaneously.

| company | raw | strict | tech | clusters |
|---|---|---|---|---|
| Commonwealth Fusion Systems | 10 | 2 | 7 | 3 |
| X (formerly Twitter) | 7 | 2 | 2 | 7 |
| Heirloom | 7 | 0 | 3 | 3 |
| Mill | 6 | 1 | 3 | 2 |
| Antora Energy | 6 | 0 | 2 | 2 |
| Electra | 6 | 0 | 2 | 2 |
| Zap Energy | 6 | 0 | 3 | 2 |
| GRAIL, Inc. | 5 | 2 | 2 | 3 |
| Erebor | 5 | 1 | 1 | 3 |
| Altos Labs | 5 | 1 | 4 | 4 |
| Airloom | 5 | 0 | 2 | 1 |
| Dioxycle | 5 | 0 | 2 | 1 |
| Electric Hydrogen | 5 | 0 | 3 | 3 |
| Heart Aerospace | 5 | 0 | 2 | 1 |
| Lilac Solutions | 5 | 0 | 2 | 1 |
| Pachama | 5 | 0 | 2 | 1 |
| Verdox | 5 | 0 | 2 | 1 |
| Xcimer | 5 | 0 | 2 | 1 |
| Yard Stick | 5 | 0 | 2 | 1 |
| Watershed | 5 | 0 | 1 | 4 |
| Radiant Industries | 5 | 0 | 2 | 4 |
| SkyPilot | 4 | 4 | 3 | 2 |
| Chroma | 4 | 2 | 3 | 2 |
| Alphabet | 4 | 2 | 2 | 3 |
| Oculus VR | 4 | 2 | 1 | 1 |
| Varda Space Industries | 4 | 1 | 2 | 3 |
| Impulse Space | 4 | 1 | 1 | 3 |
| Albedo | 4 | 0 | 2 | 2 |
| Fervo Energy | 4 | 0 | 3 | 2 |
| H2Pro | 4 | 0 | 2 | 2 |

## 11. Which technically sophisticated people back obscure companies that conventional famous investors have missed?

`FACT` — companies with ≥1 technically elite backer and **zero** professional investors among their confirmed backers. This is the purest version of the project's thesis: technical judgement without venture consensus.

| company | val | tier | tech | raw | who |
|---|---|---|---|---|---|
| Etched | $10.30B | TIER_D_5B_PLUS | 7 | 8 | Amjad Masad; Andrej Karpathy; Fei-Fei Li; Geoffrey Hinton; Aidan Gomez; Arthur Mensch; Scott Wu |
| Granola | $1.50B | TIER_C_1B_TO_5B | 4 | 6 | Guillermo Rauch; Amjad Masad; Tobias Lutke; Nat Friedman |
| Editas Medicine | $405.45M | TIER_A_UNDER_500M | 4 | 4 | George Church; David Liu; Feng Zhang; Jennifer Doudna |
| Chroma | — | TIER_U_UNKNOWN | 3 | 4 | Guillermo Rauch; Amjad Masad; Nat Friedman |
| SkyPilot | — | TIER_U_UNKNOWN | 3 | 4 | Jeff Dean; Guillermo Rauch; Amjad Masad |
| EvolutionaryScale | — | TIER_U_UNKNOWN | 2 | 3 | Nat Friedman; Patrick Hsu |
| Adept | $1.00B | TIER_C_1B_TO_5B | 2 | 2 | Andrej Karpathy; David Luan |
| Mastra | — | TIER_U_UNKNOWN | 2 | 2 | Guillermo Rauch; Amjad Masad |
| Replit | — | TIER_U_UNKNOWN | 2 | 2 | Balaji Srinivasan; Amjad Masad |
| DNNresearch | — | TIER_U_UNKNOWN | 2 | 2 | Ilya Sutskever; Geoffrey Hinton |
| Thinking Machines Lab | $12.00B | TIER_D_5B_PLUS | 2 | 2 | Mira Murati; John Schulman |
| Pairwise Plants | — | TIER_U_UNKNOWN | 2 | 2 | David Liu; Feng Zhang |
| Arc Institute | — | TIER_U_UNKNOWN | 2 | 2 | Patrick Hsu; Silvana Konermann |
| Kitty Hawk | — | TIER_U_UNKNOWN | 2 | 2 | Larry Page; Sebastian Thrun |
| Function Health | — | TIER_U_UNKNOWN | 1 | 3 | Patrick Hsu |
| Earn.com | — | TIER_U_UNKNOWN | 1 | 3 | Balaji Srinivasan |
| Pulse | — | TIER_U_UNKNOWN | 1 | 2 | Nat Friedman |
| Composite | — | TIER_U_UNKNOWN | 1 | 2 | Nat Friedman |
| Sophont | — | TIER_U_UNKNOWN | 1 | 2 | Jeff Dean |
| Helical | — | TIER_U_UNKNOWN | 1 | 2 | Aidan Gomez |
| Letta | $70.00M | TIER_A_UNDER_500M | 1 | 2 | Jeff Dean |
| Manifold Bio | — | TIER_U_UNKNOWN | 1 | 2 | George Church |
| Mammoth Biosciences | — | TIER_U_UNKNOWN | 1 | 2 | Jennifer Doudna |
| Traversal | — | TIER_U_UNKNOWN | 1 | 2 | Patrick Hsu |
| NewLimit | — | TIER_U_UNKNOWN | 1 | 2 | Patrick Hsu |
| Digital Ocean | — | TIER_U_UNKNOWN | 1 | 2 | Balaji Srinivasan |
| Lambda | — | TIER_U_UNKNOWN | 1 | 1 | Andrej Karpathy |
| /dev/agents | $500.00M | TIER_B_500M_TO_1B | 1 | 1 | Andrej Karpathy |
| Lamini | $325.00M | TIER_A_UNDER_500M | 1 | 1 | Andrej Karpathy |
| Eureka Labs | — | TIER_U_UNKNOWN | 1 | 1 | Andrej Karpathy |

## 12. Which elite-person connections are newest?

`FACT` — most recent confirmed edges carrying a real date.

| date | person | company | rel | raw | tier |
|---|---|---|---|---|---|
| 2026-09 | Bill Gates | Republic Services, Inc. | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-09 | Marc Raibert | Dynamic Creatures | PERSONAL_ANGEL_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-07 | Jeff Dean | SkyPilot | PERSONAL_ANGEL_INVESTMENT | 4 | TIER_U_UNKNOWN |
| 2026-07 | Guillermo Rauch | SkyPilot | PERSONAL_ANGEL_INVESTMENT | 4 | TIER_U_UNKNOWN |
| 2026-07 | Amjad Masad | SkyPilot | PERSONAL_ANGEL_INVESTMENT | 4 | TIER_U_UNKNOWN |
| 2026-07 | Clement Delangue | SkyPilot | PERSONAL_ANGEL_INVESTMENT | 4 | TIER_U_UNKNOWN |
| 2026-06-30 | Michael Dell | SAFEHOLD INC | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Michael Dell | HAYWARD HLDGS INC | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Michael Dell | TOWNSQUARE MEDIA INC | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Natera | FAMILY_OFFICE_INVESTMENT | 2 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Insmed Inc | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Taiwan Semiconductor Manufac | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Amazon | FAMILY_OFFICE_INVESTMENT | 3 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Stmicroelectronics N V | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Fox Corp | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Ypf Sociedad Anonima | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Cdw Corp | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Bbb Foods Inc | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Alphabet | FAMILY_OFFICE_INVESTMENT | 4 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Seagate Technology Hldngs Pl | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | United Airls Hldgs Inc | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Sea Ltd | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | NEWAMSTERDAM PHARMA CO NV | FAMILY_OFFICE_INVESTMENT | 2 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Sandisk Corp | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | REVOLUTION MEDICINES INC | FAMILY_OFFICE_INVESTMENT | 2 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Bitdeer Technologies Group | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Crh Plc | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Delta Air Lines Inc | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |
| 2026-06-30 | Stanley Druckenmiller | Tesla | FAMILY_OFFICE_INVESTMENT | 5 | TIER_D_5B_PLUS |
| 2026-06-30 | Stanley Druckenmiller | Fluor Corp | FAMILY_OFFICE_INVESTMENT | 1 | TIER_U_UNKNOWN |

## 13. Which sectors show accelerating elite-network convergence?

`DERIVED` — new confirmed elite connections in the last 12 months, by sector. Only dated edges count, and sector is only known where a company record supplied it, so unlabelled sectors are under-counted rather than absent.

| sector | companies | new_connections_12m | new_connections_6m |
|---|---|---|---|
| (unlabelled) | 1665 | 89 | 87 |
| AI_SOFTWARE | 97 | 8 | 4 |
| ENERGY_CLIMATE | 64 | 3 | 0 |
| DEFENCE | 18 | 3 | 1 |
| ROBOTICS | 13 | 2 | 1 |
| SPACE | 18 | 1 | 1 |
| SEMICONDUCTORS | 5 | 1 | 0 |
| INDUSTRIAL_DEEPTECH | 78 | 1 | 0 |
| CONSUMER_INTERNET | 26 | 1 | 1 |
| BIOTECH_LIFESCIENCES | 55 | 1 | 1 |

## 14. Which past companies generated false-positive signals?

`FACT` — cohort companies labelled FAILURE or MEDIOCRE that nonetheless attracted confirmed elite backing. **These are the most important rows in the entire project**: they are what stops elite overlap being treated as a guarantee.

| company | outcome | peak_knowable_overlap | overlap_now | val |
|---|---|---|---|---|
| Character.AI | MEDIOCRE | 2 | 4 | $2.70B |
| Inflection AI | MEDIOCRE | 2 | 3 | $650.00M |
| 23andMe | FAILURE | 0 | 2 | $305.00M |
| Convoy | FAILURE | 0 | 2 | $0 |
| Clover Health | MEDIOCRE | 0 | 1 | $2.48B |
| Olive AI | FAILURE | 0 | 1 | $0 |
| Opendoor | MEDIOCRE | 0 | 1 | $2.57B |
| Pebble | FAILURE | 0 | 1 | $23.00M |
| Rethink Robotics | FAILURE | 0 | 1 | $0 |
| Stability AI | MEDIOCRE | 0 | 1 | — |
| Zymergen | FAILURE | 0 | 1 | $300.00M |

## 15. Does elite overlap retain signal after correlation and survivorship adjustment?

`FACT` — cohort coverage, which decides whether the question is answerable at all:

| arm | companies | with any confirmed edge | with any *knowable* overlap |
|---|---|---|---|
| `WINNER` | 16 | 16 | **4** |
| `FAILURE/MEDIOCRE` | 34 | 11 | **2** |

### The honest answer: **not yet, and the apparent separation is an artefact.**

`BACKTEST.md` shows winners averaging above failures at every date. **That number must not be believed.** Only 4 winner companies and 2 failure/mediocre companies have *any* knowable overlap at all (out of 16 and 34 in the cohort). At least 8 per arm would be needed before a difference in means meant anything, and the failure arm is the thinner of the two.

The separation is therefore measuring **which companies had edges collected**, not which companies were backed by elite people. And the reason is structural, not accidental:

- Collection followed **people**, and a person's portfolio is documented through the companies that *worked*. Portfolio pages list wins; press releases announce rounds into companies that went on to raise again.
- A failed company's investor list is frequently deleted along with its website, and nobody writes a retrospective naming the angels.
- So the failure arm is under-collected **by construction**, and any test run on it will flatter the signal.

**This is survivorship bias operating on the evidence itself**, one level below the usual concern about which companies get studied. Fixing it needs the negative controls' edges collected *deliberately* — going company-first through the failure list and reconstructing who backed them from archived announcements and filings — not waiting for them to appear while following people.

Until that is done, this project can say **where elite capital is concentrated today**, which is its stated purpose, but it **cannot yet say whether that concentration predicts anything**. Treating the rankings as predictive would be exactly the error the negative controls exist to prevent.

`SECONDARY_QUESTIONS.md` question 14 and `BACKTEST.md` carry the same caveat. The highest-priority next task in `research/state.json` is this gap.

