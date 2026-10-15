"""The UniMorph tags with no UD mapping (the UM -> UD gap lists; UD_gaps.py has the UD -> UM ones), each
keyed to its UM tagset category ("Tense", "Mood", ...): the one thing such a tag still tells a consumer.
UM2UD_mapper.py re-exports the three dicts."""

blacklist = {
    "ARBEB1P": "Argument_Marking",  # Chukchi
    "ARBEB1S": "Argument_Marking",  # Chukchi
}

missing = {
    # In the UM docs but not seen in the UM data, and with no UD match. Unverified per entry: a 2026-09
    # scan of the per-language files found 14 of the original entries in real data (ACTY, SEMEL, TEL,
    # INTER, REF1, VIS, DRCT, INFER, RPRT, LKLY, HOD, IMMED, RCT, RMT; moved to unk_values); the rest
    # were only checked against another project's tagset copy. Only used to recognise a known gap.
    "ACCMP":      "Aktionsart",  # Accomplishment
    "ACH":        "Aktionsart",  # Achievement
    "ATEL":       "Aktionsart",  # Atelic
    "DYN":        "Aktionsart",  # Dynamic
    "PCT":        "Aktionsart",  # Punctual

    "NHUM":       "Animacy",  # Non-human

    "AVR":        "Case",  # Aversive

    # Local Case
    "ANTE":       "Case",  # Near, in front of (Pl)
    "APUD":       "Case",  # Next to (Pl)
    "CIRC":       "Case",  # Near (Pl)
    "ONHR":       "Case",  # On (horizontal) (Pl)
    "ONVR":       "Case",  # On (vertical) (Pl)
    "POST":       "Case",  # Behind (Pl)
    "PROXM":      "Case",  # Proximate (Dst)
    "REM":        "Case",  # Distal (Dst)
    "VERS":       "Case",  # Versative (Asp)

    "RL":         "Degree",  # Relative (for superlatives)

    "NSPEC":      "Definite",  # Non-Specific #?? definite spec

    "ABV":        "Deixis",  # Above
    "BEL":        "Deixis",  # Below
    "EVEN":       "Deixis",  # Even
    "NOREF":      "Deixis",  # No Reference Point, Distal
    "NVIS":       "Deixis",  # Invisible
    "PHOR":       "Deixis",  # Phoric, situated in discourse
    "REF2":       "Deixis",  # Second Person Reference Point

    "ASSUM":      "Evidentiality",  # Assumed
    "AUD":        "Evidentiality",  # Auditory
    "HRSY":       "Evidentiality",  # Hearsay
    "NVSEN":      "Evidentiality",  # Non-visual sensory
    "SEN":        "Evidentiality",  # Sensory
    "VISU":       "Evidentiality",  # Visual

    "NOMS":       "Case",  # Nominative, S-only (UM docs)
    "NAKH1-8":    "NounClass",  # Nakh-Daghestanian Noun Classes -- NounClass,
                                 # not Gender, matching the real UD feature
                                 # Bantu1-23 above already use

    "AUNPRP":     "Mood",  # Australian Non-Purposive

    "OBV":        "Person",  # Obviative
    "PRX":        "Person",  # Proximate

    # Politeness -- "Polite" is UD's actual feature name (see e.g. ELEV
    # above), not UniMorph's own "Politeness" category name
    "AVOID":      "Polite",  # Avoidance style
    "HIGH":       "Polite",  # High status
    "LOW":        "Polite",  # Low status
    "STELV":      "Polite",  # Elevated status ("status elevated")
    "STSUPR":     "Polite",  # Supreme status ("status supreme")
    "MPOL":       "Polite",  # Medium Polite

    # Switch_Reference: UD has no such feature. SS/DS/SIMMA occur in the data (unk_values); the rest do not.
    "SSADV":      "Switch_Reference",  # Same Subject Adverbial
    "DSADV":      "Switch_Reference",  # Different Subject Adverbial
    "OR":         "Switch_Reference",  # Open Reference
    "SEQMA":      "Switch_Reference",  # Sequential Medial
    "LOG":        "Switch_Reference",  # Logophoric

    "1DAY":       "Tense",  # Within 1 day

    "ACFOC":      "Voice",  # Accompanier Focus
    "CFOC":       "Voice",  # Conveyed Focus
}

unk_values = {
    # In the UM data, no UD match found. The first 14 were in `missing` until a 2026-09 scan found them
    # in real data; checked against Zeman's Interset mapping, no UD equivalent.
    "INTER":  "Case",           # Local Case, "among"/interessive; aym (15520 rows), que (9600) -- Zeman
    "RCT":    "Tense",          # "recent"; zul (7254) -- Zeman, but could be RecPast (Khoekhoe?)
    "RMT":    "Tense",          # "remote"; zul (5004), frr (516), evn (6), ail (4) -- Zeman
    "HOD":    "Tense",          # "hodiernal (today)"; sna (606) -- Zeman
    "IMMED":  "Tense",          # "immediate"; hai (480) -- Zeman
    "SEMEL":  "Aktionsart",     # "semelfactive"; evn (282) -- Zeman
    "TEL":    "Aktionsart",     # "telic"; ail (225) -- Zeman
    "DRCT":   "Evidentiality",  # "direct"; hai (320) -- Zeman, but could be like Fh?
    "INFER":  "Evidentiality",  # "inferred"; kca (56) -- Zeman
    "ACTY":   "Aktionsart",     # "activity"; itl (39) -- Zeman
    "RPRT":   "Evidentiality",  # "reported"; ail (6) -- Zeman
    "LKLY":   "Mood",           # "likely"; mag (4) -- Zeman
    "REF1":   "Deixis",         # "first person reference point"; mag (1) -- Zeman, but could be DeixisRef:1? cf. Pomak, Wolof
    "VIS":    "Deixis",         # "visible"; ail (1) -- Zeman

    # Switch_Reference: UD has no such feature (the other schema members are in `missing`)
    "SS":     "Switch_Reference",  # pei (1680) -- Zeman
    "DS":     "Switch_Reference",  # ail (126) -- Zeman
    "SIMMA":  "Switch_Reference",  # ail (183) -- Zeman

    # Mapped to {} in UM2UD_values, listed here so they get a category
    "APPRX":  "Case",             # Zeman; ail, krl, lud, olo, vep
    "STAT":   "Aktionsart",       # stative; ail, ckt, evn, xty
    "DECL":   "Interrogativity",  # Zeman; kor, mag, tur
    "DED":    "Mood",             # Deductive, Zeman, Yakut (sah)
    "SIM":    "Mood",             # Simulative; ail

    # Found by the 2026-10 parse of all UniMorph languages. No README explains them, so only the
    # argument markers (a clear parallel of ARG*) get a category; the rest are "UNK".
    # Argument markers written without the ARG prefix (NO1S ~ ARGNO1S, AC = accusative, DA = dative
    # argument); ame, cni, cre, kod, aym, ail. Could be mapped through the ARG machinery.
    "AC1": "UNK", "AC1PE": "UNK", "AC1PI": "UNK", "AC1S": "UNK",
    "AC2": "UNK", "AC2P": "UNK", "AC2S": "UNK", "AC3": "UNK",
    "AC3P": "UNK", "AC3S": "UNK", "DA1PE": "UNK", "DA1PI": "UNK",
    "DA1S": "UNK", "DA2P": "UNK", "DA2S": "UNK", "DA3P": "UNK",
    "DA3S": "UNK", "NO1": "UNK", "NO1P": "UNK", "NO1PE": "UNK",
    "NO1PI": "UNK", "NO1S": "UNK", "NO2": "UNK", "NO2P": "UNK",
    "NO2S": "UNK", "NO3": "UNK", "NO3F": "UNK", "NO3M": "UNK",
    "NO3P": "UNK", "NO3PA": "UNK", "NO3S": "UNK", "NO3SA": "UNK",
    "NO3SI": "UNK",
    "NFUT":   "UNK",     # mwf; name suggests near future, not confirmed
    "PC":     "UNK",     # mwf, "1;PC"; position suggests number (paucal?), not confirmed
    "COMP":   "UNK",     # kca only (14 rows, 18 more in its "Manual check needed"): never the upos, always after it ("ADJ;COMP", "ADV;COMP", "N;DAT;COMP;SG"), on forms ending in -šək; no README. Likely the comparative (CMPR, Degree=Cmp) -- not the complementizer upos of Zeman's Interset mapping (formerly mapped as CONJ, ConjType=Sub), which no language uses -- not confirmed
    "NALN":   "UNK",     # slp, "N;NALN+PSS3S"; cf. ALN (alienable), not confirmed
    "INFN":   "UNK",     # mag, "V;3;PFV;INFN"; possibly a typo of INFM, not corrected
    "CF":     "UNK",     # aym (40k rows), ail
    "FORM2":  "UNK",     # aym
    "DEO":    "UNK",     # ail
    "AGT":    "UNK",     # que, "V;NFIN;AGT"
    "BEADJ":  "UNK",     # que, "ADJ;BEADJ;PL"
    "GEADJ":  "UNK",     # que
    "CAUSV":  "UNK",     # que, "N;CAUSV;PL"
    "DISTR":  "UNK",     # que
    "EXCLV":  "UNK",     # que
    "REDUP":  "UNK",     # gup, reduplication?
    "TAXIS":  "UNK",     # kca, "V;PST;ARGNO3;ARGNOS;TAXIS"
    "ADB":    "UNK",     # ket, one row
    "_":      "UNK",     # ket, empty placeholder
    "FROM":   "UNK",     # bra, one row
    "FUTS":   "UNK",     # bra, one row ("PL,FUTS")
    "PFA":    "UNK",     # bra, "AUX;PFA;MASC;SG;PRS"
    "SL":     "UNK",     # bra, "N;SL"
}
