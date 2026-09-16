"""UD -> UniMorph tag conversion: the reverse of UM2UD_mapper.py's UM -> UD
direction. Kept in its own module so the two directions stay easy to tell
apart, but built directly on top of UM2UD_mapper's UM2UD_values -- that
table is the single source of truth for which (UD feature, UD value) pairs
a UM tag corresponds to; this module only adds the reverse index and the
UD-feature-dict -> UM-tag-list conversion built on top of it.

Only handles plain (non-layered/bracketed) UD features. A bracketed UD
feature name like "Number[obj]" is not a UniMorph or Universal Dependencies
convention -- it's specific to whatever consumer produced the bracket (e.g.
a treebank's own argument-marking annotation style, or a downstream
project's own encoding for round-tripping such a bracket through a
UM-tag-shaped string). Converting those is that consumer's responsibility,
not this package's -- see multiblimp.ud2um.ud_feats_to_um_tags for an
example of layering that kind of project-specific handling on top of the
plain conversion here.
"""
from typing import Dict, List, Optional, Tuple

from .UM2UD_mapper import UM2UD_values

# Pass 1: (feature, value) -> UM tag, via each tag's first dict item (matches
# UM2UD_values' longest-tag-first order, e.g. Mood/Ind -> "IND" over "REAL").
UD2UM_values: Dict[Tuple[str, str], str] = {
    tuple(v.items())[0]: k for k, v in UM2UD_values.items() if v.items()
}
# Pass 2: backfill (feature, value) pairs a compound tag sets beyond its
# first (e.g. VerbForm/Part for "V.PTCP"), without overwriting pass 1's picks.
for _um_tag, _ud_feats in UM2UD_values.items():
    for _feat, _val in _ud_feats.items():
        UD2UM_values.setdefault((_feat, _val), _um_tag)


def fuses_upos(tag: str) -> bool:
    """True if `tag` (or a "/" disjunction component) is a compound UM tag
    that already implies a upos, e.g. "V.PTCP" implies upos=VERB."""
    return any(UM2UD_values.get(sub, {}).get("upos") is not None for sub in tag.split("/"))


def upos_to_um_tag(upos: str) -> Optional[str]:
    return UD2UM_values.get(("upos", upos))


def feat_val_to_um_tag(feat: str, raw_val: str) -> Optional[str]:
    """One UD feature's raw value string (comma-valued for syncretic/
    disjunctive forms, e.g. "Masc,Fem") -> a single UM tag, "/"-joining
    disjunctive UM tags the same way UniMorph itself encodes them (dedup'd,
    first-seen order kept). None if none of the comma-separated values have
    a UD2UM entry for `feat`.
    """
    sub_tags = [
        UD2UM_values[(feat, val)]
        for val in raw_val.split(",")
        if (feat, val) in UD2UM_values
    ]
    if not sub_tags:
        return None
    return "/".join(dict.fromkeys(sub_tags))


def ud_feats_to_um_tags(upos: str, feats: Optional[Dict[str, str]]) -> Optional[List[str]]:
    """Convert a UD token's upos + plain (unbracketed) feats into real
    UniMorph tag strings (e.g. ["V", "PST", "3", "SG"]). Comma-valued UD
    features (syncretic forms) map to UM's "/" disjunction syntax via
    feat_val_to_um_tag. Values with no UD2UM entry are skipped. Returns None
    if upos itself has no UM counterpart (PUNCT, SYM, X, ...).
    """
    upos_tag = upos_to_um_tag(upos)
    if upos_tag is None:
        return None

    tags = [
        tag for feat, raw_val in (feats or {}).items()
        if (tag := feat_val_to_um_tag(feat, raw_val)) is not None
    ]

    if not any(fuses_upos(tag) for tag in tags):
        tags.insert(0, upos_tag)

    return tags or None
