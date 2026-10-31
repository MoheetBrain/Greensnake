# PEOPLE CLASSIFICATION REVIEW

`signal_class` in `research/people/people_universe.yaml` is a **prior**, set from public reputation before any edge was collected. This file tests those priors against what the graph actually produced.

Two derived quantities do the testing, and neither is hand-set:

- **`investment_visibility` (0–5)** — how much of this person's portfolio could actually be reconstructed, from confirmed company count and the Tier-1 share of their evidence.
- **`herding_risk` (0–1)** — how crowded their book is with the rest of the pool.

**Nothing here is applied automatically.** A scoring layer that rewrites its own inputs is not auditable. These are proposals for a human.

> An important asymmetry: low visibility is a statement about **the evidence**, not about the person. Several people were included precisely to measure how much this method cannot see. Demoting them is the method admitting its blind spot, not a judgement that they are unimportant.

## Proposed revisions (18)

| person | from | to | visibility | confirmed cos | reason |
|---|---|---|---|---|---|
| **Jensen Huang** | `CORE_HIGH_SIGNAL` | `WATCHLIST` | 0.0 | 0 | prior says core, but only 0 confirmed companies could be reconstructed (visibility 0.0). Their real activity is invisible to this method, so weighting them as a core signal over-weights the little we can see. |
| **Mira Murati** | `CORE_HIGH_SIGNAL` | `WATCHLIST` | 1.0 | 1 | prior says core, but only 1 confirmed companies could be reconstructed (visibility 1.0). Their real activity is invisible to this method, so weighting them as a core signal over-weights the little we can see. |
| **Aidan Gomez** | `EXTENDED_SIGNAL` | `DOMAIN_SPECIALIST` | 2.5 | 3 | technical band 5 with a small book (3); the value here is domain signal, not general investing signal, and the classes should say so. |
| **Arthur Mensch** | `EXTENDED_SIGNAL` | `DOMAIN_SPECIALIST` | 2.0 | 2 | technical band 5 with a small book (2); the value here is domain signal, not general investing signal, and the classes should say so. |
| **Bilal Zuberi** | `EXTENDED_SIGNAL` | `DOMAIN_SPECIALIST` | 2.0 | 2 | technical band 5 with a small book (2); the value here is domain signal, not general investing signal, and the classes should say so. |
| **Krishna Yeshwant** | `EXTENDED_SIGNAL` | `DOMAIN_SPECIALIST` | 3.0 | 4 | technical band 5 with a small book (4); the value here is domain signal, not general investing signal, and the classes should say so. |
| **Sebastian Thrun** | `EXTENDED_SIGNAL` | `DOMAIN_SPECIALIST` | 2.75 | 4 | technical band 5 with a small book (4); the value here is domain signal, not general investing signal, and the classes should say so. |
| **Vijay Pande** | `EXTENDED_SIGNAL` | `DOMAIN_SPECIALIST` | 3.0 | 3 | technical band 5 with a small book (3); the value here is domain signal, not general investing signal, and the classes should say so. |
| **Alexandr Wang** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 2.0 | 2 | reconstructable book is thin (2 companies, visibility 2.0); the prior outruns the evidence. |
| **Bernard Arnault** | `WATCHLIST` | `EXTENDED_SIGNAL` | 4.0 | 10 | prior assumed poor visibility, but 10 confirmed companies were reconstructed (visibility 4.0). The pessimism was wrong. |
| **Dario Amodei** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 1.5 | 1 | reconstructable book is thin (1 companies, visibility 1.5); the prior outruns the evidence. |
| **Demis Hassabis** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 2.0 | 1 | reconstructable book is thin (1 companies, visibility 2.0); the prior outruns the evidence. |
| **Greg Brockman** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 2.0 | 2 | reconstructable book is thin (2 companies, visibility 2.0); the prior outruns the evidence. |
| **John Collison** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 2.0 | 1 | reconstructable book is thin (1 companies, visibility 2.0); the prior outruns the evidence. |
| **Mustafa Suleyman** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 1.33 | 2 | reconstructable book is thin (2 companies, visibility 1.33); the prior outruns the evidence. |
| **Patrick Collison** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 2.0 | 1 | reconstructable book is thin (1 companies, visibility 2.0); the prior outruns the evidence. |
| **Stanley Druckenmiller** | `WATCHLIST` | `EXTENDED_SIGNAL` | 5.0 | 84 | prior assumed poor visibility, but 84 confirmed companies were reconstructed (visibility 5.0). The pessimism was wrong. |
| **Yuri Milner** | `CORE_HIGH_SIGNAL` | `EXTENDED_SIGNAL` | 1.67 | 2 | reconstructable book is thin (2 companies, visibility 1.67); the prior outruns the evidence. |

## Visibility distribution by prior class

| prior class | n | median visibility | median confirmed companies | n with zero edges |
|---|---|---|---|---|
| `CORE_HIGH_SIGNAL` | 47 | 3.78 | 9 | 1 |
| `EXTENDED_SIGNAL` | 80 | 3.0 | 6 | 5 |
| `DOMAIN_SPECIALIST` | 42 | 2.33 | 3 | 4 |
| `WATCHLIST` | 19 | 2.0 | 2 | 2 |
| `LOW_SIGNAL_OR_POOR_VISIBILITY` | 2 | 2.0 | 2 | 0 |

## Most crowded books (highest herding risk)

`ANALYSIS` — a crowded book is not a bad book. It means this person's positions carry less *independent* information, because the rest of the pool is already in them. The independence adjustment already discounts this at the company level; the column exists so the effect is visible at the person level too.

| person | herding risk | visibility | confirmed companies |
|---|---|---|---|
| Alexander Karp | 0.827 | 2.0 | 1 |
| Eric Toone | 0.814 | 5.0 | 105 |
| Dario Amodei | 0.795 | 1.5 | 1 |
| Elon Musk | 0.795 | 2.86 | 7 |
| Brian Schimpf | 0.795 | 2.0 | 1 |
| Stephen Cohen | 0.795 | 2.0 | 1 |
| Sergey Brin | 0.795 | 2.0 | 1 |
| Daniela Amodei | 0.763 | 1.5 | 1 |
| Richard Klausner | 0.763 | 3.0 | 4 |
| Demis Hassabis | 0.732 | 2.0 | 1 |
| Mustafa Suleyman | 0.732 | 1.33 | 2 |
| Noam Shazeer | 0.732 | 2.0 | 1 |
| Alexandr Wang | 0.732 | 2.0 | 2 |
| Arthur Mensch | 0.732 | 2.0 | 2 |
| Patrick Collison | 0.732 | 2.0 | 1 |

## People the graph could not see at all

`FACT` — tracked people with **no confirmed edge**. For the WATCHLIST and LOW_SIGNAL entries this was the expected result and is the finding: it calibrates the method's floor. For anyone else it is a coverage gap.

| person | prior class | interpretation |
|---|---|---|
| Brad Gerstner | `EXTENDED_SIGNAL` | coverage gap — worth another pass |
| Chase Coleman | `EXTENDED_SIGNAL` | coverage gap — worth another pass |
| Chris Olah | `DOMAIN_SPECIALIST` | coverage gap — worth another pass |
| Jared Kaplan | `DOMAIN_SPECIALIST` | coverage gap — worth another pass |
| Jensen Huang | `CORE_HIGH_SIGNAL` | coverage gap — worth another pass |
| Kevin Scott | `WATCHLIST` | expected — included to measure the visibility floor |
| Lee Fixel | `EXTENDED_SIGNAL` | coverage gap — worth another pass |
| Lisa Su | `DOMAIN_SPECIALIST` | coverage gap — worth another pass |
| Michael Moritz | `EXTENDED_SIGNAL` | coverage gap — worth another pass |
| Philippe Laffont | `EXTENDED_SIGNAL` | coverage gap — worth another pass |
| Satya Nadella | `WATCHLIST` | expected — included to measure the visibility floor |
| Shane Legg | `DOMAIN_SPECIALIST` | coverage gap — worth another pass |
