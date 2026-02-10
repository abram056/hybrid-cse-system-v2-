# extractor.py
from urllib.parse import urlparse
from .patterns import (
    URL_PATTERN,
    PHONE_PATTERNS,
    SUSPICIOUS_TLDS,
    KNOWN_SMISHING_PHRASES,
    URGENCY_TERMS,
    REWARD_TERMS,
)


def _count_phrase_hits(text: str, phrases: list[str]) -> int:
    """
    Counts how many times any phrase in `phrases` appears in text.
    Simple substring matching, case-insensitive.
    """
    # TDOD: Add explanations, what phrases fired
    text_lower = text.lower()
    count = 0
    for phrase in phrases:
        count += text_lower.count(phrase)
    return count


def _extract_tlds(urls: list[str]) -> list[str]:
    """
    Extracts TLDs from a list of URLs.
    """
    tlds = []
    for url in urls:
        try:
            parsed = urlparse(url)
            host = parsed.netloc or parsed.path
            if "." in host:
                tlds.append("." + host.split(".")[-1].lower())
        except Exception:
            continue
    return tlds


def extract_rbs_features(text: str) -> dict:
    """
    Extract rule-based features from a single text input.
    Returns a flat dictionary of numeric features.
    """

    if not isinstance(text, str):
        text = ""

    # -------------------------
    # URL features
    # -------------------------
    urls = URL_PATTERN.findall(text)
    url_count = len(urls)

    tlds = _extract_tlds(urls)
    suspicious_tld_count = sum(1 for tld in tlds if tld in SUSPICIOUS_TLDS)

    # -------------------------
    # Phone number features
    # -------------------------
    phone_matches = PHONE_PATTERNS.findall(text)
    phone_count = len(phone_matches)

    # -------------------------
    # Phrase-based features
    # -------------------------
    smishing_phrase_hits = _count_phrase_hits(text, KNOWN_SMISHING_PHRASES)
    urgency_hits = _count_phrase_hits(text, URGENCY_TERMS)
    reward_hits = _count_phrase_hits(text, REWARD_TERMS)

    # -------------------------
    # Aggregate feature dict
    # -------------------------
    features = {
        "url_count": url_count,
        "has_url": int(url_count > 0),
        "suspicious_tld_count": suspicious_tld_count,
        "phone_count": phone_count,
        "has_phone": int(phone_count > 0),
        "known_smishing_phrase_hits": smishing_phrase_hits,
        "urgency_term_hits": urgency_hits,
        "reward_term_hits": reward_hits,
        "text_length": len(text),
        "token_estimate": len(text.split()),
    }

    return features
