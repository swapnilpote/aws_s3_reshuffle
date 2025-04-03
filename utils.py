from typing import List, Optional
from loguru import logger
import boto3
from botocore.exceptions import ClientError
from config import Config

def setup_logger() -> None:
    """Configure logging settings."""
    logger.add(
        "s3_transfer.log",
        rotation="500 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

def get_s3_client():
    """Create and return an S3 client with retry configuration."""
    session = boto3.Session(**Config.get_aws_config())
    s3_client = session.client('s3', config=boto3.Config(
        retries=dict(
            max_attempts=Config.MAX_RETRIES,
            mode='standard'
        )
    ))
    return s3_client

def list_bucket_objects(bucket: str, prefix: Optional[str] = None) -> List[str]:
    """
    List all objects in a bucket with optional prefix.
    
    Args:
        bucket: Name of the S3 bucket
        prefix: Optional prefix to filter objects
        
    Returns:
        List of object keys
    """
    s3_client = get_s3_client()
    objects = []
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if 'Contents' in page:
                objects.extend(obj['Key'] for obj in page['Contents'])
    except ClientError as e:
        logger.error(f"Error listing objects in bucket {bucket}: {str(e)}")
        raise
    
    return objects

def get_object_size(bucket: str, key: str) -> int:
    """
    Get the size of an S3 object.
    
    Args:
        bucket: Name of the S3 bucket
        key: Object key
        
    Returns:
        Size of the object in bytes
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)
        return response['ContentLength']
    except ClientError as e:
        logger.error(f"Error getting object size for {key} in bucket {bucket}: {str(e)}")
        raise

def format_size(size_bytes: int) -> str:
    """
    Format size in bytes to human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB" 