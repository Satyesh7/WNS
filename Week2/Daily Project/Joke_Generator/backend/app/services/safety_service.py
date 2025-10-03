from app.config.banned_keywords import FORBIDDEN_KEYWORDS

def is_prompt_safe(prompt: str) -> bool:
    """
    Checks if a user's prompt contains any forbidden keywords.
    The check is case-insensitive.

    Args:
        prompt: The user-provided string.

    Returns:
        True if the prompt is safe, False otherwise.
    """
    if not prompt:
        return False  # An empty prompt is not considered safe to proceed.

    # Normalize the prompt to lowercase for case-insensitive matching
    lower_prompt = prompt.lower()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in lower_prompt:
            return False  # Found a forbidden keyword
            
    return True  # No forbidden keywords were found