import math
from .scorer_constants import (
    FEATURE_WEIGHTS,
    INTENSITY_WATCHLIST,
    BIAS,
    INTERACTION_BOOSTS,
)


def compute_signal_intensities(feature_dict):
    scoring_features = feature_dict.copy()
    token_count = max(scoring_features.get('token_estimate', 1), 1)
    for f in INTENSITY_WATCHLIST.keys():
        intensity = scoring_features[f] / token_count
        scoring_features[INTENSITY_WATCHLIST[f]] = intensity

    return scoring_features


def compute_weighted_sum(feature_dict):
    total = BIAS
    for feat in FEATURE_WEIGHTS:
        total += FEATURE_WEIGHTS[feat] * feature_dict.get(feat, 0)

    return total


def apply_interaction_boosts(feature_dict, score):
    reasons = set()

    if feature_dict["urgency_density"] > 0.02 and feature_dict["suspicious_tld_count"] > 0:
        score += INTERACTION_BOOSTS["urgency_tld"]
        reasons.add("Urgency combined with suspicious link.")

    if feature_dict["reward_density"] > 0.02 and feature_dict["suspicious_tld_count"] > 0:
        score += INTERACTION_BOOSTS["reward_tld"]
        reasons.add("Reward language combined with suspicious link.")

    if feature_dict["urgency_density"] > 0.02 and feature_dict["has_phone"] > 0:
        score += INTERACTION_BOOSTS["urgency_phone"]
        reasons.add("Urgency combined with phone contact.")

    return score, reasons


def sigmoid(x):
    return (1 / (1 + math.exp(-x)))


def scorer(features: dict) -> dict[str, str | list[str]]:
    # check if dictionary passed is not empty
    if not features:
        return {}

    scored_signals = compute_signal_intensities(features)
    weighted_sum = compute_weighted_sum(scored_signals)
    score, reasons = apply_interaction_boosts(scored_signals, weighted_sum)
    score = sigmoid(score)
    result = {
        "score": score,
        "reasons": list(reasons),
    }

    return result
