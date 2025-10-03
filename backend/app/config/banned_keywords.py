# List of keywords that will be blocked by the safety service.
# This check is case-insensitive.

FORBIDDEN_KEYWORDS = [
    # Violence & Tragedy
    "attack", "bomb", "massacre", "terror", "terrorist", "shooting", "murder", "riot",
    "hijack", "hostage", "disaster", "crash", "war", "assassination",

    # Self-Harm
    "suicide", "self-harm",

    # Hate Speech & Discrimination
    "racist", "racism", "nazi", "supremacy", "sexist", "homophobic", "xenophobic",
    
    # Specific Sensitive Events (as requested)
    "taj mumbai", "9/11", "holocaust",
    
    # Adult & Explicit
    "porn", "erotic", "adult", "explicit"
]