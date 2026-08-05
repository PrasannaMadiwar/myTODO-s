import os 

class Settings:
    SECURITY_KEY: str = os.getenv("SECURITY_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")