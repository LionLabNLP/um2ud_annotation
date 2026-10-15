# Information on LGSPEC tags
"These features have diﬀerent interpretations
in each language, and no mapping should be assumed between the lgspec features and any other features across languages.", UM docs p.30

#### Afrikaans, afr
- LGSPEC1: Predicative inflection (base form) for adjective
- LGSPEC2: Attributive inflection for adjective
- LGSPEC3: Diminutive form for nouns and proper nouns

UD: LGSPEC3 -> `Degree=Dim`, LGSPEC1/2 -> `AdjType=Pred/Attr` (mapped, see below).

#### Amharic, amh
- LGSPEC1 & 2: orthographic variations

#### Old English, ang
- LGSPEC1: Non-attributive possessive singular for noun inflections
- LGSPEC2: Non-attributive possessive plural for noun inflections
- LGSPEC3: Second person object for verb inflections

README text is identical to Hungarian's (copied); the data only uses LGSPEC01 and LGSPEC02, so the descriptions are doubtful for Old English.

#### Armenian, hye
- LGSPEC01: resultative
- LGSPEC02: future converb 1
- LGSPEC03: future converb 2
- LGSPEC04: connegative

UD: LGSPEC01 -> `Aspect=Perf` (mapped, see below). LGSPEC02-04 not mapped (see below).

#### Assamese, asm

- LGSPEC03: Conjugative
- LGSPEC04: Goal
- LGSPEC05: Agentive
- LGSPEC06: Contingent
- LGSPEC07: Reason
- LGSPEC08: numeral for nouns
- LGSPEC09: non-numeral for nouns

#### Bengali, ben
no information

#### Central Kurdish, ckb
Tags carry a parenthesised suffix in the data (`LGSPEC4(DA)`, `LGSPEC7(3S)`, `LGSPEC8(1P)`, `LGSPEC9(2S)`...: argument person/number or the particle).
- LGSPEC1: Izafe (affix)
- LGSPEC2: postverb adpositions `[e]`, `[ee]` (affix)
- LGSPEC3: postverb adverbial /ewe/ (affix)
- LGSPEC4: discontinuous adpositions `[da]`, `[ra]`, `[ewe2]` (affix)
- LGSPEC5: adverbial clitic
- LGSPEC6: demonstrative clitic
- LGSPEC7: copula clitic
- LGSPEC8: pronominal markers (argument/possessive) on transitive past verbs (clitic)
- LGSPEC9: argument markers on nouns/adjectives (clitic)

#### Czech, ces
"Known issues: forms of reflexive verbs lack reflexive markers as they could not be reconstructed from the original data. It is possible to restore them in future based on some other resources such as valence dictionaries or treebanks."

no further information

#### Georgian, kat
- LGSPEC1: Adverbial case
- LGSPEC2: Archaic Plural

UD: LGSPEC1 -> `Case=Ess` (mapped, see below).

#### German, deu
- LGSPEC01 & 2
no information

#### Gothic, got
- LGSPEC01: Strong (indefinite) inflection for adjective
- LGSPEC02: Weak (definite) inflection for adjective

UD: LGSPEC01/02 -> `Strength=Strong/Weak` (mapped, see below).

#### Gujarati, guj
- LGSPEC1: Conjunctive
- LGSPEC2: Consecutive
- LGSPEC3: Contrafactual
- LGSPEC4: Contrafactual

#### Hindi, hin
no information

#### Serbo-Croatian, hbs
README: "No language specifics are annotated at the current development." The data nevertheless uses LGSPEC1 (26,064 rows) and LGSPEC2 (6,417 rows).

#### Hungarian, hun
- LGSPEC1: Non-attributive possessive singular for noun inflections
- LGSPEC2: Non-attributive possessive plural for noun inflections
- LGSPEC3: Second person object for verb inflections

#### Khalkha Mongolian, khk
- LGSPEC01: VERB + `until`
- LGSPEC02: VERB + `as soon as`
- LGSPEC03: VERB + `if`
- LGSPEC04: VERB + `while`
- LGSPEC05: VERB + `not if`

#### Latin, lat
no information

#### Latvian, lav
no information

#### Lithuanian, lit
no information

#### Manx, glv
no information

#### Neapolitan, nap
no information

#### Old Norse, non
- LGSPEC1: Strong declension
- LGSPEC2: Weak declension

#### Pashto, pus
no information

#### Russian, rus
no information

#### Spanish, spa
- LGSPEC1: imperfect -ra for verbs
- LGSPEC2: imperfect -se for verbs

#### Swedish, swe
README: "No language specifics are annotated at the current development." (no LGSPEC tags in the data)

#### Tagalog, tgl
no information

#### Turkish, tur
no information

#### Tuvan, tyv
- ``NPST``: nonpast tense (present/future tense, aorist)
- ``PST;LGSPEC1``: definite past tense (assertive past, recent past)
- ``PST;LGSPEC2``: indefinite past tense (non-assertive past)
- ``PRF;LGSPEC3``: resultative aspect

#### Urdu, urd
no information

#### Walmajarri, wmt
Lemma-inherent features of the dictionary entries, mapped to LGSPEC (the README says it is not entirely clear how to interpret them):
- LGSPEC01: dv
- LGSPEC02: iv (intransitive?)
- LGSPEC03: tv (transitive?)
- LGSPEC04: mv
- LGSPEC05: 0
- LGSPEC06: n
- LGSPEC07: ng
- LGSPEC08: ny
- LGSPEC09: rr
- LGSPEC10: iv and tv
- LGSPEC11: tv and mv

#### Xibe,sjo
no information

#### Yakut, sah
- ``NPST``: nonpast tense (present/future tense, aorist)
- ``PST;LGSPEC1``: definite past tense (assertive past, recent past)
- ``PST;LGSPEC2``: indefinite past tense (non-assertive past)

UD: LGSPEC1 -> `Tense=NearPast`, LGSPEC2 -> `Tense=PastPerf` (mapped, see below).

#### Yiddish, yid
no information

#### Languages using LGSPEC tags with no README description
Checked against all `resources/unimorph/<lang>/README.md` (2026-10); tags used in the data in parentheses.
ady (1), aka (1), ara (1), ast (1-14), bra (1-5, typos LGSEPC/LGSPEPC, bare LGSPEC), cni (1-2), cor (1-2), frm (1-3), fro (1-12), frr (1-2), fur (1-2), gal (1-2), gml (01-02), gup (01-08), hai (1-9), kan (1-2), kbd (1), kmr (1-2), liv (1-6), lld (1-4), mag (1-2, typo LSGSPEC), nds (01-02), oci (1-2), osx (1-2), pei (1), sga (1-3), slp (01-03), sme (bare LGSPEC), swc (1-10), vec (1-4), xcl (bare LGSPEC, 1-8), xno (1-2), xty (1-2), zul (1-3).
Also undescribed although listed above: ben, deu (only LGSPEC01 in the data), hin (1-4), lat, lav (1-8), lit (1-3), glv, nap, pus, rus, sjo, tgl, tur, urd (1-4), yid.
Described in the README but the data uses more tags: amh (LGSPEC3 once), asm (LGSPEC01-02 undocumented), hun/ang (see above).

# LGSPEC to UD (`LGSPEC_UD`, `map_um_value_to_ud(..., lang=)`)

Only the entries in the "Mapped" table are mapped (UM2UD_mapper.py `LGSPEC_UD`). The mapping applies only when the language code is passed to `map_um_value_to_ud`; the UD value replaces the other tags' value for that feature. Everything else stays an unmapped, stripped LGSPEC tag.

**Method.** The README is the source of the meaning. As a check, the forms that carry a tag (and only that LGSPEC tag, so forms shared with another tag of the language are left out) were matched by lowercase form and upos to the tokens of the language's UD table (`resources/ud_tables/<lang>.parquet`, frequency-weighted), and the UD features on those tokens were compared. "Tokens" below are the matched UD tokens. A form match can be a homograph, and the UD tables only hold features that have a UM tag; for the others the raw treebanks (UD 2.18) were read.

## Mapped

| Language | Tag | README | UD value | Evidence (UD tables) |
|---|---|---|---|---|
| afr | `LGSPEC3` | Diminutive form for nouns and proper nouns | `Degree=Dim` | `Dim` on 75% of 16 tokens (koekies, knoppie, kaartjies, venstertjie). Small sample; README unambiguous. |
| kat | `LGSPEC1` | Adverbial case | `Case=Ess` | `Ess` on 100% of 141 tokens. The Georgian UD table has Nom, Gen, Dat, Ins, Erg, Ess and Voc: no `Adv`, so the adverbial is annotated `Ess`. |
| hye | `LGSPEC01` | resultative (`V.PTCP;LGSPEC01`) | `Aspect=Perf` | `Perf` on 93% of 246 tokens, `VerbForm=Part` on 94% (`Part` already comes from `V.PTCP`). |
| sah | `PST;LGSPEC1` | definite past tense (assertive past, recent past) | `Tense=NearPast` (replaces `Past`) | `NearPast` on 100% of 25 tokens. Small sample. |
| sah | `PST;LGSPEC2` | indefinite past tense (non-assertive past) | `Tense=PastPerf` (replaces `Past`) | `PastPerf` on 89% of 9 tokens. Smallest sample; the README wording ("non-assertive") does not itself say `PastPerf`. |
| afr | `LGSPEC1` | Predicative inflection (base form) for adjective | `AdjType=Pred` | raw UD (see below): `Pred` on 96% of 392 ADJ tokens |
| afr | `LGSPEC2` | Attributive inflection for adjective | `AdjType=Attr` | raw UD: `Attr` on 99.6% of 2,070 ADJ tokens |
| got | `LGSPEC01` | Strong (indefinite) inflection for adjective | `Strength=Strong` | raw UD: `Strong` on 100% of 813 ADJ tokens |
| got | `LGSPEC02` | Weak (definite) inflection for adjective | `Strength=Weak` | raw UD: `Weak` on 92% of 203 ADJ tokens |

`Strength` and `AdjType` have no UM tag, so they are not in `UM2UD_values`; `LGSPEC_UD_FEATURES` lists the UD features only these mappings produce (`AdjType`, `Strength`, plus features already stored), and the main project's `STORED_FEATURES` includes it. The UD tables hold them only after they are rebuilt from the treebanks.

tyv has the same README text for `PST;LGSPEC1/2` (and `PRF;LGSPEC3`: resultative aspect) but no UD table to check, so tyv is not mapped.

## Treebank evidence only (no README description; not mapped)

| Language | Tag | UM forms | Treebank |
|---|---|---|---|
| hin | `V;NFIN;LGSPEC1` | the `-na` infinitive (direct form: `अध्ययन करना`) | `VerbForm=Inf` on 98% and `Case=Nom` on 77% of 562 tokens |
| hin | `V;NFIN;LGSPEC2` | the `-ne` infinitive (oblique form: `अध्ययन करने`) | `VerbForm=Inf` on 100% and `Case=Acc` on 90% of 1,524 tokens |
| urd | `V;NFIN;LGSPEC1` | the `-na` infinitive | `VerbForm=Inf` on 97% of 64 tokens; `Case=Acc` on only 28%, no `Nom` |
| urd | `V;NFIN;LGSPEC2` | the `-ne` infinitive | `VerbForm=Inf` on 100% and `Case=Acc` on 86% of 71 tokens |

* The hin/urd README (hin: source and licence only; urd: none) does not describe the tags. Reading them as direct vs oblique infinitive is an interpretation of the forms; `Case=Acc` for the oblique infinitive is the UD-Hindi annotation convention.
* `VerbForm=Inf` is on both tags: it comes from `NFIN` in these languages (as in German, where `NFIN` is the infinitive), not from LGSPEC. A language-specific `NFIN -> Inf` would be a separate mapping.
* Urdu's `LGSPEC1` does not mirror Hindi's.

## Checked in the raw UD treebanks (UD features without a UM tag)

Forms that carry only that LGSPEC tag, matched by lowercase form and upos to the raw UD 2.18 tokens (CoNLL-U files); these features were not in the UD tables. The got and afr rows are the evidence for the mappings above; hye `LGSPEC04` is not mapped.

| Language | Tag | README | UD feature | Tokens |
|---|---|---|---|---|
| got | `LGSPEC01` | Strong (indefinite) inflection for adjective | `Strength=Strong` | 813 ADJ tokens: Strong 813 (100%) |
| got | `LGSPEC02` | Weak (definite) inflection for adjective | `Strength=Weak` | 203 ADJ tokens: Weak 187 (92%), Strong 2, none 14 |
| afr | `LGSPEC1` | Predicative inflection (base form) for adjective | `AdjType=Pred` | 392 ADJ tokens: Pred 375 (96%), Attr 17 |
| afr | `LGSPEC2` | Attributive inflection for adjective | `AdjType=Attr` | 2,070 ADJ tokens: Attr 2,062 (99.6%), Pred 8 |
| hye | `LGSPEC04` | connegative | `Connegative=Yes` | no support, see below |

hye `LGSPEC04` (`V.CVB;LGSPEC04`, the `-i` form of the verb): the Armenian treebanks (ArmTDP, BSUT) have 69 tokens with `Connegative=Yes` (66 VERB, 3 AUX), 16 of them forms found in the UM data, 13 of those on forms with `LGSPEC04`. In the other direction, of 69 VERB/AUX tokens whose form carries `LGSPEC04` only 13 are `Connegative=Yes` (`Fin`, `Mood=Cnd`); 52 are `Fin` with `Mood=Sub`, and 4 `Imp`. The `-i` forms coincide with the subjunctive forms, so the tag cannot be told apart by form.

## Not mapped: conflicting, thin, or no counterpart

* **hye `LGSPEC02`** (`V.CVB;FUT;LGSPEC02`, future converb 1, `-elu`): UD has `VerbForm=Inf` (88%) and `Case=Dat` (90%) on 301 tokens, where `V.CVB;FUT` gives `Conv`/`Fut`. Not replaced, because the README and the treebank disagree on what the form is.
* **hye `LGSPEC03`** (future converb 2, `-elik`): 3 matched tokens (`Part`, `Aspect=Prosp`); too few.
* **asm `LGSPEC03-07`** (Conjugative, Goal, Agentive, Contingent, Reason; verbs): the Assamese UD table has no or one matching token per tag (`LGSPEC04`: 4 `Inf` tokens, `LGSPEC07`: 1 `Case=Loc` noun). Too little data to check or map.
* **lav `LGSPEC1/4/5/6`**: `LGSPEC6` forms are tagged participles in UM but are finite 1PL present indicatives in UD (98% of 280 tokens); `LGSPEC1`: `Mood=Qot`/`Evident=Nfh` on 14 tokens.
* **kmr `LGSPEC1`**: `Case=Con` on 67%. **tur `LGSPEC1`**: `Aspect=Perf` on 67%. **lat `LGSPEC1`**: homograph noise. **deu `LGSPEC01`**: follows from `NFIN` meaning infinitive in German.
* **No UD counterpart:** spa `LGSPEC1/2` (`-ra`/`-se` imperfect subjunctive: UD has `Mood=Sub`, `Tense=Imp` for both), amh orthographic variants, ckb clitic labels, hun `LGSPEC1-3`, kat `LGSPEC2` (archaic plural).
