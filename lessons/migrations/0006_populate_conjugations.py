from django.db import migrations

# Conjugation tables keyed by phrase PK.
# Structure: list of {"title": str, "forms": [{"label": str, "form": str}]}

# fmt: off
CONJUGATIONS = {

    # -----------------------------------------------------------------------
    # SPANISH (pks 14–19)
    # -----------------------------------------------------------------------
    14: [  # ser / estar
        {"title": "ser (permanent)", "forms": [
            {"label": "yo",          "form": "soy"},
            {"label": "tú",          "form": "eres"},
            {"label": "él/ella",     "form": "es"},
            {"label": "nosotros",    "form": "somos"},
            {"label": "vosotros",    "form": "sois"},
            {"label": "ellos",       "form": "son"},
        ]},
        {"title": "estar (temporary/location)", "forms": [
            {"label": "yo",          "form": "estoy"},
            {"label": "tú",          "form": "estás"},
            {"label": "él/ella",     "form": "está"},
            {"label": "nosotros",    "form": "estamos"},
            {"label": "vosotros",    "form": "estáis"},
            {"label": "ellos",       "form": "están"},
        ]},
    ],
    15: [  # tener
        {"title": "tener — present tense", "forms": [
            {"label": "yo",          "form": "tengo"},
            {"label": "tú",          "form": "tienes"},
            {"label": "él/ella",     "form": "tiene"},
            {"label": "nosotros",    "form": "tenemos"},
            {"label": "vosotros",    "form": "tenéis"},
            {"label": "ellos",       "form": "tienen"},
        ]},
    ],
    16: [  # querer
        {"title": "querer — present tense", "forms": [
            {"label": "yo",          "form": "quiero"},
            {"label": "tú",          "form": "quieres"},
            {"label": "él/ella",     "form": "quiere"},
            {"label": "nosotros",    "form": "queremos"},
            {"label": "vosotros",    "form": "queréis"},
            {"label": "ellos",       "form": "quieren"},
        ]},
    ],
    17: [  # gustar — reverse subject/object
        {"title": "gustar — present tense", "forms": [
            {"label": "me (I like)",        "form": "me gusta / me gustan"},
            {"label": "te (you like)",      "form": "te gusta / te gustan"},
            {"label": "le (he/she likes)",  "form": "le gusta / le gustan"},
            {"label": "nos (we like)",      "form": "nos gusta / nos gustan"},
            {"label": "os (you pl. like)",  "form": "os gusta / os gustan"},
            {"label": "les (they like)",    "form": "les gusta / les gustan"},
        ]},
    ],
    18: [  # saber / conocer
        {"title": "saber (facts/skills)", "forms": [
            {"label": "yo",          "form": "sé"},
            {"label": "tú",          "form": "sabes"},
            {"label": "él/ella",     "form": "sabe"},
            {"label": "nosotros",    "form": "sabemos"},
            {"label": "vosotros",    "form": "sabéis"},
            {"label": "ellos",       "form": "saben"},
        ]},
        {"title": "conocer (people/places)", "forms": [
            {"label": "yo",          "form": "conozco"},
            {"label": "tú",          "form": "conoces"},
            {"label": "él/ella",     "form": "conoce"},
            {"label": "nosotros",    "form": "conocemos"},
            {"label": "vosotros",    "form": "conocéis"},
            {"label": "ellos",       "form": "conocen"},
        ]},
    ],
    19: [  # ir (irregular)
        {"title": "ir — present tense", "forms": [
            {"label": "yo",          "form": "voy"},
            {"label": "tú",          "form": "vas"},
            {"label": "él/ella",     "form": "va"},
            {"label": "nosotros",    "form": "vamos"},
            {"label": "vosotros",    "form": "vais"},
            {"label": "ellos",       "form": "van"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # FRENCH (pks 71–76)
    # -----------------------------------------------------------------------
    71: [  # être
        {"title": "être — présent", "forms": [
            {"label": "je",          "form": "suis"},
            {"label": "tu",          "form": "es"},
            {"label": "il/elle",     "form": "est"},
            {"label": "nous",        "form": "sommes"},
            {"label": "vous",        "form": "êtes"},
            {"label": "ils/elles",   "form": "sont"},
        ]},
    ],
    72: [  # avoir
        {"title": "avoir — présent", "forms": [
            {"label": "je",          "form": "ai"},
            {"label": "tu",          "form": "as"},
            {"label": "il/elle",     "form": "a"},
            {"label": "nous",        "form": "avons"},
            {"label": "vous",        "form": "avez"},
            {"label": "ils/elles",   "form": "ont"},
        ]},
    ],
    73: [  # vouloir
        {"title": "vouloir — présent", "forms": [
            {"label": "je",          "form": "veux"},
            {"label": "tu",          "form": "veux"},
            {"label": "il/elle",     "form": "veut"},
            {"label": "nous",        "form": "voulons"},
            {"label": "vous",        "form": "voulez"},
            {"label": "ils/elles",   "form": "veulent"},
        ]},
    ],
    74: [  # aimer
        {"title": "aimer — présent", "forms": [
            {"label": "je",          "form": "aime"},
            {"label": "tu",          "form": "aimes"},
            {"label": "il/elle",     "form": "aime"},
            {"label": "nous",        "form": "aimons"},
            {"label": "vous",        "form": "aimez"},
            {"label": "ils/elles",   "form": "aiment"},
        ]},
    ],
    75: [  # savoir / connaître
        {"title": "savoir (facts/skills)", "forms": [
            {"label": "je",          "form": "sais"},
            {"label": "tu",          "form": "sais"},
            {"label": "il/elle",     "form": "sait"},
            {"label": "nous",        "form": "savons"},
            {"label": "vous",        "form": "savez"},
            {"label": "ils/elles",   "form": "savent"},
        ]},
        {"title": "connaître (people/places)", "forms": [
            {"label": "je",          "form": "connais"},
            {"label": "tu",          "form": "connais"},
            {"label": "il/elle",     "form": "connaît"},
            {"label": "nous",        "form": "connaissons"},
            {"label": "vous",        "form": "connaissez"},
            {"label": "ils/elles",   "form": "connaissent"},
        ]},
    ],
    76: [  # aller (irregular)
        {"title": "aller — présent", "forms": [
            {"label": "je",          "form": "vais"},
            {"label": "tu",          "form": "vas"},
            {"label": "il/elle",     "form": "va"},
            {"label": "nous",        "form": "allons"},
            {"label": "vous",        "form": "allez"},
            {"label": "ils/elles",   "form": "vont"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # GERMAN (pks 100–105)
    # -----------------------------------------------------------------------
    100: [  # sein
        {"title": "sein — Präsens", "forms": [
            {"label": "ich",         "form": "bin"},
            {"label": "du",          "form": "bist"},
            {"label": "er/sie/es",   "form": "ist"},
            {"label": "wir",         "form": "sind"},
            {"label": "ihr",         "form": "seid"},
            {"label": "sie/Sie",     "form": "sind"},
        ]},
    ],
    101: [  # haben
        {"title": "haben — Präsens", "forms": [
            {"label": "ich",         "form": "habe"},
            {"label": "du",          "form": "hast"},
            {"label": "er/sie/es",   "form": "hat"},
            {"label": "wir",         "form": "haben"},
            {"label": "ihr",         "form": "habt"},
            {"label": "sie/Sie",     "form": "haben"},
        ]},
    ],
    102: [  # wollen / möchten
        {"title": "wollen (strong desire)", "forms": [
            {"label": "ich",         "form": "will"},
            {"label": "du",          "form": "willst"},
            {"label": "er/sie/es",   "form": "will"},
            {"label": "wir",         "form": "wollen"},
            {"label": "ihr",         "form": "wollt"},
            {"label": "sie/Sie",     "form": "wollen"},
        ]},
        {"title": "möchten (polite — would like)", "forms": [
            {"label": "ich",         "form": "möchte"},
            {"label": "du",          "form": "möchtest"},
            {"label": "er/sie/es",   "form": "möchte"},
            {"label": "wir",         "form": "möchten"},
            {"label": "ihr",         "form": "möchtet"},
            {"label": "sie/Sie",     "form": "möchten"},
        ]},
    ],
    103: [  # mögen
        {"title": "mögen — Präsens", "forms": [
            {"label": "ich",         "form": "mag"},
            {"label": "du",          "form": "magst"},
            {"label": "er/sie/es",   "form": "mag"},
            {"label": "wir",         "form": "mögen"},
            {"label": "ihr",         "form": "mögt"},
            {"label": "sie/Sie",     "form": "mögen"},
        ]},
    ],
    104: [  # wissen / kennen
        {"title": "wissen (facts)", "forms": [
            {"label": "ich",         "form": "weiß"},
            {"label": "du",          "form": "weißt"},
            {"label": "er/sie/es",   "form": "weiß"},
            {"label": "wir",         "form": "wissen"},
            {"label": "ihr",         "form": "wisst"},
            {"label": "sie/Sie",     "form": "wissen"},
        ]},
        {"title": "kennen (people/places)", "forms": [
            {"label": "ich",         "form": "kenne"},
            {"label": "du",          "form": "kennst"},
            {"label": "er/sie/es",   "form": "kennt"},
            {"label": "wir",         "form": "kennen"},
            {"label": "ihr",         "form": "kennt"},
            {"label": "sie/Sie",     "form": "kennen"},
        ]},
    ],
    105: [  # gehen / fahren
        {"title": "gehen (on foot)", "forms": [
            {"label": "ich",         "form": "gehe"},
            {"label": "du",          "form": "gehst"},
            {"label": "er/sie/es",   "form": "geht"},
            {"label": "wir",         "form": "gehen"},
            {"label": "ihr",         "form": "geht"},
            {"label": "sie/Sie",     "form": "gehen"},
        ]},
        {"title": "fahren (by vehicle)", "forms": [
            {"label": "ich",         "form": "fahre"},
            {"label": "du",          "form": "fährst"},
            {"label": "er/sie/es",   "form": "fährt"},
            {"label": "wir",         "form": "fahren"},
            {"label": "ihr",         "form": "fahrt"},
            {"label": "sie/Sie",     "form": "fahren"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # ITALIAN (pks 129–134)
    # -----------------------------------------------------------------------
    129: [  # essere
        {"title": "essere — presente", "forms": [
            {"label": "io",          "form": "sono"},
            {"label": "tu",          "form": "sei"},
            {"label": "lui/lei",     "form": "è"},
            {"label": "noi",         "form": "siamo"},
            {"label": "voi",         "form": "siete"},
            {"label": "loro",        "form": "sono"},
        ]},
    ],
    130: [  # avere
        {"title": "avere — presente", "forms": [
            {"label": "io",          "form": "ho"},
            {"label": "tu",          "form": "hai"},
            {"label": "lui/lei",     "form": "ha"},
            {"label": "noi",         "form": "abbiamo"},
            {"label": "voi",         "form": "avete"},
            {"label": "loro",        "form": "hanno"},
        ]},
    ],
    131: [  # volere
        {"title": "volere — presente", "forms": [
            {"label": "io",          "form": "voglio"},
            {"label": "tu",          "form": "vuoi"},
            {"label": "lui/lei",     "form": "vuole"},
            {"label": "noi",         "form": "vogliamo"},
            {"label": "voi",         "form": "volete"},
            {"label": "loro",        "form": "vogliono"},
        ]},
    ],
    132: [  # piacere — reverse subject/object
        {"title": "piacere — presente", "forms": [
            {"label": "mi (I like)",        "form": "mi piace / mi piacciono"},
            {"label": "ti (you like)",      "form": "ti piace / ti piacciono"},
            {"label": "gli/le (he/she)",    "form": "gli piace / le piacciono"},
            {"label": "ci (we like)",       "form": "ci piace / ci piacciono"},
            {"label": "vi (you pl. like)",  "form": "vi piace / vi piacciono"},
            {"label": "loro (they like)",   "form": "piace loro / piacciono loro"},
        ]},
    ],
    133: [  # sapere / conoscere
        {"title": "sapere (facts/skills)", "forms": [
            {"label": "io",          "form": "so"},
            {"label": "tu",          "form": "sai"},
            {"label": "lui/lei",     "form": "sa"},
            {"label": "noi",         "form": "sappiamo"},
            {"label": "voi",         "form": "sapete"},
            {"label": "loro",        "form": "sanno"},
        ]},
        {"title": "conoscere (people/places)", "forms": [
            {"label": "io",          "form": "conosco"},
            {"label": "tu",          "form": "conosci"},
            {"label": "lui/lei",     "form": "conosce"},
            {"label": "noi",         "form": "conosciamo"},
            {"label": "voi",         "form": "conoscete"},
            {"label": "loro",        "form": "conoscono"},
        ]},
    ],
    134: [  # andare (irregular)
        {"title": "andare — presente", "forms": [
            {"label": "io",          "form": "vado"},
            {"label": "tu",          "form": "vai"},
            {"label": "lui/lei",     "form": "va"},
            {"label": "noi",         "form": "andiamo"},
            {"label": "voi",         "form": "andate"},
            {"label": "loro",        "form": "vanno"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # PORTUGUESE (pks 158–163)
    # -----------------------------------------------------------------------
    158: [  # ser / estar
        {"title": "ser (permanent)", "forms": [
            {"label": "eu",          "form": "sou"},
            {"label": "tu",          "form": "és"},
            {"label": "ele/ela",     "form": "é"},
            {"label": "nós",         "form": "somos"},
            {"label": "vós",         "form": "sois"},
            {"label": "eles",        "form": "são"},
        ]},
        {"title": "estar (temporary/location)", "forms": [
            {"label": "eu",          "form": "estou"},
            {"label": "tu",          "form": "estás"},
            {"label": "ele/ela",     "form": "está"},
            {"label": "nós",         "form": "estamos"},
            {"label": "vós",         "form": "estais"},
            {"label": "eles",        "form": "estão"},
        ]},
    ],
    159: [  # ter
        {"title": "ter — presente", "forms": [
            {"label": "eu",          "form": "tenho"},
            {"label": "tu",          "form": "tens"},
            {"label": "ele/ela",     "form": "tem"},
            {"label": "nós",         "form": "temos"},
            {"label": "vós",         "form": "tendes"},
            {"label": "eles",        "form": "têm"},
        ]},
    ],
    160: [  # querer
        {"title": "querer — presente", "forms": [
            {"label": "eu",          "form": "quero"},
            {"label": "tu",          "form": "queres"},
            {"label": "ele/ela",     "form": "quer"},
            {"label": "nós",         "form": "queremos"},
            {"label": "vós",         "form": "quereis"},
            {"label": "eles",        "form": "querem"},
        ]},
    ],
    161: [  # gostar (+ de)
        {"title": "gostar (+ de) — presente", "forms": [
            {"label": "eu",          "form": "gosto"},
            {"label": "tu",          "form": "gostas"},
            {"label": "ele/ela",     "form": "gosta"},
            {"label": "nós",         "form": "gostamos"},
            {"label": "vós",         "form": "gostais"},
            {"label": "eles",        "form": "gostam"},
        ]},
    ],
    162: [  # saber / conhecer
        {"title": "saber (facts/skills)", "forms": [
            {"label": "eu",          "form": "sei"},
            {"label": "tu",          "form": "sabes"},
            {"label": "ele/ela",     "form": "sabe"},
            {"label": "nós",         "form": "sabemos"},
            {"label": "vós",         "form": "sabeis"},
            {"label": "eles",        "form": "sabem"},
        ]},
        {"title": "conhecer (people/places)", "forms": [
            {"label": "eu",          "form": "conheço"},
            {"label": "tu",          "form": "conheces"},
            {"label": "ele/ela",     "form": "conhece"},
            {"label": "nós",         "form": "conhecemos"},
            {"label": "vós",         "form": "conheceis"},
            {"label": "eles",        "form": "conhecem"},
        ]},
    ],
    163: [  # ir (irregular)
        {"title": "ir — presente", "forms": [
            {"label": "eu",          "form": "vou"},
            {"label": "tu",          "form": "vais"},
            {"label": "ele/ela",     "form": "vai"},
            {"label": "nós",         "form": "vamos"},
            {"label": "vós",         "form": "ides"},
            {"label": "eles",        "form": "vão"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # IRISH (pks 43–47)
    # -----------------------------------------------------------------------
    43: [  # tá / bí
        {"title": "tá — present (at this moment)", "forms": [
            {"label": "mé",          "form": "táim"},
            {"label": "tú",          "form": "tá tú"},
            {"label": "sé/sí",       "form": "tá sé / tá sí"},
            {"label": "muid",        "form": "táimid"},
            {"label": "sibh",        "form": "tá sibh"},
            {"label": "siad",        "form": "tá siad"},
        ]},
        {"title": "bíonn — habitual present", "forms": [
            {"label": "mé",          "form": "bím"},
            {"label": "tú",          "form": "bíonn tú"},
            {"label": "sé/sí",       "form": "bíonn sé / bíonn sí"},
            {"label": "muid",        "form": "bímid"},
            {"label": "sibh",        "form": "bíonn sibh"},
            {"label": "siad",        "form": "bíonn siad"},
        ]},
    ],
    44: [  # teastaíonn ... uaim
        {"title": "teastaíonn … ó — to want/need", "forms": [
            {"label": "mé (I)",       "form": "uaim"},
            {"label": "tú (you)",     "form": "uait"},
            {"label": "sé (he)",      "form": "uaidh"},
            {"label": "sí (she)",     "form": "uaithi"},
            {"label": "muid (we)",    "form": "uainn"},
            {"label": "sibh (you pl.)","form": "uaibh"},
            {"label": "siad (they)",  "form": "uathu"},
        ]},
    ],
    45: [  # is maith liom
        {"title": "is maith le — to like", "forms": [
            {"label": "mé (I)",       "form": "is maith liom"},
            {"label": "tú (you)",     "form": "is maith leat"},
            {"label": "sé (he)",      "form": "is maith leis"},
            {"label": "sí (she)",     "form": "is maith léi"},
            {"label": "muid (we)",    "form": "is maith linn"},
            {"label": "sibh (you pl.)","form": "is maith libh"},
            {"label": "siad (they)",  "form": "is maith leo"},
        ]},
    ],
    46: [  # tá a fhios agam
        {"title": "tá a fhios ag — to know a fact", "forms": [
            {"label": "mé (I)",       "form": "tá a fhios agam"},
            {"label": "tú (you)",     "form": "tá a fhios agat"},
            {"label": "sé (he)",      "form": "tá a fhios aige"},
            {"label": "sí (she)",     "form": "tá a fhios aici"},
            {"label": "muid (we)",    "form": "tá a fhios againn"},
            {"label": "sibh (you pl.)","form": "tá a fhios agaibh"},
            {"label": "siad (they)",  "form": "tá a fhios acu"},
        ]},
    ],
    47: [  # téim
        {"title": "téigh — to go", "forms": [
            {"label": "mé",          "form": "téim"},
            {"label": "tú",          "form": "téann tú"},
            {"label": "sé/sí",       "form": "téann sé / téann sí"},
            {"label": "muid",        "form": "téimid"},
            {"label": "sibh",        "form": "téann sibh"},
            {"label": "siad",        "form": "téann siad"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # JAPANESE (pks 187–192) — polite/casual/negative forms, not by person
    # -----------------------------------------------------------------------
    187: [  # です / います / あります
        {"title": "です (nouns/na-adjectives)", "forms": [
            {"label": "polite",          "form": "です"},
            {"label": "polite negative", "form": "ではありません"},
            {"label": "past polite",     "form": "でした"},
            {"label": "casual",          "form": "だ"},
        ]},
        {"title": "います (animate) / あります (inanimate)", "forms": [
            {"label": "polite",          "form": "います / あります"},
            {"label": "polite negative", "form": "いません / ありません"},
            {"label": "past polite",     "form": "いました / ありました"},
            {"label": "casual",          "form": "いる / ある"},
        ]},
    ],
    188: [  # 持っています
        {"title": "持つ (to hold/have)", "forms": [
            {"label": "polite",          "form": "持っています"},
            {"label": "polite negative", "form": "持っていません"},
            {"label": "past polite",     "form": "持っていました"},
            {"label": "casual",          "form": "持ってる"},
        ]},
    ],
    189: [  # 〜たいです
        {"title": "〜たい (want to do)", "forms": [
            {"label": "polite",          "form": "〜たいです"},
            {"label": "polite negative", "form": "〜たくないです"},
            {"label": "past polite",     "form": "〜たかったです"},
            {"label": "casual",          "form": "〜たい"},
        ]},
    ],
    190: [  # 好きです
        {"title": "好き (like)", "forms": [
            {"label": "polite",          "form": "好きです"},
            {"label": "polite negative", "form": "好きじゃないです"},
            {"label": "past polite",     "form": "好きでした"},
            {"label": "casual",          "form": "好き"},
        ]},
    ],
    191: [  # 知っています / わかります
        {"title": "知る (to know a fact)", "forms": [
            {"label": "polite",          "form": "知っています"},
            {"label": "polite negative", "form": "知りません"},
            {"label": "past polite",     "form": "知っていました"},
            {"label": "casual",          "form": "知ってる"},
        ]},
        {"title": "わかる (to understand)", "forms": [
            {"label": "polite",          "form": "わかります"},
            {"label": "polite negative", "form": "わかりません"},
            {"label": "past polite",     "form": "わかりました"},
            {"label": "casual",          "form": "わかる"},
        ]},
    ],
    192: [  # 行きます
        {"title": "行く (to go)", "forms": [
            {"label": "polite",          "form": "行きます"},
            {"label": "polite negative", "form": "行きません"},
            {"label": "past polite",     "form": "行きました"},
            {"label": "casual",          "form": "行く"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # CHINESE (pks 216–221) — no conjugation; show affirmative/negative/aspect
    # -----------------------------------------------------------------------
    216: [  # 是 / 在
        {"title": "是 shì (equals/identity)", "forms": [
            {"label": "affirmative",      "form": "是"},
            {"label": "negative",         "form": "不是"},
            {"label": "question",         "form": "是吗？"},
        ]},
        {"title": "在 zài (location/existence)", "forms": [
            {"label": "affirmative",      "form": "在"},
            {"label": "negative",         "form": "不在"},
            {"label": "question",         "form": "在吗？"},
        ]},
    ],
    217: [  # 有
        {"title": "有 yǒu (to have / exist)", "forms": [
            {"label": "affirmative",      "form": "有"},
            {"label": "negative",         "form": "没有"},
            {"label": "question",         "form": "有吗？/ 有没有？"},
        ]},
    ],
    218: [  # 想要
        {"title": "想要 xiǎng yào (to want)", "forms": [
            {"label": "affirmative",      "form": "想要"},
            {"label": "want to do",       "form": "想 + verb"},
            {"label": "negative",         "form": "不想"},
        ]},
    ],
    219: [  # 喜欢
        {"title": "喜欢 xǐhuān (to like)", "forms": [
            {"label": "affirmative",      "form": "喜欢"},
            {"label": "negative",         "form": "不喜欢"},
            {"label": "question",         "form": "喜欢吗？"},
        ]},
    ],
    220: [  # 知道 / 认识
        {"title": "知道 zhīdào (know a fact)", "forms": [
            {"label": "affirmative",      "form": "知道"},
            {"label": "negative",         "form": "不知道"},
            {"label": "question",         "form": "知道吗？"},
        ]},
        {"title": "认识 rènshi (know a person)", "forms": [
            {"label": "affirmative",      "form": "认识"},
            {"label": "negative",         "form": "不认识"},
            {"label": "question",         "form": "认识吗？"},
        ]},
    ],
    221: [  # 去
        {"title": "去 qù (to go)", "forms": [
            {"label": "affirmative",      "form": "去"},
            {"label": "negative",         "form": "不去"},
            {"label": "going to (future)","form": "要去"},
            {"label": "went (past)",      "form": "去了"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # KOREAN (pks 245–250) — formal / informal polite / casual
    # -----------------------------------------------------------------------
    245: [  # 이다 / 있다
        {"title": "이다 (to be — identity)", "forms": [
            {"label": "formal",          "form": "입니다"},
            {"label": "informal polite", "form": "이에요 / 예요"},
            {"label": "casual",          "form": "이야 / 야"},
            {"label": "negative polite", "form": "아니에요"},
        ]},
        {"title": "있다 (to exist/be located)", "forms": [
            {"label": "formal",          "form": "있습니다"},
            {"label": "informal polite", "form": "있어요"},
            {"label": "casual",          "form": "있어"},
            {"label": "negative polite", "form": "없어요"},
        ]},
    ],
    246: [  # 있다 to have
        {"title": "있다 (to have)", "forms": [
            {"label": "formal",          "form": "있습니다"},
            {"label": "informal polite", "form": "있어요"},
            {"label": "casual",          "form": "있어"},
            {"label": "negative polite", "form": "없어요"},
            {"label": "negative casual", "form": "없어"},
        ]},
    ],
    247: [  # 원하다
        {"title": "원하다 (to want)", "forms": [
            {"label": "formal",          "form": "원합니다"},
            {"label": "informal polite", "form": "원해요"},
            {"label": "casual",          "form": "원해"},
            {"label": "want to do",      "form": "verb stem + 고 싶어요"},
        ]},
    ],
    248: [  # 좋아하다
        {"title": "좋아하다 (to like)", "forms": [
            {"label": "formal",          "form": "좋아합니다"},
            {"label": "informal polite", "form": "좋아해요"},
            {"label": "casual",          "form": "좋아해"},
            {"label": "negative polite", "form": "안 좋아해요"},
        ]},
    ],
    249: [  # 알다 / 모르다
        {"title": "알다 (to know)", "forms": [
            {"label": "formal",          "form": "압니다"},
            {"label": "informal polite", "form": "알아요"},
            {"label": "casual",          "form": "알아"},
        ]},
        {"title": "모르다 (to not know)", "forms": [
            {"label": "formal",          "form": "모릅니다"},
            {"label": "informal polite", "form": "몰라요"},
            {"label": "casual",          "form": "몰라"},
        ]},
    ],
    250: [  # 가다
        {"title": "가다 (to go)", "forms": [
            {"label": "formal",          "form": "갑니다"},
            {"label": "informal polite", "form": "가요"},
            {"label": "casual",          "form": "가"},
            {"label": "past polite",     "form": "갔어요"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # ARABIC (pks 274–279) — present tense by person/gender
    # -----------------------------------------------------------------------
    274: [  # كان / يكون
        {"title": "يكون — مضارع (present)", "forms": [
            {"label": "أنا (I)",          "form": "أكون"},
            {"label": "أنتَ (you m.)",    "form": "تكون"},
            {"label": "أنتِ (you f.)",    "form": "تكونين"},
            {"label": "هو (he)",          "form": "يكون"},
            {"label": "هي (she)",         "form": "تكون"},
            {"label": "نحن (we)",         "form": "نكون"},
            {"label": "هم (they)",        "form": "يكونون"},
        ]},
    ],
    275: [  # عنده / لديه — to have
        {"title": "عند + ضمير (to have)", "forms": [
            {"label": "أنا (I)",          "form": "عندي"},
            {"label": "أنتَ (you m.)",    "form": "عندك"},
            {"label": "هو (he)",          "form": "عنده"},
            {"label": "هي (she)",         "form": "عندها"},
            {"label": "نحن (we)",         "form": "عندنا"},
            {"label": "أنتم (you pl.)",   "form": "عندكم"},
            {"label": "هم (they)",        "form": "عندهم"},
        ]},
    ],
    276: [  # يريد
        {"title": "يريد — مضارع (present)", "forms": [
            {"label": "أنا (I)",          "form": "أريد"},
            {"label": "أنتَ (you m.)",    "form": "تريد"},
            {"label": "أنتِ (you f.)",    "form": "تريدين"},
            {"label": "هو (he)",          "form": "يريد"},
            {"label": "هي (she)",         "form": "تريد"},
            {"label": "نحن (we)",         "form": "نريد"},
            {"label": "هم (they)",        "form": "يريدون"},
        ]},
    ],
    277: [  # يحب
        {"title": "يحب — مضارع (present)", "forms": [
            {"label": "أنا (I)",          "form": "أحب"},
            {"label": "أنتَ (you m.)",    "form": "تحب"},
            {"label": "أنتِ (you f.)",    "form": "تحبين"},
            {"label": "هو (he)",          "form": "يحب"},
            {"label": "هي (she)",         "form": "تحب"},
            {"label": "نحن (we)",         "form": "نحب"},
            {"label": "هم (they)",        "form": "يحبون"},
        ]},
    ],
    278: [  # يعرف / يعلم
        {"title": "يعرف (know a person/place)", "forms": [
            {"label": "أنا (I)",          "form": "أعرف"},
            {"label": "أنتَ (you m.)",    "form": "تعرف"},
            {"label": "هو/هي",           "form": "يعرف / تعرف"},
            {"label": "نحن (we)",         "form": "نعرف"},
            {"label": "هم (they)",        "form": "يعرفون"},
        ]},
        {"title": "يعلم (know a fact)", "forms": [
            {"label": "أنا (I)",          "form": "أعلم"},
            {"label": "أنتَ (you m.)",    "form": "تعلم"},
            {"label": "هو/هي",           "form": "يعلم / تعلم"},
            {"label": "نحن (we)",         "form": "نعلم"},
            {"label": "هم (they)",        "form": "يعلمون"},
        ]},
    ],
    279: [  # يذهب
        {"title": "يذهب — مضارع (present)", "forms": [
            {"label": "أنا (I)",          "form": "أذهب"},
            {"label": "أنتَ (you m.)",    "form": "تذهب"},
            {"label": "أنتِ (you f.)",    "form": "تذهبين"},
            {"label": "هو (he)",          "form": "يذهب"},
            {"label": "هي (she)",         "form": "تذهب"},
            {"label": "نحن (we)",         "form": "نذهب"},
            {"label": "هم (they)",        "form": "يذهبون"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # RUSSIAN (pks 303–308)
    # -----------------------------------------------------------------------
    303: [  # быть
        {"title": "быть — present (есть for all, often omitted)", "forms": [
            {"label": "note",             "form": "Present tense 'есть' applies to all persons"},
            {"label": "я/ты/он/они",     "form": "есть (or omit)"},
        ]},
        {"title": "быть — future (буду)", "forms": [
            {"label": "я (I)",            "form": "буду"},
            {"label": "ты (you)",         "form": "будешь"},
            {"label": "он/она (he/she)",  "form": "будет"},
            {"label": "мы (we)",          "form": "будем"},
            {"label": "вы (you pl.)",     "form": "будете"},
            {"label": "они (they)",       "form": "будут"},
        ]},
    ],
    304: [  # у меня есть
        {"title": "у … есть (to have — lit. 'at me there is')", "forms": [
            {"label": "я (I)",            "form": "у меня есть"},
            {"label": "ты (you)",         "form": "у тебя есть"},
            {"label": "он (he)",          "form": "у него есть"},
            {"label": "она (she)",        "form": "у неё есть"},
            {"label": "мы (we)",          "form": "у нас есть"},
            {"label": "вы (you pl.)",     "form": "у вас есть"},
            {"label": "они (they)",       "form": "у них есть"},
        ]},
    ],
    305: [  # хотеть
        {"title": "хотеть — настоящее", "forms": [
            {"label": "я (I)",            "form": "хочу"},
            {"label": "ты (you)",         "form": "хочешь"},
            {"label": "он/она (he/she)",  "form": "хочет"},
            {"label": "мы (we)",          "form": "хотим"},
            {"label": "вы (you pl.)",     "form": "хотите"},
            {"label": "они (they)",       "form": "хотят"},
        ]},
    ],
    306: [  # нравиться / любить
        {"title": "нравиться (to appeal to — like gustar)", "forms": [
            {"label": "мне (I like)",     "form": "мне нравится / нравятся"},
            {"label": "тебе (you like)",  "form": "тебе нравится / нравятся"},
            {"label": "ему (he likes)",   "form": "ему нравится / нравятся"},
            {"label": "нам (we like)",    "form": "нам нравится / нравятся"},
            {"label": "им (they like)",   "form": "им нравится / нравятся"},
        ]},
        {"title": "любить (to love/really like)", "forms": [
            {"label": "я (I)",            "form": "люблю"},
            {"label": "ты (you)",         "form": "любишь"},
            {"label": "он/она (he/she)",  "form": "любит"},
            {"label": "мы (we)",          "form": "любим"},
            {"label": "вы (you pl.)",     "form": "любите"},
            {"label": "они (they)",       "form": "любят"},
        ]},
    ],
    307: [  # знать
        {"title": "знать — настоящее", "forms": [
            {"label": "я (I)",            "form": "знаю"},
            {"label": "ты (you)",         "form": "знаешь"},
            {"label": "он/она (he/she)",  "form": "знает"},
            {"label": "мы (we)",          "form": "знаем"},
            {"label": "вы (you pl.)",     "form": "знаете"},
            {"label": "они (they)",       "form": "знают"},
        ]},
    ],
    308: [  # идти / ехать
        {"title": "идти (go on foot — one direction)", "forms": [
            {"label": "я (I)",            "form": "иду"},
            {"label": "ты (you)",         "form": "идёшь"},
            {"label": "он/она (he/she)",  "form": "идёт"},
            {"label": "мы (we)",          "form": "идём"},
            {"label": "вы (you pl.)",     "form": "идёте"},
            {"label": "они (they)",       "form": "идут"},
        ]},
        {"title": "ехать (go by vehicle — one direction)", "forms": [
            {"label": "я (I)",            "form": "еду"},
            {"label": "ты (you)",         "form": "едешь"},
            {"label": "он/она (he/she)",  "form": "едет"},
            {"label": "мы (we)",          "form": "едем"},
            {"label": "вы (you pl.)",     "form": "едете"},
            {"label": "они (they)",       "form": "едут"},
        ]},
    ],

    # -----------------------------------------------------------------------
    # SWEDISH (pks 332–337) — present tense same for all persons
    # -----------------------------------------------------------------------
    332: [  # vara
        {"title": "vara — presens", "forms": [
            {"label": "all persons",  "form": "är"},
            {"label": "negative",     "form": "är inte"},
            {"label": "past",         "form": "var"},
            {"label": "past negative","form": "var inte"},
        ]},
    ],
    333: [  # ha
        {"title": "ha — presens", "forms": [
            {"label": "all persons",  "form": "har"},
            {"label": "negative",     "form": "har inte"},
            {"label": "past",         "form": "hade"},
        ]},
    ],
    334: [  # vilja
        {"title": "vilja — presens", "forms": [
            {"label": "all persons",  "form": "vill"},
            {"label": "negative",     "form": "vill inte"},
            {"label": "past",         "form": "ville"},
        ]},
    ],
    335: [  # gilla / tycka om
        {"title": "gilla (casual like)", "forms": [
            {"label": "all persons",  "form": "gillar"},
            {"label": "negative",     "form": "gillar inte"},
            {"label": "past",         "form": "gillade"},
        ]},
        {"title": "tycka om (like/appreciate)", "forms": [
            {"label": "all persons",  "form": "tycker om"},
            {"label": "negative",     "form": "tycker inte om"},
            {"label": "past",         "form": "tyckte om"},
        ]},
    ],
    336: [  # veta / känna
        {"title": "veta (know a fact)", "forms": [
            {"label": "all persons",  "form": "vet"},
            {"label": "negative",     "form": "vet inte"},
            {"label": "past",         "form": "visste"},
        ]},
        {"title": "känna (know a person)", "forms": [
            {"label": "all persons",  "form": "känner"},
            {"label": "negative",     "form": "känner inte"},
            {"label": "past",         "form": "kände"},
        ]},
    ],
    337: [  # gå
        {"title": "gå — presens", "forms": [
            {"label": "all persons",  "form": "går"},
            {"label": "negative",     "form": "går inte"},
            {"label": "past",         "form": "gick"},
        ]},
    ],
}
# fmt: on


def populate(apps, schema_editor):
    Phrase = apps.get_model('lessons', 'Phrase')
    for pk, conjugations in CONJUGATIONS.items():
        Phrase.objects.filter(pk=pk).update(conjugations=conjugations)


def depopulate(apps, schema_editor):
    Phrase = apps.get_model('lessons', 'Phrase')
    Phrase.objects.filter(pk__in=CONJUGATIONS.keys()).update(conjugations=[])


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_conjugations_field'),
    ]

    operations = [
        migrations.RunPython(populate, depopulate),
    ]
