# PERSON ↔ PERSON NETWORK

The purpose is **not** social mapping. It is to test whether apparently independent investment signals actually come from one information network. Personal friendship is never inferred without evidence.

## Asserted correlation links (evidence-backed)

| type | count |
|---|---|
| `CO_FOUNDED_COMPANY` | 39 |
| `FREQUENT_CO_INVESTMENT` | 34 |
| `SAME_FOUNDER_ECOSYSTEM` | 32 |
| `SAME_FORMER_EMPLOYER` | 30 |
| `SAME_FIRM` | 30 |
| `SAME_BOARD` | 10 |
| `SAME_SYNDICATE` | 7 |
| `FAMILY_RELATIONSHIP` | 4 |
| `SAME_INSTITUTIONAL_SOURCE` | 2 |

## Derived co-investment links

Two people are linked when they share **≥3** companies with confirmed edges. Derived links are stored separately (`derived=1`) and are recomputed with the scored company removed, so a company can never inflate its own backers' apparent correlation.

| A | B | strength | evidence |
|---|---|---|---|
| Albert Wenger | Fred Wilson | 0.75 | Derived from this graph: 47 companies with confirmed edges from both. |
| Ali Partovi | Hadi Partovi | 0.75 | Derived from this graph: 62 companies with confirmed edges from both. |
| Bill Gates | Carmichael Roberts | 0.75 | Derived from this graph: 103 companies with confirmed edges from both. |
| Bill Gates | Chris Sacca | 0.75 | Derived from this graph: 14 companies with confirmed edges from both. |
| Bill Gates | Crystal Sacca | 0.75 | Derived from this graph: 14 companies with confirmed edges from both. |
| Bill Gates | Eric Toone | 0.75 | Derived from this graph: 103 companies with confirmed edges from both. |
| Robert Nelsen | Eli Casdin | 0.75 | Derived from this graph: 9 companies with confirmed edges from both. |
| Robert Nelsen | Kristina Burow | 0.75 | Derived from this graph: 9 companies with confirmed edges from both. |
| Carmichael Roberts | Chris Sacca | 0.75 | Derived from this graph: 14 companies with confirmed edges from both. |
| Carmichael Roberts | Crystal Sacca | 0.75 | Derived from this graph: 14 companies with confirmed edges from both. |
| Carmichael Roberts | Eric Toone | 0.75 | Derived from this graph: 103 companies with confirmed edges from both. |
| Chris Sacca | Crystal Sacca | 0.75 | Derived from this graph: 105 companies with confirmed edges from both. |
| Chris Sacca | Eric Toone | 0.75 | Derived from this graph: 14 companies with confirmed edges from both. |
| Crystal Sacca | Eric Toone | 0.75 | Derived from this graph: 14 companies with confirmed edges from both. |
| Daniel Gross | Nat Friedman | 0.75 | Derived from this graph: 9 companies with confirmed edges from both. |
| Peter Thiel | Trae Stephens | 0.75 | Derived from this graph: 38 companies with confirmed edges from both. |
| Elad Gil | Peter Thiel | 0.73 | Derived from this graph: 8 companies with confirmed edges from both. |
| Elad Gil | Trae Stephens | 0.73 | Derived from this graph: 8 companies with confirmed edges from both. |
| Maryanna Saenko | Steve Jurvetson | 0.73 | Derived from this graph: 8 companies with confirmed edges from both. |
| Daniel Gross | Elad Gil | 0.65 | Derived from this graph: 7 companies with confirmed edges from both. |
| Elad Gil | Hemant Taneja | 0.65 | Derived from this graph: 7 companies with confirmed edges from both. |
| Elad Gil | Ron Conway | 0.65 | Derived from this graph: 7 companies with confirmed edges from both. |
| Elad Gil | Vinod Khosla | 0.57 | Derived from this graph: 6 companies with confirmed edges from both. |
| Joe Lonsdale | Peter Thiel | 0.57 | Derived from this graph: 6 companies with confirmed edges from both. |
| Alfred Lin | Vinod Khosla | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Bill Gates | Vinod Khosla | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Elon Musk | Peter Thiel | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Hemant Taneja | Ron Conway | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Jessica Livingston | Paul Graham | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Josh Wolfe | Peter Thiel | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Nikolay Storonsky | Ron Conway | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Peter Thiel | Ron Conway | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Peter Thiel | Vinod Khosla | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Ron Conway | Trae Stephens | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Trae Stephens | Vinod Khosla | 0.49 | Derived from this graph: 5 companies with confirmed edges from both. |
| Alfred Lin | Ali Partovi | 0.41 | Derived from this graph: 4 companies with confirmed edges from both. |
| Alfred Lin | Elad Gil | 0.41 | Derived from this graph: 4 companies with confirmed edges from both. |
| Ali Partovi | Elad Gil | 0.41 | Derived from this graph: 4 companies with confirmed edges from both. |
| Amjad Masad | Guillermo Rauch | 0.41 | Derived from this graph: 4 companies with confirmed edges from both. |
| Aydin Senkut | Ron Conway | 0.41 | Derived from this graph: 4 companies with confirmed edges from both. |

## Which combinations appear together most often

| A | B | shared companies |
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
| Robert Nelsen | Eli Casdin | 9 |
| Robert Nelsen | Kristina Burow | 9 |
| Daniel Gross | Nat Friedman | 9 |
| Elad Gil | Peter Thiel | 8 |
| Elad Gil | Trae Stephens | 8 |
| Maryanna Saenko | Steve Jurvetson | 8 |
| Daniel Gross | Elad Gil | 7 |
| Elad Gil | Hemant Taneja | 7 |
| Elad Gil | Ron Conway | 7 |
| Elad Gil | Vinod Khosla | 6 |
| Joe Lonsdale | Peter Thiel | 6 |
| Alfred Lin | Vinod Khosla | 5 |
| Bill Gates | Vinod Khosla | 5 |
| Elon Musk | Peter Thiel | 5 |
| Hemant Taneja | Ron Conway | 5 |
| Jessica Livingston | Paul Graham | 5 |
| Josh Wolfe | Peter Thiel | 5 |
| Nikolay Storonsky | Ron Conway | 5 |
| Peter Thiel | Ron Conway | 5 |
| Peter Thiel | Vinod Khosla | 5 |
| Ron Conway | Trae Stephens | 5 |
| Trae Stephens | Vinod Khosla | 5 |
| Alfred Lin | Ali Partovi | 4 |
| Alfred Lin | Elad Gil | 4 |
| Ali Partovi | Elad Gil | 4 |
| Amjad Masad | Guillermo Rauch | 4 |
| Aydin Senkut | Ron Conway | 4 |
