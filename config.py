import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to manage environment variables and settings."""
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    
    # S3 Buckets
    SOURCE_BUCKET: str = os.getenv('SOURCE_BUCKET', '')
    DESTINATION_BUCKET: str = os.getenv('DESTINATION_BUCKET', '')
    
    # Transfer Settings
    MAX_RETRIES: int = 3
    CHUNK_SIZE: int = 8 * 1024 * 1024  # 8MB chunks for multipart uploads
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration values."""
        required_vars = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'AWS_REGION',
            'SOURCE_BUCKET',
            'DESTINATION_BUCKET'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    @classmethod
    def get_aws_config(cls) -> Dict[str, Any]:
        """Get AWS configuration dictionary."""
        return {
            'aws_access_key_id': cls.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': cls.AWS_SECRET_ACCESS_KEY,
            'region_name': cls.AWS_REGION
        } 