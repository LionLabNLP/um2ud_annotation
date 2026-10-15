# Zeman https://github.com/dan-zeman/interset/blob/master/lib/Lingua/Interset/Tagset/MUL/Unimorph.pm

import itertools
import re
from functools import lru_cache
from typing import Optional

shortened_vals = dict(sorted({
    "AB":   {"Case": "Abs"},     # absolutive
    "ABS":  {"Case": "Abs"},     # absolutive
    "AC":   {"Case": "Acc"},     # accusative
    "ACC":  {"Case": "Acc"},     # accusative
    "BE":   {"Case": "Ben"},     # benefactive
    "BEN":  {"Case": "Ben"},     # benefactive
    "DA":   {"Case": "Dat"},     # dative
    "DAT":  {"Case": "Dat"},     # dative
    "ER":   {"Case": "Erg"},     # ergative
    "ERG":  {"Case": "Erg"},     # ergative
    "NO":   {"Case": "Nom"},     # nominative
    "NOM":  {"Case": "Nom"},     # nominative
    "F":    {"Gender": "Fem"},   # Feminine
    "FEM":  {"Gender": "Fem"},   # Feminine
    "M":    {"Gender": "Masc"},  # Masculine
    "MASC": {"Gender": "Masc"},  # Masculine
    "P":    {"Number": "Plur"},  # Plural, arg marking
    "PL":   {"Number": "Plur"},  # Plural, arg marking
    "SG":   {"Number": "Sing"},  # Singular, arg marking
    "S":    {"Number": "Sing"},  # Singular, arg marking
    "INFM": {"Polite": "Infm"},  # basque
    "D":    {"Definite": "Cons"},# Construct state; UM Chuckchi, Hebrew
}.items(), key=lambda x: len(x[0]), reverse=True))

UM2UD_values = dict(sorted({
    # AKTIONSART
    "STAT": {},  # stative

    # ANIMACY
    "ANIM": {"Animacy": "Anim"},  # Animate
    "HUM":  {"Animacy": "Hum"},   # Human
    "INAN": {"Animacy": "Inan"},  # Inanimate

    # ASPECT
    "FREQ":  {"Aspect": "Freq"},    # lithuanian; not in UM docs, but found in UM data
    "HAB":   {"Aspect": "Hab"},     # Habitual
    "IPFV":  {"Aspect": "Imp"},     # imperfective
    "ITER":  {"Aspect": "Iter"},    # Iterative
    "PFV":   {"Aspect": "Perf"},    # perfective, UM specific
    "PRF":   {"Aspect": "Perf"},    # Perfect
    "PROG":  {"Aspect": "Prog"},    # Progressive
    "PROSP": {"Aspect": "Prosp"},   # Prospective

    # Aktionsart to aspect
    "DUR": {"Aspect": "Dur"},   # found in UD data

    # CASE
    "ABL":   {"Case": "Abl"},   # Ablative
    "ABS":   {"Case": "Abs"},   # Absolutive
    "ACC":   {"Case": "Acc"},   # Accusative
    "ALL":   {"Case": "All"},   # Allative
    "AT":    {"Case": "Ade"},   # adessive Zeman
    "APPRX": {},                # approximative; Zeman, ail, krl, lud, olo, vep: no UD correspondence, kept as UM:APPRX
    "BEN":   {"Case": "Ben"},   # benefactive
    "BYWAY": {"Case": "Ess"},   # Zeman
    "COM":   {"Case": "Com"},   # Comitative
    "COMPV": {"Case": "Cmp"},   # comparative
    "DAT":   {"Case": "Dat"},   # Dative
    "ERG":   {"Case": "Erg"},   # Ergative
    "EQTV":  {"Case": "Equ"},   # equative, UM: EQTV exclusive to nouns (adj have eqt)
    "ESS":   {"Case": "Loc"},   # UM essive = UD locative while UM formal = ud essive, according to Zeman
    "FRML":  {"Case": "Ess"},   # Zeman
    "GEN":   {"Case": "Gen"},   # Genitive
    "INS":   {"Case": "Ins"},   # Instrumental
    "IN":    {"Case": "Ine"},   # inessive Zeman
    "IN+ESS":{"Case": "Ine"},   # apparently same as IN+ESS according to UM docs; not in UM docs, but found in UM data
    # the other location-case compounds: each is ONE case, not an ambiguity; checked against
    # UD Case=X tokens' rows in the fi/hu/et/se UM files (~90-98% of tokens carry exactly this tag)
    "IN+ABL":{"Case": "Ela"},   # elative
    "IN+ALL":{"Case": "Ill"},   # illative
    "AT+ESS":{"Case": "Ade"},   # adessive
    "AT+ABL":{"Case": "Abl"},   # ablative (outer)
    "AT+ALL":{"Case": "All"},   # allative
    "ON+ESS":{"Case": "Sup"},   # superessive
    "ON+ABL":{"Case": "Del"},   # delative
    "ON+ALL":{"Case": "Sbl"},   # sublative
    "LOC":   {"Case": "Loc"},   # not in UM docs, but found in UM data
    "NOM":   {"Case": "Nom"},   # Nominative
    "ON":    {"Case": "Sup"},   # Zeman
    "OBL":   {"Case": "Acc"},   # gujarati oblique, only as OBL+VOC; the treebank marks oblique nouns Case=Acc (chosen, 2026-10)
    "PRIV":  {"Case": "Abe"},   # abessive / caritive / privative (UD) vs privative (UM)
    "PRP":   {"Case": "Prp"},   # purposive
    "PRT":   {"Case": "Par"},   # partitive
    "PROPR": {"Case": "Com"},   # proprietive, Zeman, not in UM data
    "REL":   {"Case": "Rel"},   # Zeman
    "SUB":   {"Case": "Sub"},   # Sublative (UM: Under)
    "TERM":  {"Case": "Ter"},   # terminative Zeman
    "TRANS": {"Case": "Tra"},   # translative
    "PROL":  {"Case": "Tra"},   # prolative/translative
    "VOC":   {"Case": "Voc"},   # Vocative

    # CLUSIVITY
    "EXCL": {"Clusivity": "Ex"},  # Exclusive
    "INCL": {"Clusivity": "In"},  # Inclusive

    # DEFINITENESS
    "DEF": {"Definite": "Def"},    # Definite
    "INDF": {"Definite": "Ind"},   # Indefinite
    "SPEC": {"Definite": "Spec"},  # Specific
    "NDEF": {"Definite": "Ind"},   # Indefinite 
    # UM nspec?

    # DEGREE
    "AB":   {"Degree": "Abs"},  # absolute superlative
    "CMPR": {"Degree": "Cmp"},  # Comparative
    "EQT":  {"Degree": "Equ"},  # Equative
    "SPRL": {"Degree": "Sup"},  # also used as superlative tag in UM with SUP(?) in afrikaans
    "SUP":  {"Degree": "Sup"},  # not in UM docs, but found in UM data
    # ell tags superlatives SPRL;AB (one reading, not two): UD Greek tokens of these forms are Degree=Sup, 16 of 17 (2026-10)
    "SPRL+AB": {"Degree": "Sup"},
    "AB+SPRL": {"Degree": "Sup"},

   # DEIXIS
    "MED":  {"Deixis": "Med"},   # Medial, not in UM data
    "PROX": {"Deixis": "Prox"},  # Proximate
    "REMT": {"Deixis": "Remt"},  # Remote
    # more deixis tags are matching, but dont occurr in our data

    # EVIDENTIALITY
    "FH":   {"Evident": "Fh"},   # Firsthand
    "NFH":  {"Evident": "Nfh"},  # Non-firsthand

    # GENDER
    "FEM":  {"Gender": "Fem"},   # Feminine
    "MASC": {"Gender": "Masc"},  # Masculine
    "NEUT": {"Gender": "Neut"},  # Neuter
    "COMN": {"Gender": "Com"},   # Common (Danish/Swedish/Dutch/... -- not a
                                 # real UM tag, see UM_tagset.py's own entry

    # INFORMATION STRUCTURE
    "FOC": {"InfStruct": "Foc"},  # Focus
    "TOP": {"InfStruct": "Top"},  # Topic

    # INTERROGATIVITY
    "DECL": {},  # Zeman; NOT Mood=Ind: tur has every IND and INFR row twice, with and without DECL, and DECL also occurs on IMP and mood-less rows; kor DECL never co-occurs with a mood; UD has no interrogativity feature (2026-10)

    # MOOD
    "ADM":   {"Mood": "Adm"},   # admirative
    "AUPRP": {"Mood": "PRP"},   # Australian Purposive, Zeman, not in UM data
    "COND":  {"Mood": "Cnd"},   # Conditional
    "HYP":   {"Mood": "Cnd,Pot"},  # basque hypothetical (earlier note: neither conditional nor potential); UD Basque tokens of these forms: 84% Cnd, 16% Pot, so both readings (2026-10)
    "DED":   {},                # Deductive, Zeman, Yakut
    "DEB":   {"Mood": "nec"},   # Debitive, Zeman, not in UM data
    "INFR":  {"Evident": "Nfh"},  # inferential, tur -mis; UD Turkish tokens of INFR forms: 86% Evident=Nfh, 0% of the rest (form match; 2026-10)
    "IMP":   {"Mood": "Imp"},   # Imperative-Jussive
    "IND":   {"Mood": "Ind"},   # Indicative
    "INT":   {"Mood": "Int"},   # UM has its own "interrogativity" feature with only INT and DECL(arative) as values
    "INTEN": {"Mood": "Des"},   # Zeman
    "IRR":   {"Mood": "Irr"},   # didnt occur but is in um docs
    "OBLIG": {"Mood": "Nec"},   # both have "must" meaning
    "OPT":   {"Mood": "Opt"},   # Optative-Desiderative
    "PERM":  {"Mood": "Perm"},  # Permissive
    "POT":   {"Mood": "Pot"},   # Potential
    "PURP":  {"Mood": "Prp"},   # didnt occur but is in um docs
    "REAL":  {"Mood": "Ind"},   # Realis, Zeman, not in UM data
    "SBJV":  {"Mood": "Sub"},   # Subjunctive
    "SIM":   {},                # Simulative
    "QUOT":  {"Mood": "Qot"},   # is evident in UM, but is mood in UD (specifically for estonian)

    # NOUN TYPE
    "STRONG":   {"NounType": "Strong"},  # not in UM docs, but found in UM data
    "WEAK":     {"NounType": "Weak"},    # not in UM docs, but found in UM data

    # NOUN CLASSES (Nakh-Daghestanian1-8 in UM)

    # NUMBER
    "DU":    {"Number": "Dual"},    # Dual
    "GRPL":  {"Number": "Grpl"},    # greater plural, in UM and UD docs, not in data
    "GPAUC": {"Number": "Grpa"},    # greater paucal, in UM and UD docs, not in data
    "INVN":  {"Number": "Inv"},     # inverse; in UM and UD docs, not in data
    "PAUC":  {"Number": "Pauc"},    # in UM docs, not in data
    "PL":    {"Number": "Plur"},    # Plural
    "SG":    {"Number": "Sing"},    # Singular
    "TRI":   {"Number": "Tri"},     # trial

    # PERSON
    "0":    {"Person": "0"},    # Zero person
    "1":    {"Person": "1"},    # First person
    "2":    {"Person": "2"},    # Second person
    "3":    {"Person": "3"},    # Third person
    "4":    {"Person": "4"},    # hungarian PSS UM
    "AUTO": {"Person": "0"},    # irish impersonal/autonomous form, person=0 according to UD treebank readme; not in UM docs, but found in UM data
    "IMPRS":{"Person": "0"},    # Impersonal, Zeman, not in UM data

    # "INF": "Informal", # used as basuqe person, how does UD handle this?
    # ud doesnt have obviative

    # POLARITY
    "NEG": {"Polarity": "Neg"},  # Negative
    "POS": {"Polarity": "Pos"},  # Positive

    # POLITENESS
    "ELEV": {"Polite": "Elev"},  # Referent Elevating
    "FORM": {"Polite": "Form"},  # Formal
    "HUMB": {"Polite": "Humb"},  # Speaker Humbling
    "INFM": {"Polite": "Infm"},  # Informal
    "POL":  {"Polite": "Form"},  # Zeman

    # STYLE
    "COL":   {"Style": "Coll"}, # Zeman; og politeness
    "LIT":   {"Style": "Lit"},  # Literary
    "FOREG": {"Style": "Form"}, # Zeman

    # SUBCAT
    "INTR": {"SubCat": "Intr"},  # Intransitive
    "TR":   {"SubCat": "Tran"},  # Transitive

    # TENSE
    "FUT": {"Tense": "Fut"},   # Future
    "PRS": {"Tense": "Pres"},  # Present
    "NPST": {"Tense": "Pres"}, # yakut non-past; UD Yakut tokens of these forms: 98% Tense=Pres (2026-10 check)
    "PST": {"Tense": "Past"},  # Past

    # UPOS
    "ADJ":      {"upos": "ADJ"},      # Adjective
    "ADJ.CVB":  {"upos": "ADJ"},      # korean, CVB on ADJ?
    "ADJ.MSDR": {"upos": "ADJ"},      # korean, MSDR on ADJ?
    "ADJ.PTCP": {"upos": "ADJ"},      # korean, yakut, PTPC on ADJ?
    "ADP":      {"upos": "ADP"},      # Adposition
    "ADV":      {"upos": "ADV"},      # Adverb
    "ART":      {"upos": "DET",
                 "PronType": "Art"},  # Article, Afrikaans
    "AUX":      {"upos": "AUX"},      # Auxiliary, only Xibe has AUX
    "CONJ":     {"upos": "CONJ"},     # Conjunction, Zeman, strictly not UD (CCONJ vs SCONJ)
    "CLF":      {"upos": "NOUN",      # Classifier, Zeman, not in UM data
                 "NounType": "Class"},
    "DET":      {"upos": "DET",
                 "PronType": "Prn"},  # Determiner, prontype according to Zeman; chukchi, karelian, xibe
    "INTJ":     {"upos": "INTJ"},     # Interjection
    "N":        {"upos": "NOUN"},     # Noun
    "NUM":      {"upos": "NUM",       # Numeral
                 "NumType": "Card"},
    "PART":     {"upos": "PART"},     # Particle
    "PRO":      {"upos": "PRON",      # Pronoun, Zeman,not in UM docs, but found in UM data
                 "PronType": "Prn"},
    "PROPN":    {"upos": "PROPN",     # Proper Noun
                 "NounType": "Prop"},
    "V":        {"upos": "VERB"},     # AUX?
    "V.PTCP":   {"upos": "VERB",      # Participle (Verbal Adjective)
                 "VerbForm": "Part"},
    "V.CVB":    {"upos": "VERB",      # Converb (Verbal Adverb)
                 "VerbForm": "Conv"},
    "V.MSDR":   {"upos": "VERB",      # Zeman
                 "VerbForm": "Vnoun"},
    "V.NFIN":   {"upos": "VERB",      # not in UM docs, but found in UM data
                 "VerbForm": "NonFin"},
    "PRE":      {"upos": "ADP"},      # preposition, used in livvi, veps; not in UM docs, but found in UM data

    # (VALENCY)
    "REFL": {"Reflex": "yes"},  # Zeman
    "DITR": {"SubCat": "Tran"}, # Ditransitive, Zeman, not in UM data

    # VERBFORM
    "BASE":   {"Degree": "Pos"},       # synthetic: unimorph.py's positive-degree code (UD2UM Degree=Pos, "POS" on ADJ/ADV)
    "SUPI":   {"VerbForm": "Sup"},     # supine; synthetic, UM has no supine tag (SUP is taken by Degree)
    "FIN":    {"VerbForm": "Fin"},     # Finite
    "NFIN":   {"VerbForm": "NonFin"},  # found in ud data but isnt in ud verbform docs; pr inf?
    # double check w ud
    "INF":    {"VerbForm": "Inf"},                    # not in UM docs, but found in UM data
    "PTCP":   {"upos": "VERB", "VerbForm": "Part"},   # not in UM docs, but found in UM data
    "CVB":    {"VerbForm": "Conv"},                   # Zeman; not in UM docs, but found in UM data
    "MSDR":   {"VerbForm": "Vnoun"},                  # Zeman; bare form of V.MSDR, e.g. "V;MSDR" combination
    "COP":    {"VerbForm": "Cop"},                    # Zeman; kmr (Kurmanji) copula
    "DIM":    {"Degree": "Dim"},                      # Zeman; diminutive, itl (Itelmen)
    "PSSD":   {"Definite": "Cons"},                   # heb possessed noun = construct state; UD Hebrew nouns of PSSD forms: 88% Definite=Cons vs 24% of the rest (2026-10)
    "ALN":    {"Poss": "Yes"},                        # Zeman; alienable possession, evn (Evenki)
    "PSS":    {"Poss": "Yes"},                        # Zeman; bare possessive marker (distinct from the
                                                       # PSS1S/PSS3PM/... argument-marking compounds --
                                                       # see parse_ufeat_value's ARG/PSS branch), ket (Ket), hun (the "-é" forms: no possessor given)
    "INCH":   {"Aspect": "Inch"},                     # Zeman; inchoative, ail (Aikanã)
    "PRON":   {"upos": "PRON"},                       # Zeman; hsi (Xasi/Caiapo)

    # VOICE
    "ACT":   {"Voice": "Act"},    # Active
    "AGFOC": {"Voice": "AgFoc"},  # Agent Focus
    "ANTIP": {"Voice": "Antip"},  # Antipassive
    "APPL":  {"Voice": "Appl"},   # applicative; only ind has it in UM (UD Indonesian has no Voice=Appl, other treebanks do)
    "BFOC":  {"Voice": "Bfoc"},   # from UM docs
    "CAUS":  {"Voice": "Cau"},    # valency to voice
    "DIR":   {"Voice": "Dir"},    # from docs
    "IFOC":  {"Voice": "Ifoc"},   # from UM docs
    "INV":   {"Voice": "Inv"},    # Inverse
    "LFOC":  {"Voice": "Lfoc"},   # from UM docs
    "MID":   {"Voice": "Mid"},    # Middle
    "PASS":  {"Voice": "Pass"},   # Passive
    "PFOC":  {"Voice": "Pass"},   # Patient Focus
    "RECP":  {"Voice": "Rcp"},    # valency to voice

    # OBJ
    "IO": {"Case": "IO"},  # indirect object?? for argument marking; not in UM docs, but found in UM data

}.items(), key=lambda x: len(x[0]), reverse=True))

for cls in (f"Bantu{i+1}" for i in range(23)):
    UM2UD_values[cls.upper()] = {"NounClass": cls}


def _primary_feat(ud_feats: dict) -> str:
    """The UD feature a UM2UD_values entry is about: its first non-upos key ("V.PTCP" -> VerbForm),
    else "upos" for a upos-only tag."""
    return next((f for f in ud_feats if f != "upos"), next(iter(ud_feats)))


# Bare UM tag -> its primary UD feature, e.g. val2feat["PL"] == "Number". Built from UM2UD_values
# only: the 1-2 letter codes of shortened_vals are only unambiguous in argument/possessor context.
val2feat = {tag: _primary_feat(ud_feats) for tag, ud_feats in UM2UD_values.items() if ud_feats}
feat2val: dict = {}
for _val, _feat in val2feat.items():
    feat2val.setdefault(_feat, []).append(_val)


from .UM_gaps import blacklist, missing, unk_values   # the UM tags with no UD mapping, see UM_gaps.py

fix_typos = {
    "V.CV":    "V.CVB",   # korean
    "INST":    "INS",     # UM INST vs INS case? Only found docs on INS=instrumental but INST is used by a number of langs, together with INS; not in UM docs, but found in UM data
    "MASV":    "MASC",    # irish
    "SUBJ":    "SBJV",    # portugese
    "V.PCTP":  "V.PTCP",  # slovenian
    "PCTP":    "PTCP",    # bare form of V.PCTP; not in the current data
    "CV":      "CVB",     # bare form of V.CV (korean); not in the current data
    "PRES":    "PRS",     # basque, sanskrit, yiddish
    "PAST":    "PST",     # basque
    "ARBAB1S": "ARGAB1S", # chukchi
    "ARBAB3S": "ARGAB3S", # chukchi
    "AJD":     "ADJ",     # typo, xcl (Classical Armenian)
}


# "any value but X" (pashto (non)NOM, old french non{NOM}, hsi non{NOM/ACC}, gup non{PST}): UD has no
# negated values. Recognised once the negated values resolve to a feature, so this covers any feature.
NEGATION_PATTERN = re.compile(r"^(?:\(NON\)|NON|NOT)\{?([^{}]+?)\}?$")
NEGATION_PREFIX = "non"
NEGATION_SEP = "|"   # canonical code: "nonNOM", "nonNOM|ACC"


def parse_negation(val):
    """The (typo-fixed) UM values a negated `val` excludes, e.g. "not{NOM}" -> ["NOM"],
    "non{NOM/ACC}" -> ["NOM", "ACC"]; None if `val` is not a negation (a value that resolves to
    no feature is not accepted either)."""
    val = val.strip().upper()
    if val in UM2UD_values or val in shortened_vals:
        return None
    match = NEGATION_PATTERN.match(val)
    if not match:
        return None
    inner = [fix_typos.get(v, v) for v in re.split(r"[/+,|]", match.group(1)) if v]
    if not inner or any(val2feat.get(v) is None and unk_values.get(v) is None for v in inner):
        return None
    return inner


def negation_feature(val):
    """The feature of the values a negated `val` excludes (`parse_negation`), else None."""
    inner = parse_negation(val)
    return None if inner is None else (val2feat.get(inner[0]) or unk_values.get(inner[0]))


def negation_code(inner):
    """Canonical code for a negation of the UM values `inner`: "nonNOM", "nonNOM|ACC"."""
    return NEGATION_PREFIX + NEGATION_SEP.join(inner)


# UM "POS" is polarity on verbs but the positive degree on adjectives/adverbs (swe, lit, ind)
VERBAL_FEATURES = {"VerbForm", "Tense", "Mood", "Aspect", "Person", "Voice", "Evidentiality", "Evident",
                   "Interrogativity", "Polite"}


def pos_is_degree(upos, features) -> bool:
    """True if UM "POS" in a row of this upos with these UM features (feature names) is Degree=Pos."""
    return upos in ("ADJ", "ADV") and not any(
        f.partition("[")[0] in VERBAL_FEATURES and not f.endswith("[psor]") for f in features)


def parse_complex_um_value(complx_ufeat, lookup_spaces, ufeat_type=None):
    # handles ARG marking and PSS marking
    complx_ufeat = re.sub(ufeat_type, "", complx_ufeat)
    parsed = list()
    case_id = None
    for space in lookup_spaces:
        if complx_ufeat:
            for um_value, ud_map in space.items():
                # try to match longest value UM string
                for um_value, ud_map in space.items():
                    if re.findall(um_value, complx_ufeat):
                        # remove matched value
                        complx_ufeat = re.sub(um_value, "", complx_ufeat)
                        # add matched value to parsed feature: value mapping
                        for feature, value in ud_map.items(): 
                            if ufeat_type=="ARG" and feature=="Case":
                                case_id = value.lower()
                            else:
                                parsed.append((feature, value))
    return {feat+f"[{case_id if case_id else "psor"}]": val 
            for feat, val in parsed}


def _notice(message, log_file=None):
    """Print `message`, or append it to the txt file `log_file` if given."""
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


def _gap_category(val):
    return blacklist.get(val) or unk_values.get(val) or missing.get(val) or ("Language_Specific" if LGSPEC_PATTERN.fullmatch(val.upper()) else None)


def parse_ufeat_value(ufeat, warn_unknown=True, warn_known_gaps=True, log_file=None, unmapped=None):
    # input is ONE ufeat subvalue (arg/pssd ok, but no disj/conj); `unmapped`: a list that collects
    # {"tag", "status", ...} records for what could not be mapped
    primary_space = (shortened_vals if ufeat in shortened_vals else UM2UD_values)
    parsed = dict()
    # special case for complex strings used in argument marking/possession
    # Argument marking: ARGNO2S -> {'Number[nom]': 'Sing', 'Person[nom]': '2'}
    # Possession: PSS1S -> {'Number[psor]': 'Sing', 'Person[psor]': '1'}
    if ufeat in primary_space and ufeat.startswith(("ARG", "PSS")):
        # an exact entry wins over the argument/possessor decomposition (PSSD is not PSS + D)
        parsed = dict(primary_space[ufeat])
    elif ufeat.startswith("ARG") or ufeat.startswith("PSS"):
        parsed = parse_complex_um_value(ufeat, [shortened_vals, UM2UD_values],
                                         re.match(r"(ARG|PSS)", ufeat).group(1))
        if (not parsed) and (ufeat in primary_space):
            # a bare "PSS" (Ket's generic possessive) has no person/number to decompose: plain lookup
            parsed = dict(primary_space[ufeat])
    elif ufeat in primary_space:
        # simples case_ add the corresponding UD morpho annotation
        # NOM -> {"Case": "Nom"}
        parsed = dict(primary_space[ufeat])

    elif is_known_gap(ufeat):
        if unmapped is not None:
            unmapped.append({"tag": ufeat, "status": "known_gap", "category": _gap_category(ufeat)})
        if warn_known_gaps:
            _notice(f"Note: known gap, no UD mapping: {ufeat}", log_file)
    else:
        if unmapped is not None:
            unmapped.append({"tag": ufeat, "status": "unknown", "category": None})
        if warn_unknown:
            _notice(f"Warning: Unknown Unimorph value {ufeat}", log_file)
    return parsed


# A feature's value is kept as a set of alternatives; an alternative is a frozenset of values that
# hold together: {Plur, Sing} for SG+PL (both), {Fem} and {Masc} for MASC/FEM (either).
def _alternatives(val):
    return {frozenset([v]) for v in (val.split(",") if isinstance(val, str) else [val])}


def add_readings(readings, new):
    """Add the {feature: value} dict `new` to `readings` ({feature: set of alternatives}); a comma
    value ("Cnd,Pot") is two alternatives. Alternatives of different tags (HYP;POT) or of a
    disjunction (MASC/FEM) are added side by side."""
    for feat, val in new.items():
        readings.setdefault(feat, set()).update(_alternatives(val))
    return readings


def conjoin_readings(parts):
    """Combine {feature: alternatives} dicts that hold together (SG+PL): on a feature several parts
    state, every alternative of one is joined with every alternative of the next."""
    out = {}
    for part in parts:
        for feat, alts in part.items():
            out[feat] = set(alts) if feat not in out else {a | b for a in out[feat] for b in alts}
    return out


def render_readings(feat, alts, keep_conjunctions=False):
    """The output value of a feature: sorted "A,B" (either). With keep_conjunctions, values that hold
    together are joined with "+" and "," separates the alternatives: "Plur+Sing", "Fem,Masc"."""
    if feat == "VerbForm" and len(set().union(*alts)) > 1:
        alts = {a - {"NonFin"} for a in alts} - {frozenset()}   # let more specific verbform override generic nonfin
    if not keep_conjunctions:
        return ",".join(sorted(set().union(*alts)))
    return ",".join("+".join(sorted(a)) for a in sorted(alts, key=lambda a: sorted(a)))


def _piece_readings(ufeat, **kwargs):
    """{feature: alternatives} of one ";"-piece. "/" and "," bind tighter than "+": "ON/AT+ABL" is
    ON+ABL or AT+ABL, each looked up as a known compound tag if there is one."""
    groups = [[alt.strip() for alt in re.split(r"[/,]", group) if alt.strip()] for group in ufeat.split("+")]
    result = {}
    for combo in itertools.product(*groups):
        name = "+".join(combo)
        if len(combo) > 1 and name in UM2UD_values:
            parts = [{feat: _alternatives(val) for feat, val in UM2UD_values[name].items()}]
        else:
            parts = [{feat: _alternatives(val) for feat, val in parse_ufeat_value(part, **kwargs).items()}
                     for part in combo]
        for feat, alts in conjoin_readings(parts).items():
            result.setdefault(feat, set()).update(alts)
    return result


# UniMorph's numbered language-specific placeholder tags (LGSPEC1, LGSPEC01, ...): their meaning
# differs per language, so by default they are stripped (see LGSPEC_UD for the mapped ones).
LGSPEC_PATTERN = re.compile(r"L(?:GSPEC|SGSPEC|GSEPC|GSPEPC)\d*(?:\([^)]*\))?")   # also the typos found in the data, a bare LGSPEC, and ckb's "LGSPEC4(DA)"


# LGSPEC tags with a UD meaning, used by map_um_value_to_ud(..., lang=): {language: {tag as written in
# the data: {UD feature: UD value}}}. The value replaces the other tags' value for that feature (sah
# PST;LGSPEC1 is NearPast, not Past). Meaning: the language's UniMorph README; evidence: UD tokens of
# the forms that carry the tag (details in LGSPECs.md).
LGSPEC_UD = {
    # afr: README "Diminutive form for nouns and proper nouns" (inkpot -> inkpotjie, N;SG;LGSPEC3).
    #   UD: Degree=Dim on 75% of 16 matched tokens (koekies, knoppie, kaartjies). Small sample.
    #   README "Predicative inflection (base form) for adjective" / "Attributive inflection for
    #   adjective" (LGSPEC1 / LGSPEC2). Raw UD 2.18 (AfriBooms ADJ tokens): AdjType=Pred on 96% of
    #   392 tokens of LGSPEC1 forms, AdjType=Attr on 99.6% of 2,070 of LGSPEC2 forms. AdjType has
    #   no UM tag of its own.
    "afr": {"LGSPEC1": {"AdjType": "Pred"}, "LGSPEC2": {"AdjType": "Attr"}, "LGSPEC3": {"Degree": "Dim"}},
    # kat: README "Adverbial case" (-ad forms of nouns/adjectives). The Georgian UD table has no
    #   Case=Adv; the adverbial is annotated Ess: 100% of 141 matched tokens.
    "kat": {"LGSPEC1": {"Case": "Ess"}},
    # got: README "Strong (indefinite) / Weak (definite) inflection for adjective". Raw UD 2.18
    #   (PROIEL ADJ tokens): Strength=Strong on 100% of 813 tokens of LGSPEC01 forms, Strength=Weak
    #   on 92% of 203 of LGSPEC02 forms. Strength has no UM tag of its own.
    "got": {"LGSPEC01": {"Strength": "Strong"}, "LGSPEC02": {"Strength": "Weak"}},
    # hye: README "resultative" (V.PTCP;LGSPEC01, -ac forms). UD: Aspect=Perf on 93% of 246 matched
    #   tokens (VerbForm=Part 94%, already given by V.PTCP).
    "hye": {"LGSPEC01": {"Aspect": "Perf"}},
    # sah: README "PST;LGSPEC1: definite past tense (assertive past, recent past)" and
    #   "PST;LGSPEC2: indefinite past tense (non-assertive past)". UD: NearPast on 100% of 25 matched
    #   tokens; PastPerf on 89% of 9 (small samples; LGSPEC2 is the weaker match for its README text).
    "sah": {"LGSPEC1": {"Tense": "NearPast"}, "LGSPEC2": {"Tense": "PastPerf"}},
}
# UD features only the LGSPEC mappings produce (no UM2UD_values entry); a consumer that keeps the
# features of UM2UD_values should keep these too
LGSPEC_UD_FEATURES = {feat for tags in LGSPEC_UD.values() for ud in tags.values() for feat in ud}


def um_tag_upos(tag: str) -> Optional[str]:
    """The UD upos a bare UM tag implies, e.g. "ART" -> "DET", "PRO" -> "PRON",
    "PRE" -> "ADP", "V" -> "VERB"; None if the tag implies no upos (or is
    unknown). Normalizes known typos first (fix_typos).
    """
    return UM2UD_values.get(fix_typos.get(tag, tag), {}).get("upos")


def feature_for(val: str) -> Optional[str]:
    """The UM feature category of a bare UM value, mapped or not: val2feat's entry, else its category
    in unk_values/blacklist, else "Language_Specific" for an LGSPEC tag, else None (unrecognized).
    Known typos are fixed first, as in map_um_value_to_ud."""
    val = fix_typos.get(val, val)
    if val in val2feat:
        return val2feat[val]
    if LGSPEC_PATTERN.fullmatch(val.upper()):
        return "Language_Specific"
    if val in blacklist:
        return blacklist[val]
    if val in unk_values:
        return unk_values[val]
    return negation_feature(val)


def is_known_gap(val: str) -> bool:
    """True for a UM value this package knows and deliberately leaves unmapped: blacklist, unk_values,
    missing, LGSPEC placeholders and negations (a gap, as opposed to a value it has never seen)."""
    val = fix_typos.get(val, val)
    return (val in blacklist or val in unk_values or val in missing
            or LGSPEC_PATTERN.fullmatch(val.upper()) is not None or negation_feature(val) is not None)


def map_um_value_to_ud(ufeat_raw, warn_unknown=True, warn_known_gaps=True, return_unmapped=False,
                       keep_conjunctions=False, log_file=None, lang=None):
    """A UniMorph feature string as {"morpho": {UD feature: value}, "upos": upos or None}.

    Several values for one feature come back as one sorted "A,B" value (either). With
    `keep_conjunctions`, values UniMorph joins with "+" are kept apart from alternatives: SG+PL is
    "Plur+Sing", MASC/FEM is "Fem,Masc" ("," separates alternatives). Separate tags of one feature
    (HYP;POT) are always alternatives.

    `warn_unknown` prints values this package has never seen; `warn_known_gaps` prints a note for
    the known, deliberately unmapped ones (blacklist, unk_values, missing, negations; LGSPEC
    placeholders are stripped first and never noted). `log_file` appends these messages to a txt
    file instead of printing them. `return_unmapped` adds an "unmapped" list to the result with
    one record per tag that has no UD value: {"tag", "status": unknown | known_gap | negation,
    "category"} (negations also list the excluded UM values).

    `lang` (UniMorph language code) applies that language's entries of `LGSPEC_UD`: its mapped
    LGSPEC tags give their UD value, replacing the other tags' value for that feature. Without
    `lang`, and for LGSPEC tags without an entry, they are stripped."""
    ufeat_string = str(ufeat_raw)
    if ufeat_string=="nan":  # this happens for eg eng.segmentations entries
        return {}
    readings = dict()
    unmapped = []
    ufeat_string = ufeat_string.upper().replace(":", ";")
    lgspec_ud = LGSPEC_UD.get(lang, {}) if lang else {}
    lgspec_values = {feat: val for tag in LGSPEC_PATTERN.findall(ufeat_string)
                     for feat, val in lgspec_ud.get(tag, {}).items()}
    ufeat_string = LGSPEC_PATTERN.sub("", ufeat_string)   # unmapped LGSPEC tags are dropped
    kwargs = dict(warn_unknown=warn_unknown, warn_known_gaps=warn_known_gaps, log_file=log_file, unmapped=unmapped)
    for ufeat in ufeat_string.split(";"): # normal split
        ufeat = ufeat.strip() # rm trailing whitespaces 
        ufeat = fix_typos.get(ufeat, ufeat)
        if ufeat in ("", "-"):
            continue
        excluded = parse_negation(ufeat)
        if (ufeat in blacklist) or (ufeat in unk_values) or excluded is not None:
            # skip: dont know what to map these to
            if excluded is not None:
                unmapped.append({"tag": ufeat, "status": "negation", "category": negation_feature(ufeat), "excluded": excluded})
            else:
                unmapped.append({"tag": ufeat, "status": "known_gap", "category": _gap_category(ufeat)})
            if warn_known_gaps:
                _notice(f"Note: known gap, no UD mapping: {ufeat}", log_file)
            continue
        for feat, alts in _piece_readings(ufeat, **kwargs).items():
            readings.setdefault(feat, set()).update(alts)

    for feat, val in lgspec_values.items():
        readings[feat] = {frozenset([val])}
    out_format = {k: render_readings(k, v, keep_conjunctions) for k, v in sorted(readings.items())}
    if out_format.get("Polarity") == "Pos" and pos_is_degree(
            out_format.get("upos"), [f for f in out_format if f not in ("upos", "Polarity")]):
        del out_format["Polarity"]
        out_format.setdefault("Degree", "Pos")
    result = {"morpho": {k: v for k, v in out_format.items() if k!="upos"},
              "upos": out_format.get("upos", None)}
    if return_unmapped:
        result["unmapped"] = list({tuple(sorted((k, str(v)) for k, v in r.items())): r for r in unmapped}.values())
    return result



# Vocabulary for readers of raw UniMorph feature strings (exported for consumers)
UM2UD = UM2UD_values            # UM tag -> its {UD feature: UD value} dict (UM2UD["V.PTCP"] == {"upos": "VERB", "VerbForm": "Part"})
SHORTENED_UM_VALS = shortened_vals
COMPOUND_TAGS = {tag for tag in UM2UD_values if "+" in tag}   # "+" tags known as one value; any other "+" is an ambiguity

# Raw UM upos codes, checked before feature_for(): several are also values of other features
# (DET/ART/PRO as PronType, PROPN as NounType, NUM as NumType).
UPOS_VALUES = {
    "N", "PROPN", "ADJ", "PRO", "CLF", "ART", "DET", "V", "ADV", "AUX",
    "ADP", "CONJ", "NUM", "PART", "INTJ", "AJD", "PRE", "ADJ.CVB",
    "PRON",
}


@lru_cache(maxsize=None)
def cached_map_um_value_to_ud(val: str):
    """map_um_value_to_ud, cached (its ARG*/PSS* parsing scans the whole vocabulary per call).
    Repeated readings are collapsed: comma values come back as sorted unique readings."""
    mapped = map_um_value_to_ud(val)
    morpho = {
        feat: ",".join(sorted(set(v.split(",")))) if isinstance(v, str) and "," in v else v
        for feat, v in mapped["morpho"].items()
    }
    return {**mapped, "morpho": morpho}
