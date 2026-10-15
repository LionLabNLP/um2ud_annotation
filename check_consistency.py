"""Consistency check between the UM tagset (UM_tagset.py) and the mappings (UM2UD_mapper.py).

    python -m resources.um2ud_annotation.check_consistency      # from the repository root

`check()` returns {problem: sorted tags}; the CONFLICTS end with exit status 1, the rest is information.
"""
import re

from .UD2UM_mapper import UD2UM
from .UD_gaps import ud_gaps
from .UM2UD_mapper import LGSPEC_PATTERN, LGSPEC_UD, UM2UD_values, fix_typos, shortened_vals
from .UM_gaps import blacklist, missing, unk_values
from .UM_tagset import UM_feature2values

CONFLICTS = ("mapped_and_gap", "mapped_not_in_tagset", "ud_gap_now_mapped")


def check():
    tagset = {tag for tags in UM_feature2values.values() for tag in tags}
    mappings = {**shortened_vals, **UM2UD_values}
    mapped = {tag for tag, ud in mappings.items() if ud}                  # an empty dict marks a known gap
    gaps = set(unk_values) | set(blacklist) | set(missing)
    known = set(mappings) | gaps | set(fix_typos) | {f"{m.group(1)}{i}" for tag in gaps if (m := re.fullmatch(r"([A-Z]+)(\d)-(\d)", tag))
                                                    for i in range(int(m.group(2)), int(tag[-1]) + 1)}   # "NAKH1-8"
    lgspec_values = {(feat, val) for tags in LGSPEC_UD.values() for ud in tags.values() for feat, val in ud.items()}
    return {
        # a tag that has a UD value and is also listed as a gap
        "mapped_and_gap": sorted(mapped & gaps),
        # a mapped tag the tagset does not document ("+" compounds are combinations of listed tags)
        "mapped_not_in_tagset": sorted(tag for tag in mapped - tagset if "+" not in tag),
        # a UD value listed in UD_gaps.py that UD2UM has a tag for by now
        "ud_gap_now_mapped": sorted(key for key in ud_gaps if tuple(key.split("=", 1)) in UD2UM),
        # an LGSPEC_UD value of a feature UD -> UM knows, but with no UM code of its own (Tense=NearPast)
        "lgspec_value_without_um_code": sorted(
            f"{feat}={val}" for feat, val in lgspec_values
            if (feat, val) not in UD2UM and feat in {f for f, _ in UD2UM}),
        # documented in the tagset, but no mapping, gap entry or typo fix mentions it
        "tagset_tag_without_entry": sorted(tagset - known),
        # gap entries the tagset does not document: data-only tags (LGSPEC placeholders left out)
        "gap_not_in_tagset": sorted(tag for tag in gaps - tagset if not LGSPEC_PATTERN.fullmatch(tag)),
    }


if __name__ == "__main__":
    result = check()
    for name, tags in result.items():
        kind = "CONFLICT" if name in CONFLICTS else "info"
        print(f"[{kind}] {name}: {len(tags)}" + (f"  {', '.join(tags)}" if tags else ""))
    raise SystemExit(any(result[name] for name in CONFLICTS))
