# ============================================================
# MANIPULATION WORDS
# ============================================================

fear_words = [
    "destroy", "danger", "threat", "crisis", "attack", "collapse",
    "catastrophe", "disaster", "chaos", "panic", "terror", "violence",
    "war", "invasion", "explosion", "deadly", "fatal", "kill",
    "eliminate", "wipe out", "annihilate", "devastate", "ruin"
]

loaded_words = [
    "radical", "corrupt", "evil", "shameful", "disgusting", "pathetic",
    "outrageous", "criminal", "traitor", "liar", "fraud", "incompetent",
    "coward", "hypocrite", "extremist", "fanatic", "puppet", "regime",
    "propaganda", "brainwash", "manipulate", "exploit", "abuse"
]

exaggeration_words = [
    "always", "never", "everyone", "nobody", "nothing", "everything",
    "worst", "best", "greatest", "most", "least", "totally", "absolutely",
    "completely", "utterly", "literally", "insane", "unbelievable",
    "shocking", "incredible", "unprecedented", "historic", "massive"
]

clickbait_words = [
    "you won't believe", "shocking truth", "they don't want you to know",
    "secret", "exposed", "revealed", "breaking", "urgent", "warning",
    "miracle", "cure", "banned", "censored", "hidden", "leaked"
]

# All manipulation words combined
ALL_MANIPULATION_WORDS = (
    fear_words + loaded_words + exaggeration_words + clickbait_words
)


# ============================================================
# BIAS WORDS
# ============================================================

left_words = [
    "equality", "diversity", "inclusion", "climate change", "welfare",
    "progressive", "social justice", "universal healthcare", "green energy",
    "renewable", "lgbtq", "feminism", "gun control", "tax the rich",
    "working class", "unions", "regulate", "systemic", "privilege",
    "marginalized", "oppression", "activist", "protest", "reform"
]

right_words = [
    "freedom", "patriot", "traditional", "border security", "second amendment",
    "tax cuts", "free market", "small government", "law and order",
    "national security", "immigration control", "america first",
    "constitution", "military", "pro-life", "religious freedom",
    "capitalism", "socialism bad", "deep state", "mainstream media",
    "cancel culture", "woke", "elite", "globalist"
]

neutral_words = [
    "according to", "reports suggest", "officials say", "research shows",
    "data indicates", "study finds", "analysts say", "sources confirm",
    "government announced", "statistics show"
]