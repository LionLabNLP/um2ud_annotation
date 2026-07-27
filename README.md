# um2ud_morpho
Mapping morphological annotation from Unimorph to Universal Dependencies format and tags

# Usage

This repo's main intention is to map from the Unimorph (UM) annotation strings to valid Universal Dependencies (UD) formatted annotation (UPOS and morphological annotation).

Given an annotation string in Unimorph format `V;V.PTCP;PST` (eat/eaten), we can obtain a UD-compatible feature dictionary `{'morpho': {'Tense': 'Past', 'VerbForm': 'Part'}, 'upos': 'VERB'}`:

```
from um2ud_morpho.UM2UD_mapper import map_um_value_to_ud
ud_annotation = map_um_value_to_ud("V;V.PTCP;PST")
print(ud_annotation)
{'morpho': {'Tense': 'Past', 'VerbForm': 'Part'}, 'upos': ('VERB',)}
````

When faced with a foreign value, a warning will be printed. Add the mapping to `UM2UD_values` or `unk_values` as needed.

# Contents

**UM_tagset.py**
* Contains the tagset of the Unimorph tags (and the features which the central documentation outlines), based on the UM docs and actual UM data.

**data/**
* Preparsed UM annotation types (i.e., without lemma/form information) per language (`lang_code.json`), all in one file (`complete_parses.json`), and a collection of all unique annotation string parses across all languages (`unique_parses.json`) 

**LGSPECs.md**
* Compiled documentation on `LGSPECXX` tags from the Unimorph data repositories' readme files

**UM2UD_mapper.py**
* Usage functions
* Mapping of UM to UD annotation
* `missing`: Values that are mentioned in the Unimorph docs but did not occur in the Unimorph data, and for which we also don't have a UD-match
* `fix_typos`, which maps clear typos/simple mistags to their intended forms, and `blacklist`, which has two values with typos (`ARBEB1P`,`ARBEB1S`) where the originally intended form is unclear

# Known Issues

#### Unmapped Features/Values 
Some features/values are not modelled in UD and can therefore not be represented; these are found in `UM2UD_mapper`'s `UM2UD_values` dict, but correspond to an empty feature dictionary.

|Feature|Value|Reason|Affects|
|---|---|---|---|
|Aktionsart|STAT, stative | Feature not modelled by UD|Chukchi (ckt)|
|Case|APPRX, approximate|Value not in UD|Livvi (olo), Veps (vep)|
|Case|OBL, oblique|Value not in UD|Gujarati (OBL+VOC) (guj)|
|Interrogativity|DECL, declarative|Feature not modelled by UD|Korean (kor), Turkish (tur)|
|Mood|DED, deductive|Value not in UD|Sakha/Yakut (sah)|
|Mood|INFR, ??|Value not in UD|Turkish (tur)|
|Voice|APPL, applicative|Value not in UD|Indonesian (ind)|
|upos?|ADJ.CVB/MSDR/PTCP|Verbal tags on ADJ unclear, only upos=ADJ mapped|Korean (kor)|

The same file also has `unk_values`. These did occur in the Unimorph data, but for which neither documentation nor a corresponding UD value could be found, so that it is unclear whether they could be modelled by UD:

|Feature|Value|Affects|
|---|---|---|
|Tense|NPST, Nonpast|Sakha/Yakut (sah)|
|Mood|HYP, hypothetic|Basque (eus)|
|Case|(non)NOM, negated nominative|Pashto (pus)|

#### Language-Specific (LGSPEC) Tags

The following languages use `LGSPECXX` ("language specific") morphological tags. For most of these, no documentation could be found, and all of them are treated as `unk_values`: Afrikaans, Amharic, Armenian, Assamese, Bengali, Czech, Georgian, German, Gothic, Gujarati, Hindi, Hungarian, Latin, Latvian, Lithuanian, Manx, Neapolitan, Pashto, Russian, Spanish, Tagalog, Turkish, Urdu, Xibe, Yakut, Yiddish.
See also `LGSPECs.md`

#### Complex Values

Unimorph specifies that values can be annotated as atomic (`value1`) or as conjunctions (`value1+value2`), disjunctions (`value1/value2`), or negations (`non(value1)`). In contrast, UD can only model disjunctions (UM: `value1/value2` -> UD: `value1,value2`). Conjunctions, where 2+ values want to populate the same feature are returned as tuples of values for the time being.

Issues due to conjunctions/multivalue conflicts commonly arise in:
- Breton (bre): Aspect
- Karelian (krl): Tense
- Korean (kor): Polite
- Spanish (spa): upos
- Indonesian (ind): Voice
- Macedonian (mkd): Aspect
- Lithuanian (lit): upos
- Czech (ces): Gender
- Japanese (jpn): Aspect, Mood, Polite, Style, Voice
- Chukchi (ckt): Aspect, Case
- Greek (ell): Case

It is possible that some instances of multivalue conflicts are/were intended as disjunctions.

# Creation

The mapping is created specifically for the Unimorph -> Universal Dependencies direction. The focus is on mapping the values that occur in the Unimorph data to UD-compatible annotation.

1. Compile UM tagset from UM docs and data
2. Search for direct matches in UD (i.e., same feature and value name, like Tense/FUT -> Tense/Fut, 'future') and close matches with direct correspondence (Tense/PRS -> Tense/Pres, 'present')
3. Search for indirect correspondence via UD docs and UM-UD mapping (2023), e.g., Mood/OBLIG -> Mood/Nec
4. Write mapping, note extra/missing values, and define additional heuristics (incl. for argument marking/possession, and non-atomic values)


# Citations

**UM master repository:** https://github.com/unimorph/unimorph

**UM documentation:** Sylak-Glassman, J. (2016). The Composition and Use of the Universal Morphological Feature Schema (Unimorph Schema). Johns Hopkins University, p. 1–79. https://unimorph.github.io/publications/

**UM-UD mapping** by Dan Zeman (2023): https://github.com/dan-zeman/interset/blob/master/lib/Lingua/Interset/Tagset/MUL/Unimorph.pm

**UD features and values:** https://universaldependencies.org/survey-feats.html