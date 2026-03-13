from hybrid_cse_system_v2.interpreter.rbs_interpreter import generate_reasons


def test_reason_generator_returns_reasons_for_smish():
    rbs_features = {
        "url_count": 1,
        "has_url": 1,
        "suspicious_tld_count": 1,
        "phone_count": 0,
        "has_phone": 0,
        "known_smishing_phrase_hits": 2,
        "urgency_term_hits": 2,
        "reward_term_hits": 1,
        "text_length": 488,
        "token_estimate": 75,
        "digit_ratio": 0.012295082,
        "numeric_token_count": 6,
        "short_code_count": 1,
        "uppercase_ratio": 0.0,
        "repeated_punct_count": 0,
        "proximity_suspicious_hits": 2,
    }

    reasons = generate_reasons(rbs_features)

    assert isinstance(reasons, list)
    assert len(reasons) > 0
    assert any("Short numeric code detected" in reason for reason in reasons)
    assert any(
        "Urgency and reward terms detected together"
        in reason for reason in reasons
    )
    assert any(
        "Sensitive account verification language detected"
        in reason for reason in reasons
    )


def test_reason_generator_returns_reasons_for_ham():
    rbs_features = {
        "url_count": 0,
        "has_url": 0,
        "suspicious_tld_count": 0,
        "phone_count": 0,
        "has_phone": 0,
        "known_smishing_phrase_hits": 0,
        "urgency_term_hits": 0,
        "reward_term_hits": 0,
        "text_length": 488,
        "token_estimate": 75,
        "digit_ratio": 0.0075757575757576,
        "numeric_token_count": 0,
        "short_code_count": 0,
        "uppercase_ratio": 0.030303030303030304,
        "repeated_punct_count": 0,
        "proximity_suspicious_hits": 0,
    }

    reasons = generate_reasons(rbs_features)

    assert isinstance(reasons, list)
    assert len(reasons) == 0


def test_reason_generator_returns_reasons_for_spam():
    rbs_features = {
        "url_count": 0,
        "has_url": 0,
        "suspicious_tld_count": 0,
        "phone_count": 0,
        "has_phone": 0,
        "known_smishing_phrase_hits": 2,
        "urgency_term_hits": 2,
        "reward_term_hits": 4,
        "text_length": 370,
        "token_estimate": 53,
        "digit_ratio": 0.0,
        "numeric_token_count": 0,
        "short_code_count": 0,
        "uppercase_ratio": 0.05945945945945946,
        "repeated_punct_count": 0,
        "proximity_suspicious_hits": 0,
    }

    reasons = generate_reasons(rbs_features)

    assert isinstance(reasons, list)
    assert len(reasons) > 0
    assert any(
        "Urgency and reward terms detected together"
        in reason for reason in reasons
    )
    assert any("Known smish phrase detected" in reason for reason in reasons)
