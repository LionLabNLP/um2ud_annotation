"""UD -> UniMorph tag conversion, the reverse of UM2UD_mapper.py: a reverse index of UM2UD_values (the
single source of truth for which UD pairs a UM tag stands for) and the UD feature dict -> UM tag list
conversion. Plain UD features only: bracketed names (Number[obj]) are the consumer's to convert."""
from typing import Dict, List, Optional, Tuple

from .UD_gaps import ud_gaps   # the UD values with no UM tag, see UD_gaps.py
from .UM2UD_mapper import UM2UD_values, _notice

# Pass 1: (feature, value) -> UM tag, via each tag's first dict item (UM2UD_values is ordered longest
# tag first, e.g. Mood=Ind -> "IND" over "REAL"). Several UM tags can share one UD pair (Aspect=Perf is
# PFV and PRF); all are kept, "/"-joined like a disjunctive UM tag, so a later form+lemma lookup finds
# the real one. upos collisions keep a single pick: joining them would put a disjunction on every token
# of that upos (ADJ's collision with Korean's ADJ.MSDR/ADJ.PTCP/ADJ.CVB broke every language's plain
# adjectives); Korean's deverbal adjectives stay a known gap.
# UM tags that map to UD but are specific to one language, so UD -> UM must not offer them as the
# UniMorph spelling of the UD value (NPST would turn every Tense=Pres into "NPST/PRS")
_NO_REVERSE = {"NPST", "HYP"}

_pair_to_tags: Dict[Tuple[str, str], List[str]] = {}
for _um_tag, _ud_feats in UM2UD_values.items():
    if not _ud_feats.items() or _um_tag in _NO_REVERSE:
        continue
    _pair_to_tags.setdefault(tuple(_ud_feats.items())[0], []).append(_um_tag)
UD2UM_values: Dict[Tuple[str, str], str] = {
    # upos keeps the last of its colliding tags in UM2UD_values order
    pair: (tags[-1] if pair[0] == "upos" else "/".join(dict.fromkeys(tags)))
    for pair, tags in _pair_to_tags.items()
}
# Pass 2: backfill (feature, value) pairs a compound tag sets beyond its
# first (e.g. VerbForm/Part for "V.PTCP"), without overwriting pass 1's picks.
for _um_tag, _ud_feats in UM2UD_values.items():
    if _um_tag in _NO_REVERSE:
        continue
    for _feat, _val in _ud_feats.items():
        UD2UM_values.setdefault((_feat, _val), _um_tag)


# A UD value UniMorph spells as several features: the equivalent UD features. The token's own
# annotation stays as it is; apply this to the dict used for matching or tagging.
UD_VALUE_EXPANSIONS: Dict[Tuple[str, str], Dict[str, str]] = {
    ("Tense", "Imp"): {"Tense": "Past", "Aspect": "Imp"},   # UM: PST;IPFV (es, pt, it)
}


# UD values that include more specific ones: a token with the general value fits rows that state
# any of the specific values (UD Aspect=Imp is imperfective in general; UniMorph tells PROG, HAB,
# ITER apart, and Turkish -iyor forms are PROG there but Imp in the treebank)
UD_VALUE_INCLUDES: Dict[Tuple[str, str], List[str]] = {
    ("Aspect", "Imp"): ["Prog", "Hab", "Iter"],
}


def widen_ud_value(feat: str, value: str) -> str:
    """`value` (comma readings allowed) plus the more specific values it includes."""
    base = feat.partition("[")[0]
    readings = value.split(",")
    for reading in list(readings):
        readings += [v for v in UD_VALUE_INCLUDES.get((base, reading), []) if v not in readings]
    return ",".join(readings)


def expand_ud_feats(feats: Dict[str, str]) -> Dict[str, str]:
    """`feats` with UD_VALUE_EXPANSIONS applied (a feature already present is kept)."""
    for (feat, val), parts in UD_VALUE_EXPANSIONS.items():
        if feats.get(feat) == val:
            feats = {**feats, **{k: v for k, v in parts.items() if k == feat or k not in feats}}
    return feats


def fuses_upos(tag: str) -> bool:
    """True if `tag` (or a "/" disjunction component) is a compound UM tag
    that already implies a upos, e.g. "V.PTCP" implies upos=VERB."""
    return any(UM2UD_values.get(sub, {}).get("upos") is not None for sub in tag.split("/"))


def upos_to_um_tag(upos: str) -> Optional[str]:
    return UD2UM_values.get(("upos", upos))


def ud_gap(feat: str, val: str) -> Optional[Dict]:
    """The `ud_gaps` entry of the UD value `feat`=`val` (a comma value is looked up whole, then by its
    first listed part); None if it is not a known gap."""
    entry = ud_gaps.get(f"{feat}={val}")
    if entry is None and "," in val:
        entry = next((ud_gaps[key] for part in val.split(",") if (key := f"{feat}={part}") in ud_gaps), None)
    if entry is None and "[" in feat and all((feat.partition("[")[0], part) in UD2UM_values for part in val.split(",")):
        # Number[obj]=Plur: the value is mapped, converting the layered name is the consumer's job
        entry = {"category": "layered feature, converted by the consumer", "languages": []}
    return entry


def _report_unmapped(feat, val, unmapped, warn_unknown, warn_known_gaps, log_file):
    """Record (and print) one UD value without a UM tag as unknown or as a known gap."""
    gap = ud_gap(feat, val)
    record = {"feature": feat, "value": val, "status": "known_gap" if gap else "unknown",
              "category": gap["category"] if gap else None}
    if gap and gap["languages"]:
        record["languages"] = gap["languages"]
    if unmapped is not None and record not in unmapped:
        unmapped.append(record)
    if gap and warn_known_gaps:
        _notice(f"Note: known gap, no UniMorph tag: {feat}={val}", log_file)
    elif not gap and warn_unknown:
        _notice(f"Warning: Unknown UD value {feat}={val}", log_file)


def feat_val_to_um_tag(feat: str, raw_val: str, warn_unknown: bool = False, warn_known_gaps: bool = False,
                       log_file: Optional[str] = None, unmapped: Optional[list] = None) -> Optional[str]:
    """One UD feature value (comma-valued for syncretic forms, "Masc,Fem") as one UM tag, "/"-joining the
    UM tags of its parts; None if no part has a UD2UM entry.

    A part without a UM tag is reported as in UM2UD_mapper: `warn_unknown` warns for a value neither
    mapped nor in `ud_gaps`, `warn_known_gaps` notes a listed one (both off by default: this runs once
    per token), `log_file` appends the messages to a txt file, `unmapped` (a list) collects
    {"feature", "value", "status", "category"} records."""
    sub_tags = []
    for val in raw_val.split(","):
        if (feat, val) in UD2UM_values:
            sub_tags.append(UD2UM_values[(feat, val)])
        elif warn_unknown or warn_known_gaps or unmapped is not None:
            _report_unmapped(feat, val, unmapped, warn_unknown, warn_known_gaps, log_file)
    if not sub_tags:
        return None
    return "/".join(dict.fromkeys(sub_tags))


def ud_feats_to_um_tags(upos: str, feats: Optional[Dict[str, str]], warn_unknown: bool = False,
                        warn_known_gaps: bool = False, return_unmapped: bool = False,
                        log_file: Optional[str] = None):
    """A UD token's upos and plain feats as UM tags (["V", "PST", "3", "SG"]); comma values become "/"
    disjunctions (feat_val_to_um_tag), values without a UD2UM entry are skipped, None if the upos has
    no UM counterpart (PUNCT, SYM, X, ...).

    `warn_unknown`, `warn_known_gaps` and `log_file` work as in feat_val_to_um_tag. With
    `return_unmapped` the result is {"tags": <list or None>, "unmapped": [...]}, one record
    {"feature", "value", "status": unknown | known_gap, "category"[, "languages"]} per skipped value."""
    unmapped = []
    kwargs = dict(warn_unknown=warn_unknown, warn_known_gaps=warn_known_gaps, log_file=log_file, unmapped=unmapped)
    tags = _feats_to_um_tags(upos, feats, kwargs)
    return {"tags": tags, "unmapped": unmapped} if return_unmapped else tags


def _feats_to_um_tags(upos, feats, kwargs):
    upos_tag = upos_to_um_tag(upos)
    if upos_tag is None:
        _report_unmapped("upos", upos, kwargs["unmapped"], kwargs["warn_unknown"], kwargs["warn_known_gaps"], kwargs["log_file"])
        return None

    feats = expand_ud_feats(feats or {})
    tags = [
        tag for feat, raw_val in (feats or {}).items()
        if (tag := feat_val_to_um_tag(feat, raw_val, **kwargs)) is not None
    ]

    if not any(fuses_upos(tag) for tag in tags):
        tags.insert(0, upos_tag)

    return tags or None


# --- reading raw UniMorph feature strings ---

BASE = "BASE"   # UniMorph's unmarked Degree
UD2UM = {
    **UD2UM_values,
    # positive degree is unmarked in UniMorph (BASE); without this "Pos" resolves to Polarity's POS
    ("Degree", "Pos"): BASE,
}
