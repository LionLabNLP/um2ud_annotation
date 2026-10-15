# um2ud_annotation
Mapping morphological annotation from Unimorph to Universal Dependencies format and tags

# Usage

This repo's main intention is to map from the Unimorph (UM) annotation strings to valid Universal Dependencies (UD) formatted annotation (UPOS and morphological annotation).

Given an annotation string in Unimorph format `V;V.PTCP;PST` (eat/eaten), we can obtain a UD-compatible feature dictionary `{'morpho': {'Tense': 'Past', 'VerbForm': 'Part'}, 'upos': 'VERB'}`:

```
from um2ud_annotation.UM2UD_mapper import map_um_value_to_ud
ud_annotation = map_um_value_to_ud("V;V.PTCP;PST")
print(ud_annotation)
{'morpho': {'Tense': 'Past', 'VerbForm': 'Part'}, 'upos': 'VERB'}
````

More examples, both directions (the UD -> UM side is described under "UD -> UM direction"):

```
from um2ud_annotation.UM2UD_mapper import map_um_value_to_ud
from um2ud_annotation.UD2UM_mapper import ud_feats_to_um_tags

# a) UM string -> UD. Argument marking (ARG*/PSS*) becomes bracketed features:
map_um_value_to_ud("V;ARGNO1S;ARGAC3P;PST")
{'morpho': {'Number[acc]': 'Plur', 'Number[nom]': 'Sing', 'Person[acc]': '3', 'Person[nom]': '1', 'Tense': 'Past'}, 'upos': 'VERB'}

# a) with tags that have no UD value; return_unmapped=True lists them, with the warnings off:
map_um_value_to_ud("N;XYZ;INTER;NHUM;NOM;SG;non{ACC}", warn_unknown=False, warn_known_gaps=False, return_unmapped=True)
{'morpho': {'Case': 'Nom', 'Number': 'Sing'}, 'upos': 'NOUN',
 'unmapped': [{'tag': 'XYZ', 'status': 'unknown', 'category': None},                  # never seen
              {'tag': 'INTER', 'status': 'known_gap', 'category': 'Case'},             # listed gap
              {'tag': 'NHUM', 'status': 'known_gap', 'category': 'Animacy'},
              {'tag': 'NON{ACC}', 'status': 'negation', 'category': 'Case', 'excluded': ['ACC']}]}   # negation

# b) UD upos + feature dict -> UM tags (a comma value becomes a "/" disjunction):
ud_feats_to_um_tags("NOUN", {"Gender": "Fem", "Number": "Sing"})
['N', 'FEM', 'SG']

# b) with a value that has no UM tag (Foo=Bar is in no list, so it is "unknown"; a listed one is "known_gap"):
ud_feats_to_um_tags("VERB", {"Tense": "Past", "Gender": "Fem,Masc", "Foo": "Bar"}, return_unmapped=True)
{'tags': ['V', 'PST', 'FEM/MASC'], 'unmapped': [{'feature': 'Foo', 'value': 'Bar', 'status': 'unknown', 'category': None}]}
```

When faced with a foreign value, a warning will be printed. Add the mapping to `UM2UD_values` or `unk_values` as needed. Several values for one feature (conjunction, disjunction, or two tags of one feature such as `HYP;POT`) are collected per feature and returned as one sorted comma value (`Mood: 'Cnd,Pot'`); there are no tuples.

Keyword arguments of `map_um_value_to_ud(s, warn_unknown=True, warn_known_gaps=True, return_unmapped=False, keep_conjunctions=False, log_file=None, lang=None)`:
* `warn_unknown`: print `Warning: Unknown Unimorph value X` for a value the package has never seen.
* `warn_known_gaps`: print `Note: known gap, no UD mapping: X` for a known gap (`blacklist`, `unk_values`, `missing`, negations); LGSPEC placeholders are stripped before parsing and never noted. `False` skips known gaps silently. `is_known_gap(value)` tests membership.
* `log_file="x.txt"`: append the warnings and notes to that file instead of printing them.
* `return_unmapped=True`: the result gets an extra `"unmapped"` list with one record per tag that has no UD value: `{"tag", "status": "unknown" | "known_gap" | "negation", "category"}` (a negation also has `"excluded"`, the negated UM values). Without the flag the result is exactly `{"morpho", "upos"}`.
* `lang="sah"`: UniMorph language code; applies that language's `LGSPEC_UD` entries (see LGSPEC tags below). Without it every LGSPEC tag is stripped.
* `keep_conjunctions=True`: keep "both" apart from "either" (see Complex Values). The default gives one sorted `A,B`.

The README tables below are the human-readable list; the code lists are `unk_values` / `blacklist` / `missing` in `UM_gaps.py` and the `UM2UD_values` entries with an empty dict.

# Contents

**UM_tagset.py**
* Contains the tagset of the Unimorph tags (documentation vocabulary; includes the data-only and synthetic tags the mappers use, e.g. NPST, HYP, PSSD, BASE, SUPI; compounds like `IN+ABL` are combinations of listed tags) (and the features which the central documentation outlines), based on the UM docs and actual UM data.

**data/**
* Preparsed UM annotation types (i.e., without lemma/form information) per language (`lang_code.json`), all in one file (`complete_parses.json`), and a collection of all unique annotation string parses across all languages (`unique_parses.json`) 

**UM_gaps.py**, **UD_gaps.py**
* The two gap lists, one per direction, importable on their own. `UM_gaps.py`: the UniMorph tags with no UD mapping (`blacklist`, `missing`, `unk_values`, each tag keyed to its UM category; `UM2UD_mapper` re-exports them). `UD_gaps.py`: `ud_gaps`, the UD `Feature=Value` pairs of the UD 2.18 treebanks that have no UniMorph tag (837), each with its category and the languages it occurs in. The categories (assigned by hand, the same for every value of a feature) are listed in its docstring: `morphosyntactic: no tag yet`, `lexical-semantic property (no UniMorph slot)`, `non-inflectional / lexical label`, and for upos `no UniMorph part of speech` (PUNCT, SYM, X) and a CCONJ/SCONJ entry (UniMorph only has CONJ). Layered names (`Number[obj]`) of mapped values count as known, converted by the consumer. The five values the treebanks have that the original list lacked (`Case=Add`, `Case=Cau`, `HebBinyan=NITPAEL`, `PartType=Sub`, `Tense=FutPast`) take the category of their feature. A value found in the treebanks but listed nowhere is reported as unknown.

**check_consistency.py**
* `python -m resources.um2ud_annotation.check_consistency` (from the repository root) checks the package's lists against each other (not the mapping behaviour, and not the UniMorph or UD data). Run it after editing a mapping or gap list. Three checks are conflicts and end with exit status 1:
  * `mapped_and_gap`: a tag with a UD value that is also in `blacklist`, `missing` or `unk_values`.
  * `mapped_not_in_tagset`: a mapped tag `UM_tagset.py` does not list (`+` compounds excluded).
  * `ud_gap_now_mapped`: a `ud_gaps` value that UD2UM has a tag for by now (a stale gap entry).

  Three are information only:
  * `lgspec_value_without_um_code`: `LGSPEC_UD` values with no UM code of their own (`Tense=NearPast`, `Tense=PastPerf`; expected).
  * `tagset_tag_without_entry`: tagset tags no mapping, gap entry or typo fix mentions (currently 0).
  * `gap_not_in_tagset`: gap entries the tagset does not document, i.e. tags found only in the data (`AC1*`, `NO1*`, `COMP`, ...; 65 currently, expected).

**LGSPECs.md**
* Compiled documentation on `LGSPECXX` tags from the Unimorph data repositories' readme files, and the treebank evidence for the `LGSPEC_UD` mappings and the candidates not mapped

**UM2UD_mapper.py**
* `map_um_value_to_ud` and its helpers (complex values, negations, argument/possessor tags)
* `UM2UD_values`, `shortened_vals`: the UM -> UD mapping
* `LGSPEC_UD`: LGSPEC tags with a UD meaning in one language (used with `lang=`)
* `fix_typos`: maps clear typos/simple mistags to their intended forms
* `blacklist` (two typo values, `ARBEB1P`/`ARBEB1S`, whose intended form is unclear), `unk_values` (tags kept without a UD mapping, keyed to their UM category) and `missing` (in the Unimorph docs but not in the data, no UD match) are defined in `UM_gaps.py`

# UD -> UM direction

`UD2UM_mapper.py` reverses the table (built on `UM2UD_values`, which stays the single source of truth):
* `ud_feats_to_um_tags(upos, feats)`, `feat_val_to_um_tag`, `upos_to_um_tag`, `UD2UM_values` / `UD2UM`: UD -> UM tag(s).
* `feat_val_to_um_tag(feat, val, warn_unknown=False, warn_known_gaps=False, log_file=None, unmapped=None)` and `ud_feats_to_um_tags(upos, feats, warn_unknown=False, warn_known_gaps=False, return_unmapped=False, log_file=None)` report UD values without a UM tag like the UM -> UD function does: `warn_unknown` for a value neither mapped nor listed in `ud_gaps` (`Warning: Unknown UD value X=Y`), `warn_known_gaps` for a listed one (`Note: known gap, no UniMorph tag: X=Y`), `log_file` for a txt log, `return_unmapped` for `{"tags", "unmapped"}` with one `{"feature", "value", "status", "category"[, "languages"]}` record per skipped value (`feat_val_to_um_tag` collects them in the list passed as `unmapped`). The warnings are off by default (the functions run once per treebank token); the result without `return_unmapped` is unchanged.
* `ud_gaps` (`UD_gaps.py`), `ud_gap(feat, val)`: the UD `Feature=Value` pairs of the UD 2.18 treebanks that have no UniMorph tag, each with its category and the languages it occurs in.
* `expand_ud_feats`, `widen_ud_value` with `UD_VALUE_EXPANSIONS` / `UD_VALUE_INCLUDES`: UD values that UM spells as several features, or that include more specific values (see caveats).

`UM2UD_mapper.py` also exports `UM2UD`, `SHORTENED_UM_VALS`, `COMPOUND_TAGS` (known `+` tags), `UPOS_VALUES`, `LGSPEC_UD_FEATURES`, `parse_negation`, `negation_feature`, `negation_code`, `is_known_gap`, `pos_is_degree` and `cached_map_um_value_to_ud`. The package does not depend on any project code.

# Known Issues

#### Unmapped Features/Values
These are keys of `UM2UD_values` with an empty feature dictionary, or entries of `unk_values`; the tag is kept as UM-only (`UM:<tag>`) by consumers.

|Feature|Value|Reason|Affects|
|---|---|---|---|
|Aktionsart|STAT, stative | Feature not modelled by UD|Chukchi (ckt), Evenki (evn), Aikana (ail), Xibe (xty)|
|Case|APPRX, approximate|Value not in UD|Livvi (olo), Veps (vep), Karelian (krl), Ludian (lud), Aikana (ail)|
|Interrogativity|DECL, declarative|Feature not modelled by UD. Not Mood=Ind: in Turkish every IND/INFR row exists with and without DECL, and DECL also occurs on IMP and mood-less rows|Korean (kor), Magahi (mag), Turkish (tur)|
|Mood|DED, deductive|Value not in UD|Sakha/Yakut (sah)|
|Mood|SIM, simulative|Value not in UD|Aikana (ail)|
|any|negations: `(non)NOM`, `not{NOM}`, `non{PST}`, `non{NOM/ACC}`|"any value but X". Recognised for any feature once the negated value resolves to one (`parse_negation`, `negation_feature`); skipped by `map_um_value_to_ud`; the main project's `ufeats_to_dict` stores the canonical code `nonNOM` / `nonNOM\|ACC` under the feature, so a consumer can state the feature's other values|Pashto (pus), Old French (fro), hsi, gup, ail|
|upos?|ADJ.CVB/MSDR/PTCP|Verbal tags on ADJ unclear, only upos=ADJ mapped|Korean (kor)|

`unk_values` also holds values that occur in UM data without UD or documented equivalent: INTER (Aymara, Quechua), RCT, RMT, HOD, IMMED (tense), SEMEL, TEL, ACTY (Aktionsart), DRCT, INFER, RPRT (evidentiality), LKLY (mood), REF1, VIS (deixis), SS, DS, SIMMA (switch reference), plus the entries above (LGSPEC tags are recognised by `LGSPEC_PATTERN`, not listed). `missing` lists tags from the UM docs not seen in the data (unverified).

#### Mappings that are judgement calls
Each was checked against the UD treebank of the language (share of tokens carrying the UD value for the UM-tagged forms), 2026-10:

|UM|UD|Basis|
|---|---|---|
|NPST (Yakut)|Tense=Pres|98% of tokens|
|HYP (Basque)|Mood=Cnd,Pot|84% Cnd, 16% Pot, so both readings|
|INFR (Turkish)|Evident=Nfh|86% of tokens|
|OBL (Gujarati, only `OBL+VOC`)|Case=Acc|treebank marks oblique nouns Acc|
|APPL (Indonesian)|Voice=Appl|direct; UD Indonesian has no Voice=Appl, other treebanks do|
|PSSD (Hebrew)|Definite=Cons|88% vs 24% of other nouns|
|SPRL+AB / AB+SPRL (Greek)|Degree=Sup|one reading, not two; 16 of 17 tokens|
|IN+ABL, IN+ALL, AT+ESS, AT+ABL, AT+ALL, ON+ESS, ON+ABL, ON+ALL (fi, hu, et, se)|Ela, Ill, Ade, Abl, All, Sup, Del, Sbl|each is ONE case, not an ambiguity; 90-98% of tokens|
|POS on ADJ/ADV without verbal features|Degree=Pos (not Polarity)|`pos_is_degree`; UD2UM goes back to `BASE`|
|BASE, SUPI|Degree=Pos, VerbForm=Sup|synthetic codes (UM has no supine tag; SUP is Degree)|

#### Full parse of all UniMorph languages (2026-10)
`data/` was regenerated from every `resources/unimorph/<lang>/<lang>` file (all POS): 178 languages (was 71), 32,920 unique annotation strings (was 10,318). All 71 earlier languages parse without any unknown value; every unknown value below comes from languages added in this run.

Values the parser warned about in this run. All are now registered in `unk_values` (category `UNK`, the bucket for values with no known feature: no README explains them), except the brace artifacts of kca (`3}`, `P}`):

|Language|Values|Reading / what is needed|
|---|---|---|
|ame, cni, cre, kod, aym, ail|`NO1`, `NO1P`, `NO2`, `NO3F`, `NO3SA`, `NO1PE`, `NO2S` ... `AC1`, `AC1PE`, `AC3S` ... `DA1S` ... (kod, ame, cni, cre, aym; ail `AC3P`)|argument-marking tags written without the `ARG` prefix (`NO1S` = `ARGNO1S`, `AC` = accusative, `DA` = dative argument); mappable by adding the prefix, not done yet (aym alone: ~26-54k rows per AC tag)|
|aym, ail|`CF`, `FORM2` (aym 40k / 6k rows), `DEO` (ail)|meaning unclear (`CF` possibly counterfactual, `FORM2` a second form variant; `DEO` unknown); aym `CF` 40k rows, `FORM2` 6k rows|
|que|`AGT`, `BEADJ`, `GEADJ`, `CAUSV`, `DISTR`, `EXCLV`|derivational/clitic suffixes on nominals and verbs (names suggest agentive, "for"/"of" adjectival, causal, distributive, exclusive; not checked against Quechua docs); no UD value|
|mwf|`NFUT`, `PC`|`NFUT` near future (Tense=Fut candidate), `PC` paucal (Number=Pauc candidate)|
|mag|`INFN`, `LSGSPEC1/2`|typos: `INFN` probably `INFM`, `LSGSPEC` = `LGSPEC`|
|bra|`LGSEPC1/2`, `LGSPEPC1-3`, `LGSPEC`, `FROM`, `FUTS`, `PFA`, `SL`|typos of LGSPEC (`LGSEPC`, `LGSPEPC`), plus one-off stray tags (`FUTS` comes from a `,` that should be `;`)|
|kca|`COMP`|never the upos; follows it (`ADJ;COMP`, `ADV;COMP`, `NUM;COMP`, `N;DAT;COMP;SG`) on `-šək` forms: probably the comparative (`CMPR`, `Degree=Cmp`). Formerly mapped as the complementizer upos (`CONJ`, `ConjType=Sub`) after Zeman's Interset mapping, which no language uses; now `unk_values`, unconfirmed (no README)|
|slp|`NALN`|probably non-alienable possession (counterpart of `ALN`)|
|ket|`ADB`, `_`|`ADB` probably adverb (upos); `_` is an empty placeholder|
|gup|`REDUP`|reduplication; no UD value|
|kca|`PSS{2/3}D`, `ARGAC{D/P}`, `TAXIS`|braces around a disjunction inside a tag (`PSS2D/PSS3D`): not expanded (`D` is dual here but Construct state in the shortened-value table); `TAXIS` is a switch-reference style tag|
|aym, lug, pei, evn, ail, aka, gup, mag|`IMMED`, `RMT`, `RCT`, `VERS`, `MPOL`|already in `unk_values`; no longer warned about (also inside compounds like `PRS/PST+IMMED`)|
|ckb|(fixed) `ADJ(DA)(1P)`, `DEF(3S)`, `CMPR(EWE)` ...|`LGSPEC_PATTERN` removed the preceding `;` too, so `ADJ;LGSPEC4(DA);LGSPEC7(1P)` became `ADJ(DA)(1P)` and the upos was lost. The pattern now matches the tag itself (digits optional, parenthesised suffix, the LGSEPC/LGSPEPC/LSGSPEC typos) only. `ADP + ADJ` (fused forms) now parses as the conjunction `ADP`, `ADJ`: `upos: 'ADJ,ADP'`|

Differences to the previous `data/` in the 71 languages that were already parsed (parse of the same strings with the current mapper vs the old files):
* 1,529 strings changed; almost all from the new mappings: `Evident=Nfh` for `INFR` (tur, 312), `Mood=Cnd,Pot` for `HYP` (eus, 478), the 8 location-case compounds (fi/hu/et/se/krl/olo/vep, ~300), `Degree=Pos` instead of `Polarity=Pos` on ADJ/ADV (ind, 45), `Definite=Cons` for `PSSD` (heb), `Tense=Pres` for `NPST` (sah), `Voice=Appl` (ind), `Case=Acc` for `OBL` (guj). The rest are only reordered values.
* HYP combined with another mood (Basque): readings are now merged per feature before output, `HYP;POT` -> `Mood=Cnd,Pot`, `HYP;IND` -> `Mood=Cnd,Ind,Pot`. The second is only a union: of the UD tokens with a `HYP;IND` form in the Basque treebank (4), none has Mood=Ind or Cnd (no Mood at all), while `HYP;POT` forms are Cnd (25) or Pot (3).
* 58 strings were added and 2,189 removed in the 16 languages whose UniMorph file changed since the old parse (hun, ces, deu, lat, fin, por, cat, ita, swe ...): data version difference, not a mapper change.

#### UD -> UM caveats
* UD values that several UM tags collapse onto are returned `/`-joined (`Case=Acc` -> `ACC/OBL`, `Case=Ade` -> `AT+ESS/AT`, `Degree=Sup` -> `SPRL+AB/AB+SPRL/SPRL/SUP`, `Evident=Nfh` -> `INFR/NFH`). Only upos collisions keep a single pick, since a joined upos would be baked into every token.
* NPST and HYP are never offered as the UM spelling (`_NO_REVERSE`); NPST would turn every Tense=Pres into `NPST/PRS`.
* `Tense=Imp` (es, pt, it) is expanded by `expand_ud_feats` to `Tense=Past` + `Aspect=Imp` (UM: `PST;IPFV`). The token's own annotation is not changed; apply the expansion to the dict used for matching.
* `Aspect=Imp` includes Prog, Hab, Iter (`widen_ud_value`): UM tells these apart, UD does not (Turkish -iyor forms are PROG in UM, Imp in the treebank).
* The UD -> UM functions handle plain UD features only; bracketed ones (`Number[obj]`) are the consumer's job (the main project reads raw UM strings into such keys itself).
* Korean's deverbal adjectives (`ADJ.MSDR/ADJ.PTCP/ADJ.CVB`) stay a known, unfixed gap: upos ADJ resolves to plain `ADJ`.

#### Language-Specific (LGSPEC) Tags

`LGSPECXX` ("language specific") tags mean something different in every language that uses them, so they are stripped by default. A few have a documented meaning and treebank support and are mapped when `map_um_value_to_ud(..., lang=)` is given the language code (`LGSPEC_UD` in UM2UD_mapper.py): afr `LGSPEC3` (`Degree=Dim`), kat `LGSPEC1` (`Case=Ess`), hye `LGSPEC01` (`Aspect=Perf`), sah `PST;LGSPEC1/2` (`Tense=NearPast/PastPerf`), afr `LGSPEC1/2` (`AdjType=Pred/Attr`), got `LGSPEC01/02` (`Strength=Strong/Weak`). `LGSPEC_UD_FEATURES` lists the UD features these produce. The evidence, and the candidates not mapped (hin/urd, hye, asm), are in `LGSPECs.md`. Languages that use them (most have no README description, see `LGSPECs.md`): Afrikaans, Amharic, Armenian, Assamese, Bengali, Czech, Georgian, German, Gothic, Gujarati, Hindi, Hungarian, Latin, Latvian, Lithuanian, Manx, Neapolitan, Pashto, Russian, Spanish, Tagalog, Turkish, Urdu, Xibe, Yakut, Yiddish.
See also `LGSPECs.md`

#### Not done (no good evidence, or a consumer decision)
* **Language-specific `NFIN -> Inf`** (hin, urd, deu): `NFIN` is the infinitive there (`VerbForm=Inf` on 97-100% of the matched UD tokens), but `NFIN` maps to `NonFin` everywhere. The evidence is the treebanks only, no README says so; see `LGSPECs.md`.
* **Further LGSPEC tags** (hin/urd `Case`, hye `LGSPEC02/03/04`, asm, lav, kmr, tur): treebank-only, conflicting or too few tokens; not mapped (`LGSPECs.md`).
* **Using `LGSPEC_UD` in a consumer:** `map_um_value_to_ud(..., lang=)` applies it. A consumer that reads UM codes first has to inject the UD values itself (`NearPast`, `Strength=Strong`, ... have no UM code); the main project does this in `multiblimp.um2ud.convert_language`, from the `Language_Specific` tag `ufeats_to_dict` keeps.
* **Languages whose tables were not built or counted** (e.g. Slovak, 28M rows) are outside the checks above.

#### Complex Values

Unimorph specifies that values can be annotated as atomic (`value1`) or as conjunctions (`value1+value2`), disjunctions (`value1/value2`), or negations (`non(value1)`). In contrast, UD can only model disjunctions (UM: `value1/value2` -> UD: `value1,value2`). By default conjunctions, where 2+ values populate the same feature, are returned in the same comma format as disjunctions (`Plur,Sing`): the distinction is lost. With `keep_conjunctions=True` UniMorph's `+` is kept: `SG+PL` is `Plur+Sing` (both), `MASC/FEM` is `Fem,Masc` (either); `,` separates alternatives, `+` joins values that hold together. Separate `;` tags of one feature (`HYP;POT`) are always alternatives (`Cnd,Pot`).

`/` and `,` bind tighter than `+`: `ON/AT+ABL` (vep) is `ON+ABL` or `AT+ABL`, each looked up as a known compound tag (`Case=Abl,Del`); `PRS/PST+IMMED` (aym) is `Tense=Past,Pres` plus the known gap `IMMED`. These two strings are the only mixed ones in the UniMorph data (earlier versions skipped such pieces).

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
