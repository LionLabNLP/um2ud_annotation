# UM docs: https://unimorph.github.io/doc/unimorph-schema.pdf 
# (draft of june 2, 2016; retrieved july 22 2026)

UM_feature2values = {
  "Aktionsart": [
    "STAT",   # Stative
    "DYN",    # Dynamic
    "TEL",    # Telic
    "ATEL",   # Atelic
    "PCT",    # Punctual
    "DUR",    # Durative
    "ACH",    # Achievement
    "ACCMP",  # Accomplishment
    "SEMEL",  # Semelfactive
    "ACTY"    # Activity
  ],
  "Animacy": [
    "ANIM",  # Animate
    "INAN",  # Inanimate
    "HUM",   # Human
    "NHUM"   # Non-human
  ],
  "Aspect": [
    "IPFV",   # Imperfective
    "PFV",    # Perfective
    "PRF",    # Perfect
    "PROG",   # Progressive
    "PROSP",  # Prospective
    "ITER",   # Iterative
    "HAB"     # Habitual
  ],
  "Core Case": [
    "NOM",    # Nominative
    "ACC",    # Accusative
    "ERG",    # Ergative
    "ABS",    # Absolutive
    "NOMS"    # Nominative, S-only
  ],
  "Non Core, Non Local Case": [
    "DAT",    # Dative: marks indirect object — to (indirect object)
    "BEN",    # Benefactive: marks a beneficiary of an action — (a gift, e.g.) to, for (s.o.)
    "PRP",    # Purposive: marks purpose of or reason for an action — for (profit, e.g.)
    "GEN",    # Genitive: marks possessor — of s.o., s.o.'s
    "REL",    # Relative: marks possessor and A role — of s.o., s.o.'s
    "PRT",    # Partitive: marks a patient as partially affected — some of
    "INS",    # Instrumental: marks means by which an action occurred — by (means of) sth, with sth, using sth
    "COM",    # Comitative: marks accompaniment — (together) with
    "VOC",    # Vocative: indicates direct form of address — "s.o.!"
    "COMPV",  # Comparative: marks standard of comparison — than sth, s.o.
    "EQTV",   # Equative: marks equality or similarity — (as much) as s.o./sth, like s.o./sth
    "PRIV",   # Privative: indicates lack of something — without, lacking sth
    "PROPR",  # Proprietive: indicates quality of possessing something — having sth
    "AVR",    # Aversive: indicates what is to be feared, avoided — (afraid) of (ghosts, e.g.), (dying) from (poison, e.g.)
    "FRML",   # Formal: indicates that sth is function as sth else — as sth, in the capacity of sth
    "TRANS",  # Translative: indicates that an entity is the result of a transformation
    "BYWAY"   # Essive-modal: indicates that a motion event occurs 'by way of' a location
  ],
  "Local Case": [
    "INTER",  # Among (Pl)
    "AT",     # At (Pl)
    "POST",   # Behind (Pl)
    "IN",     # In (Pl)
    "CIRC",   # Near (Pl)
    "ANTE",   # Near, in front of (Pl)
    "APUD",   # Next to (Pl)
    "ON",     # On (Pl)
    "ONHR",   # On (horizontal) (Pl)
    "ONVR",   # On (vertical) (Pl)
    "SUB",    # Under (Pl)
    "REM",    # Distal (Dst)
    "PROXM",  # Proximate (Dst)
    "ESS",    # Essive (Mot)
    "ALL",    # Allative (Mot)
    "ABL",    # Ablative (Mot)
    "APPRX",  # Approximative (Asp)
    "TERM",   # Terminative (Asp)
    "PROL",   # Prolative/translative (Asp)
    "VERS"    # Versative (Asp)
  ],
  "Degree": [
    "CMPR",  # Comparative
    "SPRL",  # Superlative
    "AB",    # Absolute (for superlatives)
    "RL",    # Relative (for superlatives)
    "EQT"    # Equative
  ],
  "Definite": [
    "DEF",    # Definite
    "INDF",   # Indefinite
    "SPEC",   # Specific
    "NSPEC"   # Non-Specific
  ],
  "Deixis": [
    "PROX",   # Proximate
    "MED",    # Medial
    "REMT",   # Remote
    "REF1",   # First Person Reference Point
    "REF2",   # Second Person Reference Point
    "NOREF",  # No Reference Point, Distal
    "PHOR",   # Phoric, situated in discourse
    "VIS",    # Visible
    "NVIS",   # Invisible
    "ABV",    # Above
    "EVEN",   # Even
    "BEL"     # Below
  ],
  "Evidentiality": [
    "FH",     # Firsthand
    "DRCT",   # Direct
    "SEN",    # Sensory
    "VISU",   # Visual
    "NVSEN",  # Non-visual sensory
    "AUD",    # Auditory
    "NFH",    # Non-firsthand
    "QUOT",   # Quotative
    "RPRT",   # Reported
    "HRSY",   # Hearsay
    "INFER",  # Inferred
    "ASSUM"   # Assumed
  ],
  "VerbForm": [ # "Finiteness"
    "FIN",   # Finite
    "NFIN"   # Nonfinite
  ],
  "Gender": [
    "MASC",       # Masculine
    "FEM",        # Feminine
    "NEUT",       # Neuter
  ],
  "NounType": ([f"BANTU{i}" for i in range(1,24)] # Bantu Noun Classes
    +[f"NAKH{i}" for i in range(1,9)]     # Nakh-Daghestanian Noun Classes
  )
  ,
  "InfStruct": [
    "TOP",  # Topic
    "FOC"   # Focus
  ],
  "Interrogativity": [
    "DECL",  # Declarative
    "INT"    # Interrogative
  ],
  "Mood": [
    "IND",     # Indicative
    "SBJV",    # Subjunctive
    "REAL",    # Realis
    "IRR",     # Irrealis
    "AUPRP",   # Australian Purposive
    "AUNPRP",  # Australian Non-Purposive
    "IMP",     # Imperative-Jussive
    "COND",    # Conditional
    "PURP",    # General Purposive ('in order to')
    "INTEN",   # Intentive
    "POT",     # Potential
    "LKLY",    # Likely
    "ADM",     # Admirative
    "OBLIG",   # Obligative
    "DEB",     # Debitive
    "PERM",    # Permissive
    "DED",     # Deductive
    "SIM",     # Simulative
    "OPT"      # Optative-Desiderative
  ],
  "Number": [
    "SG",     # Singular
    "PL",     # Plural
    "GRPL",   # Greater plural
    "DU",     # Dual
    "TRI",    # Trial
    "PAUC",   # Paucal
    "GPAUC",  # Greater paucal
    "INVN"    # Inverse
  ],
  "upos": [
    "N",       # Noun
    "PROPN",   # Proper Name
    "ADJ",     # Adjective
    "PRO",     # Pronoun
    "CLF",     # Classifier
    "ART",     # Article
    "DET",     # Determiner
    "V",       # Verb
    "ADV",     # Adverb
    "AUX",     # Auxiliary
    "V.PTCP",  # Participle (Verbal Adjective)
    "V.MSDR",  # Masdar (Verbal Noun)
    "V.CVB",   # Converb (Verbal Adverb)
    "ADP",     # Adposition
    "COMP",    # Complementizer
    "CONJ",    # Conjunction
    "NUM",     # Numeral
    "PART",    # Particle
    "INTJ"     # Interjection
  ],
  "Person": [
    "0",     # Zero person
    "1",     # First person
    "2",     # Second person
    "3",     # Third person
    "4",     # Fourth person
    "INCL",  # Inclusive
    "EXCL",  # Exclusive
    "PRX",   # Proximate
    "OBV"    # Obviative
  ],
  "Polarity": [
    "POS",  # Positive
    "NEG"   # Negative
  ],
  "Politeness (Speaker-Referent)": [
    "INFM",  # Informal, speaker-referent
    "FORM",  # Formal, speaker-referent
    "ELEV",  # Referent Elevating, speaker-referent
    "HUMB"   # Speaker Humbling, speaker-referent
  ],
  "Politeness (Speaker-Addressee)": [
    "POL",   # Polite, speaker-addressee
    "MPOL"   # Medium Polite, speaker-addressee
  ],
  "Politeness (Speaker-Bystander)": [
    "AVOID",   # Avoidance style, speaker-bystander
    "LOW",     # Low status, speaker-bystander
    "HIGH",    # High status, speaker-bystander
    "STELV",   # Elevated status ("status elevated"), speaker-bystander
    "STSUPR"   # Supreme status ("status supreme"), speaker-bystander
  ],
  "Politeness (Speaker-Setting)": [
    "LIT",     # Literary, speaker-setting
    "FOREG",   # Formal register, speaker-setting
    "COL"      # Colloquial, speaker-setting
  ],
  "Tense": [
    "PRS",     # Present
    "PST",     # Past
    "FUT",     # Future
    "IMMED",   # Immediate
    "HOD",     # Hodiernal (today)
    "1DAY",    # Within 1 day
    "RCT",     # Recent
    "RMT"      # Remote
  ],
  "Valency": [
    "IMPRS",  # Impersonal
    "INTR",   # Intransitive
    "TR",     # Transitive
    "DITR",   # Ditransitive
    "REFL",   # Reflexive
    "RECP",   # Reciprocal
    "CAUS",   # Causative
    "APPL"    # Applicative
  ],
  "Voice": [
    "ACT",     # Active
    "MID",     # Middle
    "PASS",    # Passive
    "ANTIP",   # Antipassive
    "DIR",     # Direct
    "INV",     # Inverse
    "AGFOC",   # Agent Focus
    "PFOC",    # Patient Focus
    "LFOC",    # Location Focus
    "BFOC",    # Beneficiary Focus
    "ACFOC",   # Accompanier Focus
    "IFOC",    # Instrument Focus
    "CFOC"     # Conveyed Focus
  ]
}

# not in UM docs, found in UM data
UM_feature2values["Aspect"] += [
    "FREQ", # Lithuanian
]
UM_feature2values["Non Core, Non Local Case"] += [
    "INST", # Czech, Hungarian, Kazakh, Latvian, Lithuanian
    "OBL",  # Japanese, Turkish, Yakut
    "IO",   # Basque, indirect object arg marking case
]
UM_feature2values["Local Case"] += [
    "IN+ESS", # Estonian, Finnish, Hungarian, Karelian, Livvi, Veps
    "LOC",    # Locative; Armenian, Assamese, Azerbaijani, Bengali, Gujarati, Kazakh, Korean, Latin, Latvian, Lithuanian, Sanskrit, Tatar, Turkish, Uzbek
]
UM_feature2values["Degree"] += [
    "SUP",   # Afrikaans
]
UM_feature2values["Gender"] += [
    "MASV",  # Irish
]
UM_feature2values["Mood"] += [
    "INFR",  # Turkish
    "SUBJ",  # Portugese, SBJV mistag
]
UM_feature2values["NounType"] += [
    "STRONG", # Irish
    "WEAK",   # Irish
]
UM_feature2values["Person"] += [
    "AUTO", # Irish, autonomous verb
]
UM_feature2values["upos"] += [
    "PRON", # Irish, pronoun PRO mistag
    "PRE",  # preposition?
]
UM_feature2values["VerbForm"] += [
    "INF",  # infinitive?
    "PTCP", # participle?
    "PCTP", # V.PCTP mistag -> V:PTCP, slovenian
    "NFIN", # nonfinite, V.NFIN
    "CVB",  # converbal
    "CV",   # CVB mistag, korean
]
UM_feature2values["Tense"] += [
    "PRES",  # PRS mistag, basque, sanskrit, yiddish
    "PAST",  # PST mistag, basque
]
# used for argumentmarking (ARGXX) and possession marking (PSSX(X))
UM_feature2values["Supplements"] = [
    "AB",   # absolutive
    "AC",   # accusative
    "BE",   # benefactive
    "DA",   # dative
    "ER",   # ergative
    "NO",   # nominative
    "F",    # Feminine
    "M",    # Masculine
    "P",    # Plural, arg marking
    "PL",   # Plural, arg marking
    "SG",   # Singular, arg marking
    "S",    # Singular, arg marking
    "INFM", # basque
    "D",    # Construct state; UM Chuckchi, Hebrew
]

UM_feature2values["Case"] = (UM_feature2values["Core Case"] 
                             + UM_feature2values["Non Core, Non Local Case"] 
                             + UM_feature2values["Local Case"])
UM_feature2values["Polite"] = (UM_feature2values["Politeness (Speaker-Addressee)"] 
                               + UM_feature2values["Politeness (Speaker-Bystander)"]
                               +UM_feature2values["Politeness (Speaker-Referent)"]
                               +UM_feature2values["Politeness (Speaker-Setting)"])
