import os
from typing import Dict, Any
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "S3 File Download API"
    VERSION: str = "1.0.0"
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    
    # S3 Bucket
    SOURCE_BUCKET: str = os.getenv('SOURCE_BUCKET', '')
    
    # MongoDB Settings
    MONGODB_URL: str = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    MONGODB_DB_NAME: str = os.getenv('MONGODB_DB_NAME', 's3_files')
    MONGODB_COLLECTION: str = os.getenv('MONGODB_COLLECTION', 'file_records')
    
    # Download Settings
    DOWNLOAD_PATH: str = os.getenv('DOWNLOAD_PATH', './downloads')
    MAX_RETRIES: int = 3
    CHUNK_SIZE: int = 8 * 1024 * 1024  # 8MB chunks for multipart downloads
    
    class Config:
        case_sensitive = True
        env_file = ".env"

    def get_aws_config(self) -> Dict[str, Any]:
        """Get AWS configuration dictionary."""
        return {
            'aws_access_key_id': self.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': self.AWS_SECRET_ACCESS_KEY,
            'region_name': self.AWS_REGION
        }

settings = Settings() 