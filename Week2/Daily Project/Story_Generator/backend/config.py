import os

class Config:
    """
    Application configuration.
    """
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your-default-gemini-key')