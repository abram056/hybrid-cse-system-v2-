FEATURE_WEIGHTS = {
    "has_phone": 0.8,
    "suspicious_tld_count": 2.0,
    "urgency_density": 20.0,
    "reward_density": 15.0,
    "known_smish_density": 25.0,
}


INTENSITY_WATCHLIST = {
    "urgency_term_hits": "urgency_density",
    "reward_term_hits": "reward_density",
    "known_smishing_phrase_hits": "known_smish_density",
}

INTERACTION_BOOSTS = {
    "urgency_tld": 1.0,
    "reward_tld": 0.8,
    "urgency_phone": 0.7,
}

BIAS = -2.0
