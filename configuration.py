import os 
import dotenv
dotenv.load_dotenv()

class Settings:
    SECURITY_KEY: str = os.getenv("SECURITY_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")