"""Canonical company entity resolution.

Two layers, both auditable:
  1. Deterministic normalisation (legal suffixes, punctuation, spacing, common
     corporate noise). Catches "OpenAI" / "Open AI" / "OpenAI, Inc." / "OpenAI Inc".
  2. A curated alias map in data/company_aliases.yaml for anything normalisation
     cannot see -- renames (Facebook -> Meta), and explicit
     DO-NOT-MERGE pairs so a subsidiary is never silently folded into its parent.

Everything a normaliser decides is written to `company_aliases` so a reviewer can
see exactly which raw string produced which canonical entity.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import yaml

LEGAL_SUFFIXES = [
    "com",
    "incorporated", "inc", "corporation", "corp", "company", "co",
    "limited", "ltd", "llc", "l l c", "plc", "lp", "llp", "gmbh", "ag", "sa",
    "sas", "bv", "nv", "ab", "oy", "as", "aps", "pte", "pty", "spa", "srl",
    "kk", "kabushiki kaisha", "holdings", "holding", "group", "technologies",
    "technology", "labs", "laboratories", "systems",
]
# Suffixes that are part of many real brand names -- only stripped when the
# remainder is still >= 3 chars and the name has >1 token.
SOFT_SUFFIXES = {"technologies", "technology", "labs", "laboratories",
                 "systems", "holdings", "holding", "group", "com"}
# Leading articles that some sources carry and others do not
# ("Boring Company" / "The Boring Company").
LEADING_NOISE = ("the ",)

_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)
_WS_RE = re.compile(r"\s+")


def _ascii_fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def normalise_name(name: str) -> str:
    """Loose key: lowercase, de-accented, punctuation-free, suffix-stripped."""
    s = _ascii_fold(name).lower().strip()
    s = s.replace("&", " and ")
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    for lead in LEADING_NOISE:
        if s.startswith(lead) and len(s) > len(lead) + 2:
            s = s[len(lead):].strip()
    changed = True
    while changed:
        changed = False
        for suf in sorted(LEGAL_SUFFIXES, key=len, reverse=True):
            if s.endswith(" " + suf):
                rest = s[: -(len(suf) + 1)].strip()
                if suf in SOFT_SUFFIXES and (len(rest) < 3 or " " not in s.strip()):
                    continue
                if rest:
                    s, changed = rest, True
                    break
    return _WS_RE.sub(" ", s).strip()


def ai_variants(key: str) -> set[str]:
    """Keys that should match a tight key across the ubiquitous "AI" suffix.

    "Decart" and "Decart AI" are one company; so are "Medra"/"Medra AI" and
    "Olive"/"Olive AI". Stripping "ai" inside normalise_name would be simpler but
    mangles the canonical key -- "Open AI" would become "open" and collide with
    anything called Open. So the suffix is handled as an ADDITIONAL match key,
    never as the entity's own key.
    """
    out = {key}
    if key.endswith("ai") and len(key) > 4:
        out.add(key[:-2])
    else:
        out.add(key + "ai")
    return out


def raw_key(name: str) -> str:
    """Tight key WITHOUT suffix stripping.

    Used for names a human has explicitly guarded in `do_not_merge`: those must
    resolve on their exact spelling, because the whole point is that suffix
    normalisation would wrongly collapse them ("Brilliant" vs "Brilliant Labs").
    """
    s = _ascii_fold(name).lower().strip().replace("&", " and ")
    s = _PUNCT_RE.sub(" ", s)
    return _WS_RE.sub("", s)


def tight_key(name: str) -> str:
    """Tightest key: normalised with all spaces removed.

    Collapses "Open AI" and "OpenAI", "Neuralink" and "Neura Link".
    Used only as a *candidate* matcher; never auto-merges across the
    do-not-merge list.
    """
    return normalise_name(name).replace(" ", "")


def slugify(name: str) -> str:
    s = normalise_name(name).replace(" ", "_")
    return re.sub(r"_+", "_", s).strip("_") or "unnamed"


class AliasMap:
    """Curated overrides layered on top of deterministic normalisation."""

    def __init__(self, path: str | Path | None = None):
        self.explicit: dict[str, str] = {}      # tight alias key -> canonical name
        self.do_not_merge: list[set[str]] = []  # groups that must stay distinct
        self.parent_of: dict[str, str] = {}     # canonical name -> parent name
        self.guarded_raw: set[str] = set()      # exact spellings that must not collapse
        if path and Path(path).exists():
            self.load(path)

    def load(self, path: str | Path) -> None:
        data = yaml.safe_load(Path(path).read_text()) or {}
        for entry in data.get("merges", []):
            canon = entry["canonical_name"]
            for a in entry.get("aliases", []):
                self.explicit[tight_key(a)] = canon
            self.explicit[tight_key(canon)] = canon
            if entry.get("parent_company"):
                self.parent_of[canon] = entry["parent_company"]
        for grp in data.get("do_not_merge", []):
            self.do_not_merge.append({tight_key(n) for n in grp["names"]})
            self.guarded_raw.update(raw_key(n) for n in grp["names"])

    def blocked(self, key_a: str, key_b: str) -> bool:
        if key_a == key_b:
            return False
        for grp in self.do_not_merge:
            if key_a in grp and key_b in grp:
                return True
        return False

    def is_guarded(self, name: str) -> bool:
        """Is this exact name a member of any do_not_merge group?"""
        return raw_key(name) in self.guarded_raw


class CompanyResolver:
    """Assigns a stable company_id to every raw company string it is shown."""

    def __init__(self, alias_map: AliasMap | None = None):
        self.alias_map = alias_map or AliasMap()
        self._by_tight: dict[str, str] = {}      # tight key -> company_id
        self._by_alt: dict[str, str] = {}        # "AI"-variant key -> company_id
        self._canonical: dict[str, str] = {}     # company_id -> canonical name
        self._raw_seen: dict[str, str] = {}      # raw string -> company_id
        self.audit: list[dict] = []

    def resolve(self, raw_name: str, resolved_by: str = "auto") -> str:
        raw = (raw_name or "").strip()
        if raw in self._raw_seen:
            return self._raw_seen[raw]
        # A name a human has explicitly guarded resolves on its exact spelling,
        # so suffix normalisation cannot collapse it into a neighbour. Without
        # this, do_not_merge was documented but never enforced at resolve time.
        guarded = self.alias_map.is_guarded(raw)
        tk = raw_key(raw) if guarded else tight_key(raw)
        canonical = self.alias_map.explicit.get(tight_key(raw), raw)
        ck = raw_key(canonical) if self.alias_map.is_guarded(canonical) else tight_key(canonical)

        cid = self._by_tight.get(ck)
        if cid is None and tk != ck:
            cid = self._by_tight.get(tk)
        if cid is None and not guarded:
            for alt in ai_variants(ck) | ai_variants(tk):
                cand = self._by_tight.get(alt) or self._by_alt.get(alt)
                if cand and not self.alias_map.blocked(tk, alt):
                    cid = cand
                    break
        if cid is None:
            cid = "c_" + slugify(canonical)
            # collision guard: two genuinely different names slugging identically
            n = 1
            while cid in self._canonical and tight_key(self._canonical[cid]) != ck:
                n += 1
                cid = f"c_{slugify(canonical)}_{n}"
            self._canonical[cid] = canonical
            self._by_tight[ck] = cid
        self._by_tight.setdefault(tk, cid)
        if not guarded:
            for alt in ai_variants(ck) | ai_variants(tk):
                self._by_alt.setdefault(alt, cid)
        self._raw_seen[raw] = cid
        self.audit.append({
            "alias_norm": tk, "alias_raw": raw, "company_id": cid,
            "resolved_by": resolved_by,
            "note": "explicit alias map" if tk in self.alias_map.explicit
                    else ("exact" if tk == ck else "normalised"),
        })
        return cid

    def canonical_name(self, company_id: str) -> str:
        return self._canonical.get(company_id, company_id)

    def set_canonical(self, company_id: str, name: str) -> None:
        self._canonical[company_id] = name
        self._by_tight[tight_key(name)] = company_id

    def collision_report(self) -> list[dict]:
        """Names that landed in the same entity but look suspiciously different,
        and names in different entities that a human may want to merge."""
        out = []
        by_cid: dict[str, set[str]] = {}
        for a in self.audit:
            by_cid.setdefault(a["company_id"], set()).add(a["alias_raw"])
        for cid, raws in by_cid.items():
            if len(raws) > 1:
                out.append({"kind": "merged", "company_id": cid,
                            "canonical": self.canonical_name(cid),
                            "raw_names": sorted(raws)})
        # near-miss detection across entities
        keys = sorted(self._by_tight.items())
        for i, (ka, ca) in enumerate(keys):
            for kb, cb in keys[i + 1:]:
                if ca == cb or self.alias_map.blocked(ka, kb):
                    continue
                if len(ka) >= 6 and len(kb) >= 6 and (ka.startswith(kb) or kb.startswith(ka)):
                    out.append({"kind": "near_miss", "company_id": ca, "other_id": cb,
                                "canonical": self.canonical_name(ca),
                                "other": self.canonical_name(cb)})
        return out
