from .reasons import REASON_MESSAGES

def generate_reasons(features):
    reasons = []

    if features["short_code_count"] > 0:
        reasons.append(REASON_MESSAGES["short_code"])

    if features["has_url"] and features["suspicious_tld_count"] > 0:
        reasons.append(REASON_MESSAGES["suspicious_link"])

    if (
        features["urgency_term_hits"] > 0 and
        features["reward_term_hits"] > 0
    ):
        reasons.append(REASON_MESSAGES["urgency_reward_combo"])

    if features["proximity_suspicious_hits"] > 0:
        reasons.append(REASON_MESSAGES["account_verification_language"])

    if features["digit_ratio"] > 0.2:
        reasons.append(REASON_MESSAGES["excessive_digits"])

    if features["uppercase_ratio"] > 0.3:
        reasons.append(REASON_MESSAGES["excessive_uppercase"])

    if features["repeated_punct_count"] > 0:
        reasons.append(REASON_MESSAGES["repeated_punctuation"])

    return reasons