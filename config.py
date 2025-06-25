import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'questiondb')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Suman@123')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    @classmethod
    def get_database_uri(cls):
        """Generate database URI from configuration with proper URL encoding."""
        # URL encode the password to handle special characters
        encoded_password = quote_plus(cls.DB_PASSWORD)
        return f"mysql+pymysql://{cls.DB_USER}:{encoded_password}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}" 

    def __init__(self):
        print("Loaded OpenAI key:", self.OPENAI_API_KEY)

print("Loaded OpenAI key:", os.getenv('OPENAI_API_KEY'))
print("Loaded OpenAI key (from Config):", Config.OPENAI_API_KEY) 