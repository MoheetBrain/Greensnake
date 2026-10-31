"""The PERSON <-> PERSON graph, and the clustering that drives independence.

Ten investors from one network are not ten independent signals. This module
answers "how many genuinely distinct information sources back this company?".

Two kinds of cluster are computed, and they are NOT the same thing:

  NETWORK cluster   -- connected components of the person<->person correlation
                       graph (same firm, co-founded, family, shared employer,
                       repeated co-investment). Drives INDEPENDENCE_ADJUSTED.
  DOMAIN cluster    -- which information domain a person reads the world from
                       (AI research, semiconductors, fusion, defence, ...).
                       Drives CROSS-DOMAIN analysis.

CIRCULARITY GUARD. Co-investment correlation is derived from this same graph, so
scoring company X with a correlation link that exists *because of* company X
would double-count. Every cluster computation for company X therefore rebuilds
derived co-investment edges with X removed from the evidence (leave-one-out).
"""
from __future__ import annotations

import json
from collections import defaultdict

from ..core.enums import CORRELATION_STRENGTH_DEFAULT

# Threshold at which a correlation link is treated as "same information source".
CLUSTER_THRESHOLD = 0.50
# How many shared confirmed companies before two people count as co-investors.
CO_INVESTMENT_MIN_SHARED = 3
CO_INVESTMENT_MAX_STRENGTH = 0.75

# domain -> information cluster label
DOMAIN_TO_CLUSTER = {
    "AI_SOFTWARE": "AI",
    "SEMICONDUCTORS": "SEMICONDUCTORS",
    "QUANTUM": "QUANTUM",
    "ENERGY_CLIMATE": "ENERGY_CLIMATE",
    "MATERIALS": "MATERIALS_MINING",
    "INDUSTRIAL_DEEPTECH": "INDUSTRIAL",
    "BIOTECH_LIFESCIENCES": "BIO",
    "HEALTHCARE_SERVICES": "HEALTHCARE",
    "AGRICULTURE_FOOD": "AGRIFOOD",
    "SPACE": "SPACE",
    "DEFENCE": "DEFENCE",
    "ROBOTICS": "ROBOTICS",
    "TRANSPORT_MOBILITY": "MOBILITY",
    "FINTECH": "FINTECH",
    "CRYPTO": "CRYPTO",
    "CONSUMER_INTERNET": "CONSUMER",
    "GENERALIST": "GENERALIST",
}
# archetype overlay -- a professional allocator reads the world through capital
# markets regardless of the sector label they attach to a deal.
ARCHETYPE_CLUSTER = {
    "PROFESSIONAL_INVESTOR": "VENTURE_CAPITAL",
    "FAMILY_OFFICE_PRINCIPAL": "PRIVATE_CAPITAL",
}


def person_domain_clusters(con) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for r in con.execute("SELECT person_key, domains, archetypes FROM people"):
        doms = json.loads(r["domains"] or "[]")
        arch = json.loads(r["archetypes"] or "[]")
        cl = {DOMAIN_TO_CLUSTER.get(d, "OTHER") for d in doms}
        # Only add the capital-markets overlay for people with NO technical or
        # founding archetype -- otherwise every founder-investor collapses to "VC".
        if not ({"RESEARCH_SCIENTIST", "ACADEMIC", "FOUNDER_OPERATOR"} & set(arch)):
            for a in arch:
                if a in ARCHETYPE_CLUSTER:
                    cl.add(ARCHETYPE_CLUSTER[a])
        out[r["person_key"]] = cl or {"OTHER"}
    return out


def person_primary_cluster(con) -> dict[str, str]:
    """ONE information cluster per person: the lens they actually read through.

    Counting the union of every backer's domains overstates diversity -- seven
    people with four domains each can "cover" a dozen domains while all reading
    the same three sources. Cross-domain diversity is therefore counted over
    PRIMARY clusters, one per person.

    A pure capital allocator's primary lens is capital markets, whatever sector
    label is on the deal. Anyone with a research, academic or founding archetype
    keeps their leading domain, because they read that domain directly.
    """
    out: dict[str, str] = {}
    for r in con.execute("SELECT person_key, domains, archetypes FROM people"):
        doms = json.loads(r["domains"] or "[]")
        arch = set(json.loads(r["archetypes"] or "[]"))
        if not (arch & {"RESEARCH_SCIENTIST", "ACADEMIC", "FOUNDER_OPERATOR"}):
            overlay = next((ARCHETYPE_CLUSTER[a] for a in sorted(arch)
                            if a in ARCHETYPE_CLUSTER), None)
            if overlay:
                out[r["person_key"]] = overlay
                continue
        out[r["person_key"]] = DOMAIN_TO_CLUSTER.get(doms[0], "OTHER") if doms else "OTHER"
    return out


def _confirmed_company_sets(con) -> dict[str, set[str]]:
    d: dict[str, set[str]] = defaultdict(set)
    for r in con.execute(
            "SELECT person_key, company_id FROM person_company_edges WHERE is_confirmed=1"):
        d[r["person_key"]].add(r["company_id"])
    return d


def derive_co_investment(con, write: bool = True) -> list[tuple[str, str, float, int]]:
    """FREQUENT_CO_INVESTMENT links derived from the graph itself (global view).

    Stored with derived=1 so the asserted network stays separable from the
    inferred one. Never used for a company's own score without leave-one-out.
    """
    sets = _confirmed_company_sets(con)
    keys = sorted(sets)
    out = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            shared = sets[a] & sets[b]
            if len(shared) >= CO_INVESTMENT_MIN_SHARED:
                s = min(CO_INVESTMENT_MAX_STRENGTH, 0.25 + 0.08 * (len(shared) - CO_INVESTMENT_MIN_SHARED + 1))
                out.append((a, b, s, len(shared)))
    if write:
        con.execute("DELETE FROM investor_relationships WHERE derived=1")
        for a, b, s, n in out:
            con.execute(
                "INSERT OR REPLACE INTO investor_relationships (rel_id, person_key_a,"
                " person_key_b, correlation_type, strength, evidence, source_url, derived)"
                " VALUES (?,?,?,?,?,?,NULL,1)",
                (f"d_{a}__{b}", a, b, "FREQUENT_CO_INVESTMENT", s,
                 f"Derived from this graph: {n} companies with confirmed edges from both."))
        con.commit()
    return out


class CorrelationGraph:
    """Adjacency with per-company leave-one-out recomputation of derived links."""

    def __init__(self, con):
        self.asserted: dict[tuple[str, str], float] = {}
        for r in con.execute(
                "SELECT person_key_a, person_key_b, correlation_type, strength"
                " FROM investor_relationships WHERE derived=0"):
            a, b = sorted([r["person_key_a"], r["person_key_b"]])
            s = r["strength"] or CORRELATION_STRENGTH_DEFAULT.get(r["correlation_type"], 0.4)
            self.asserted[(a, b)] = max(self.asserted.get((a, b), 0.0), float(s))
        self.company_sets = _confirmed_company_sets(con)

    def _derived_strength(self, a: str, b: str, exclude_company: str | None) -> float:
        sa = self.company_sets.get(a, set())
        sb = self.company_sets.get(b, set())
        shared = sa & sb
        if exclude_company:
            shared = shared - {exclude_company}
        n = len(shared)
        if n < CO_INVESTMENT_MIN_SHARED:
            return 0.0
        return min(CO_INVESTMENT_MAX_STRENGTH,
                   0.25 + 0.08 * (n - CO_INVESTMENT_MIN_SHARED + 1))

    def strength(self, a: str, b: str, exclude_company: str | None = None) -> float:
        a, b = sorted([a, b])
        return max(self.asserted.get((a, b), 0.0),
                   self._derived_strength(a, b, exclude_company))

    def clusters(self, people: list[str], exclude_company: str | None = None,
                 co_founders: set[str] | None = None) -> list[list[str]]:
        """Connected components among `people` at CLUSTER_THRESHOLD.

        `co_founders` are people holding FOUNDER_EQUITY in the company being
        scored. They are ALWAYS unioned, because founding a company together is
        one joint decision, not N independent judgements about it. Without this
        rule the outcome depends on whether some correlation record happens to
        cite the company -- correct by accident, and wrong the moment the
        evidence is worded differently.
        """
        people = sorted(set(people))
        parent = {p: p for p in people}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry:
                parent[ry] = rx

        cf = sorted((co_founders or set()) & set(people))
        for a, b in zip(cf, cf[1:]):
            union(a, b)
        for i, a in enumerate(people):
            for b in people[i + 1:]:
                if self.strength(a, b, exclude_company) >= CLUSTER_THRESHOLD:
                    union(a, b)
        groups: dict[str, list[str]] = defaultdict(list)
        for p in people:
            groups[find(p)].append(p)
        return [sorted(v) for v in groups.values()]


def independence_adjusted(clusters: list[list[str]], weights: dict[str, float],
                          delta: float = 0.35) -> float:
    """Sum over clusters: the strongest member counts in full, every additional
    member of the SAME information network counts at `delta`.

        IA = sum_c [ max_{p in c} w_p  +  delta * sum_{p in c, p != argmax} w_p ]

    delta = 1.0 reproduces the raw weighted score (no discount);
    delta = 0.0 collapses each network to its single strongest voice.
    The raw factual counts are always preserved alongside this.
    """
    total = 0.0
    for c in clusters:
        ws = sorted((weights.get(p, 0.0) for p in c), reverse=True)
        if not ws:
            continue
        total += ws[0] + delta * sum(ws[1:])
    return total
