# extractor.py
from urllib.parse import urlparse
import re
from .patterns import (
    URL_PATTERN,
    PHONE_PATTERNS,
    SUSPICIOUS_TLDS,
    KNOWN_SMISHING_PHRASES,
    URGENCY_TERMS,
    REWARD_TERMS,
    SUSPICIOUS_TERM_PAIRS
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


def _proximity_hits(text: str, term_groups: list[tuple[str, str]], window: int = 5) -> int:
    """
    Counts how many times two terms appear within
    `window` tokens of each other.
    """
    tokens = text.lower().split()
    count = 0

    for term1, term2 in term_groups:
        for i, token in enumerate(tokens):
            if term1 in token:
                start = max(0, i - window)
                end = min(len(tokens), i + window + 1)
                if any(term2 in t for t in tokens[start:end]):
                    count += 1
    return count


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

    # ---------------------------
    # Structural Features
    # ----------------------------
    tokens = text.split()
    text_length = len(text)

    # digit ratio
    digit_count = sum(c.isdigit() for c in text)
    digit_ratio = digit_count / text_length if text_length > 0 else 0

    # Numeric tokens
    numeric_tokens = [t for t in tokens if t.isdigit()]
    numeric_token_count = len(numeric_tokens)

    # Short codes (4–6 digits)
    short_code_count = sum(1 for t in numeric_tokens if 4 <= len(t) <= 6)

    # Uppercase ratio
    uppercase_count = sum(c.isupper() for c in text)
    uppercase_ratio = uppercase_count / text_length if text_length > 0 else 0

    # Repeated punctuation
    repeated_punct_count = len(re.findall(r"[!$?]{2,}", text))

    proximity_hits = _proximity_hits(text, SUSPICIOUS_TERM_PAIRS)
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
        "digit_ratio": digit_ratio,
        "numeric_token_count": numeric_token_count,
        "short_code_count": short_code_count,
        "uppercase_ratio": uppercase_ratio,
        "repeated_punct_count": repeated_punct_count,
        "proximity_suspicious_hits": proximity_hits,
    }

    return features
