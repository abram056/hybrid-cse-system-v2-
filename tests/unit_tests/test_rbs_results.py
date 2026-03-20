from hybrid_cse_system_v2.rbs.extractor import extract_rbs_features


def test_ham_message_features():
    text = "Hey bro, are you coming to class?"

    features = extract_rbs_features(text)
    key_flags = [
        "url_count", "has_url", "suspicious_tld_count",
        "phone_count", "has_phone", "known_smishing_phrase_hits",
        "urgency_term_hits", "reward_term_hits",
        "digit_ratio", "numeric_token_count",
        "short_code_count", "repeated_punct_count",
        "proximity_suspicious_hits",
    ]

    assert isinstance(features, dict)
    assert len(features) > 0
    for flag in key_flags:
        assert features[flag] == 0


def test_spam_message_features():
    text = """
        ttention Customers
        Get your exclusive offer now! Limited time only - Free Shipping on all orders!
        Click here to claim yours - https://fakebank.xyz
        Don't miss this chance!
        #SaleProjo #FreeShippin
        """

    features = extract_rbs_features(text)

    assert isinstance(features, dict)
    assert len(features) > 0
    assert features["url_count"] == 1
    assert features["has_url"] == 1
    # assert features["suspicious_tld_count"] == 1
    assert features["phone_count"] == 0
    assert features["has_phone"] == 0
    assert features["known_smishing_phrase_hits"] >= 1
    assert features["urgency_term_hits"] >= 1
    assert features["reward_term_hits"] >= 1
    assert features["numeric_token_count"] == 0
    assert features["short_code_count"] == 0
    assert features["repeated_punct_count"] == 0
    assert features["proximity_suspicious_hits"] == 0


def test_smish_message_features():
    text = """
        "Dear Custromer,
        We've just discovered something suspicious about your account and need
         to act fast! Your credit card information was recently accessed
         without authorization.
        If you don't take immediate action, we'll have to freeze it permanently!
        Click on this link: <https://www.example.com/freeze-account
        Don’t delay - before it’s too late!
        Best regards,
        The Security Team
        """

    features = extract_rbs_features(text)

    assert isinstance(features, dict)
    assert len(features) > 0
    assert features["url_count"] == 1
    assert features["has_url"] == 1
    assert features["suspicious_tld_count"] == 0
    assert features["phone_count"] == 0
    assert features["has_phone"] == 0
    # assert features["known_smishing_phrase_hits"] >= 1
    assert features["urgency_term_hits"] >= 1
    assert features["reward_term_hits"] >= 0
    assert features["numeric_token_count"] == 0
    assert features["short_code_count"] == 0
    assert features["repeated_punct_count"] == 0
    assert features["proximity_suspicious_hits"] >= 1
