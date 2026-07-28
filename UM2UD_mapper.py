# dan https://github.com/dan-zeman/interset/blob/master/lib/Lingua/Interset/Tagset/MUL/Unimorph.pm

import re

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
    "AT":    {"Case": "Ade"},   # adessive dan
    "APPRX": {},                # dan
    "BEN":   {"Case": "Ben"},   # benefactive
    "BYWAY": {"Case": "Ess"},   # dan
    "COM":   {"Case": "Com"},   # Comitative
    "COMPV": {"Case": "Cmp"},   # comparative
    "DAT":   {"Case": "Dat"},   # Dative
    "ERG":   {"Case": "Erg"},   # Ergative
    "EQTV":  {"Case": "Equ"},   # equative, UM: EQTV exclusive to nouns (adj have eqt)
    "ESS":   {"Case": "Loc"},   # UM essive = UD locative while UM formal = ud essive, according to dan
    "FRML":  {"Case": "Ess"},   # dan
    "GEN":   {"Case": "Gen"},   # Genitive
    "INS":   {"Case": "Ins"},   # Instrumental
    "IN":    {"Case": "Ine"},   # inessive dan
    "IN+ESS":{"Case": "Ine"},   # apparently same as IN+ESS according to UM docs; not in UM docs, but found in UM data
    "LOC":   {"Case": "Loc"},   # not in UM docs, but found in UM data
    "NOM":   {"Case": "Nom"},   # Nominative
    "ON":    {"Case": "Sup"},   # dan
    "OBL":   {},                # only used in gujarati and only in conjuntion with voc as OBL+VOC (voc also only appears as obl+voc); not in UM docs, but found in UM data
    "PRIV":  {"Case": "Abe"},   # abessive / caritive / privative (UD) vs privative (UM)
    "PRP":   {"Case": "Prp"},   # purposive
    "PRT":   {"Case": "Par"},   # partitive
    "PROPR": {"Case": "Com"},   # proprietive, dan, not in UM data
    "REL":   {"Case": "Rel"},   # dan
    "SUB":   {"Case": "Sub"},   # Sublative (UM: Under)
    "TERM":  {"Case": "Ter"},   # terminative dan
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

    # INFORMATION STRUCTURE
    "FOC": {"InfStruct": "Foc"},  # Focus
    "TOP": {"InfStruct": "Top"},  # Topic

    # INTERROGATIVITY
    "DECL": {},  # dan

    # MOOD
    "ADM":   {"Mood": "Adm"},   # admirative
    "AUPRP": {"Mood": "PRP"},   # Australian Purposive, dan, not in UM data
    "COND":  {"Mood": "Cnd"},   # Conditional
    "DED":   {},                # Deductive, dan, Yakut
    "DEB":   {"Mood": "nec"},   # Debitive, dan, not in UM data
    "INFR":  {},                # not in UM docs, but found in UM data
    "IMP":   {"Mood": "Imp"},   # Imperative-Jussive
    "IND":   {"Mood": "Ind"},   # Indicative
    "INT":   {"Mood": "Int"},   # UM has its own "interrogativity" feature with only INT and DECL(arative) as values
    "INTEN": {"Mood": "Des"},   # dan
    "IRR":   {"Mood": "Irr"},   # didnt occur but is in um docs
    "OBLIG": {"Mood": "Nec"},   # both have "must" meaning
    "OPT":   {"Mood": "Opt"},   # Optative-Desiderative
    "PERM":  {"Mood": "Perm"},  # Permissive
    "POT":   {"Mood": "Pot"},   # Potential
    "PURP":  {"Mood": "Prp"},   # didnt occur but is in um docs
    "REAL":  {"Mood": "Ind"},   # Realis, dan, not in UM data
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
    "IMPRS":{"Person": 0},      # Impersonal, dan, not in UM data

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
    "POL":  {"Polite": "Form"},  # dan

    # STYLE
    "COL":   {"Style": "Coll"}, # dan; og politeness
    "LIT":   {"Style": "Lit"},  # Literary
    "FOREG": {"Style": "Form"}, # dan

    # SUBCAT
    "INTR": {"SubCat": "Intr"},  # Intransitive
    "TR":   {"SubCat": "Tran"},  # Transitive

    # TENSE
    "FUT": {"Tense": "Fut"},   # Future
    "PRS": {"Tense": "Pres"},  # Present
    "PST": {"Tense": "Past"},  # Past

    # UPOS
    "ADJ":      {"upos": "ADJ"},      # Adjective
    "ADJ.CVB":  {"upos": "ADJ"},      # korean, CVB on ADJ?
    "ADJ.MSDR": {"upos": "ADJ"},      # korean, MSDR on ADJ?
    "ADJ.PTCP": {"upos": "ADJ"},      # korean, yakut, PTPC on ADJ?
    "ADP":      {"upos": "ADP"},      # Adposition
    "ADV":      {"upos": "ADV"},      # Adverb
    "ART":      {"upos": "DET",
                 "Prontype": "Art"},  # Article, Afrikaans
    "AUX":      {"upos": "AUX"},      # Auxiliary, only Xibe has AUX
    "CONJ":     {"upos": "CONJ"},     # Conjunction, dan, strictly not UD (CCONJ vs SCONJ)
    "CLF":      {"upos": "NOUN",      # Classifier, dan, not in UM data
                 "NounType": "Class"},
    "COMP":     {"upos": "CONJ",      # Complementizer, dan, not in UM data
                 "ConjType": "Sub"},
    "DET":      {"upos": "DET",
                 "PronType": "Prn"},  # Determiner, prontype according to dan; chukchi, karelian, xibe
    "INTJ":     {"upos": "INTJ"},     # Interjection
    "N":        {"upos": "NOUN"},     # Noun
    "NUM":      {"upos": "NUM",       # Numeral
                 "NumType": "Card"},
    "PART":     {"upos": "PART"},     # Particle
    "PRO":      {"upos": "PRON",      # Pronoun, dan,not in UM docs, but found in UM data
                 "PronType": "Prn"},
    "PROPN":    {"upos": "PROPN",     # Proper Noun
                 "NounType": "Prop"},
    "V":        {"upos": "VERB"},     # AUX?
    "V.PTCP":   {"upos": "VERB",      # Participle (Verbal Adjective)
                 "VerbForm": "Part"},
    "V.CVB":    {"upos": "VERB",      # Converb (Verbal Adverb)
                 "VerbForm": "Conv"},
    "V.MSDR":   {"upos": "VERB",      # dan
                 "VerbForm": "Vnoun"},
    "V.NFIN":   {"upos": "VERB",      # not in UM docs, but found in UM data
                 "VerbForm": "NonFin"},
    "PRE":      {"upos": "ADP"},      # preposition, used in livvi, veps; not in UM docs, but found in UM data

    # (VALENCY)
    "REFL": {"Reflex": "yes"},  # dan
    "DITR": {"SubCat": "Tran"}, # Ditransitive, dan, not in UM data

    # VERBFORM
    "FIN":    {"VerbForm": "Fin"},     # Finite
    "NFIN":   {"VerbForm": "NonFin"},  # found in ud data but isnt in ud verbform docs; pr inf?
    # double check w ud
    "INF":    {"VerbForm": "Inf"},                    # not in UM docs, but found in UM data
    "PTCP":   {"upos": "VERB", "VerbForm": "Part"},   # not in UM docs, but found in UM data
    "CVB":    {"VerbForm": "Conv"},                   # dan; not in UM docs, but found in UM data
 
    # VOICE
    "ACT":   {"Voice": "Act"},    # Active
    "AGFOC": {"Voice": "AgFoc"},  # Agent Focus
    "ANTIP": {"Voice": "Antip"},  # Antipassive
    "APPL":  {},                  # None map according to dan, conflict in ind.pickle; ud data: {"Voice": "Appl"}, # valency to voice
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


blacklist = [
    "ARBEB1P",  # Chukchi
    "ARBEB1S",  # Chukchi
]

missing = {
    # These are mentioned in the UM docs but are missing from the actual UM data
    # We also dont have a UD match for any of them
    # Aktionsart
    "ACCMP":      {},  # Accomplishment
    "ACH":        {},  # Achievement
    "ACTY":       {},  # Activity
    "ATEL":       {},  # Atelic
    "DYN":        {},  # Dynamic
    "PCT":        {},  # Punctual
    "SEMEL":      {},  # Semelfactive
    "TEL":        {},  # Telic

    # Animacy
    "NHUM":       {},  # Non-human

    # Case
    "AVR":        {},  # Aversive
    "PROPR":      {},  # Proprietive

    # Local Case
    "ANTE":       {},  # Near, in front of (Pl)
    "APUD":       {},  # Next to (Pl)
    "CIRC":       {},  # Near (Pl)
    "INTER":      {},  # Among (Pl)
    "ONHR":       {},  # On (horizontal) (Pl)
    "ONVR":       {},  # On (vertical) (Pl)
    "POST":       {},  # Behind (Pl)
    "PROXM":      {},  # Proximate (Dst)
    "REM":        {},  # Distal (Dst)
    "VERS":       {},  # Versative (Asp)

    # Comparison/Degree
    "RL":         {},  # Relative (for superlatives)

    # Definiteness
    "NSPEC":      {},  # Non-Specific #?? definite spec

    # Deixis
    "ABV":        {},  # Above
    "BEL":        {},  # Below
    "EVEN":       {},  # Even
    "NOREF":      {},  # No Reference Point, Distal
    "NVIS":       {},  # Invisible
    "PHOR":       {},  # Phoric, situated in discourse
    "REF1":       {},  # First Person Reference Point
    "REF2":       {},  # Second Person Reference Point
    "VIS":        {},  # Visible

    # Evidentiality
    "ASSUM":      {},  # Assumed
    "AUD":        {},  # Auditory
    "DRCT":       {},  # Direct
    "HRSY":       {},  # Hearsay
    "INFER":      {},  # Inferred
    "NVSEN":      {},  # Non-visual sensory
    "RPRT":       {},  # Reported
    "SEN":        {},  # Sensory
    "VISU":       {},  # Visual

    # Gender/Nounclass
    "NAKH1-8":    {},  # Nakh-Daghestanian Noun Classes

    # Mood
    "AUNPRP":     {},  # Australian Non-Purposive
    "LKLY":       {},  # Likely

    # Person
    "OBV":        {},  # Obviative
    "PRX":        {},  # Proximate

    # Politeness (Speaker-Bystander)
    "AVOID":      {},  # Avoidance style
    "HIGH":       {},  # High status
    "LOW":        {},  # Low status
    "STELV":      {},  # Elevated status ("status elevated")
    "STSUPR":     {},  # Supreme status ("status supreme")

    # Politeness (Speaker-Addressee)
    "MPOL":       {},  # Medium Polite

    # Tense
    "1DAY":       {},  # Within 1 day
    "HOD":        {},  # Hodiernal (today)
    "IMMED":      {},  # Immediate
    "RCT":        {},  # Recent
    "RMT":        {},  # Remote

    # Voice
    "ACFOC":      {},  # Accompanier Focus
    "CFOC":       {},  # Conveyed Focus
}

unk_values = [
    # found in UM data but couldnt find an appropriate UD match
    # also includes any conjunction (v1+v2)
    "NPST",      # yakut tense
    "HYP",       # basque mood, (≠conditional, ≠potential)
    "(non)NOM",  # pashto negated case
    "(NON)NOM",
]

fix_typos = {
    "V.CV":    "V.CVB",   # korean
    "INST":    "INS",     # UM INST vs INS case? Only found docs on INS=instrumental but INST is used by a number of langs, together with INS; not in UM docs, but found in UM data
    "MASV":    "MASC",    # irish
    "SUBJ":    "SBJV",    # portugese
    "V.PCTP":  "V.PTCP",  # slovenian
    "PRES":    "PRS",     # basque, sanskrit, yiddish
    "PAST":    "PST",     # basque
    "ARBAB1S": "ARGAB1S", # chukchi
    "ARBAB3S": "ARGAB3S", # chukchi
}

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


def parse_ufeat_value(ufeat): #input is ONE ufeat subvalue (arg/pssd ok, but no disj/conj)
    primary_space = (shortened_vals if ufeat in shortened_vals else UM2UD_values)
    parsed = dict()
    # special case for complex strings used in argument marking/possession
    # Argument marking: ARGNO2S -> {'Number[nom]': 'Sing', 'Person[nom]': '2'}
    # Possession: PSS1S -> {'Number[psor]': 'Sing', 'Person[psor]': '1'}
    if ufeat.startswith("ARG") or ufeat.startswith("PSS"):
        parsed = parse_complex_um_value(ufeat, [shortened_vals, UM2UD_values],
                                         re.match(r"(ARG|PSS)", ufeat).group(1))
    elif ufeat in primary_space:
        # simples case_ add the corresponding UD morpho annotation
        # NOM -> {"Case": "Nom"}
        parsed = safe_dict_update(parsed, primary_space[ufeat])

    else:
        print("Warning: Unknown Unimorph value", ufeat)
    return parsed


def safe_dict_update(dict1, dict2, is_disjunction=False):
    # dict1 is main dict, add dict2
    for k, v in dict2.items():
        if k not in dict1:
            # no conflict
            dict1[k] = v
        elif dict[k]==v or v=="NonFin": # let more specific verbform override generic nonfin
            continue
        elif is_disjunction:
            # 2+ values are given as a disjunction; e.g. MASC/FEM -> Fem,Masc
            dict1[k]= ",".join(sorted(dict1[k].split(",")+[v]))
        else:
            # conflict: 2+ values want to populate the same feature -> create set
            if type(dict1.get(k))!=set:
                dict1[k] = {dict1[k]}
            dict1.get(k).add(v)
    return dict1


def map_um_value_to_ud(ufeat_raw):
    ufeat_string = str(ufeat_raw)
    if ufeat_string=="nan":  # this happens for eg eng.segmentations entries 
        return {}
    mapped_morpho = dict()
    ufeat_string = re.sub(r".?LGSPEC\d+", "", ufeat_string.upper()  # we dont handle LGSPEC
                          ).replace(":", ";")
    for ufeat in ufeat_string.split(";"): # normal split
        ufeat = ufeat.strip() # rm trailing whitespaces 
        ufeat = fix_typos.get(ufeat, ufeat)
        if ufeat in blacklist + ["", "-"] + unk_values: # skip: dont know what to map these to
            continue
        # first: check if: / or +, i.e. non-atomic value (disjunction/conjunction)
        if not re.findall(r"\+|/", ufeat):
            # normal case, atomic UM ufeat value, e.g. "NOM"
            mapped_morpho = safe_dict_update(mapped_morpho, 
                                             parse_ufeat_value(ufeat))
        else:
            # do partial parse
            if "+" in ufeat and "/" in ufeat: # highly complex
                continue # skip: we cant model conjucntions, also order of operations is unclear here
            elif "+" in ufeat: # conjunction
                if ufeat in UM2UD_values: # very few conjunctions have one atomic UD counterpart
                    mapped_morpho = safe_dict_update(mapped_morpho,
                                                     UM2UD_values[ufeat])
                else:
                    for subval in ufeat.split("+"):
                        # slight chance that all components point to the same UD value
                        # otherwise, we cannot model conjunctions
                        mapped_morpho = safe_dict_update(mapped_morpho,
                                                         parse_ufeat_value(subval))
            else: # disjunction (these, we can model in UD)
                for subval in ufeat.split("/"):
                    mapped_morpho = safe_dict_update(mapped_morpho,
                                                     parse_ufeat_value(subval),
                                                     is_disjunction=True)

    out_format = {k: (v if type(v)!=set else (tuple(v) if len(v)>1 else v.pop())) 
                  for k,v in sorted(mapped_morpho.items())}
    out_format = {"morpho": {k: v for k, v in out_format.items() if k!="upos"},
                  "upos": out_format.get("upos", None)}

    return out_format

