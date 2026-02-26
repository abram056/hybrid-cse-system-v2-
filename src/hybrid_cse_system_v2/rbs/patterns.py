import re

# URL Patterns
URL_PATTERN = re.compile(
    r"(https?://|www\.)[^|s]+",
    re.IGNORECASE
)

SUSPICIOUS_TLDS = {
    ".ru", ".cn", ".tk", ".xyz", ".top",
    ".icu", ".cfd", ".sbs", ".bond", ".win",
    ".help", ".xin", ".zip", ".mov", ".cf",
    ".ml", ".ga", ".gq", ".cm", ".co",
}

PHONE_PATTERNS = re.compile(
    r"(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}"
)

KNOWN_SMISHING_PHRASES = [
    "verify your account",
    "account suspended",
    "unusual activity",
    "click the link",
    "confirm your identity",
    "your account will be closed",
    "act now",
    "limited time",
    "to claim your",
    "click this link",
    "account has been",
    "claim your prize",
    "click here to",
    "your account has",
    "the link below",
    "on your account",
    "congrats youve won",
    "has been flagged",
    "this link now",
    "link to claim",
    "account has been compromised",
    "sensitive information",
]

URGENCY_TERMS = [
    "urgent",
    "immediately",
    "asap",
    "now",
    "today",
    "final notice",
    "last chance",
]

REWARD_TERMS = [
    "won",
    "winner",
    "free",
    "reward",
    "claim",
    "prize",
]

SUSPICIOUS_TERM_PAIRS = [
    ("verify", "account"),
    ("confirm", "identity"),
    ("account", "suspend"),
    ("click", "link"),
    ("claim", "prize"),
]
