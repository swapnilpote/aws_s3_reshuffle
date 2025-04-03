import os
from typing import List, Optional
from datetime import datetime
from loguru import logger
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm

from app.core.config import settings
from app.models.s3_models import FileRecord, DownloadResponse
from app.services.mongodb_service import MongoDBService

class S3Service:
    """Service class to handle S3 operations."""
    
    def __init__(self, mongodb_service: MongoDBService):
        """Initialize the S3 service."""
        self.s3_client = self._get_s3_client()
        self.source_bucket = settings.SOURCE_BUCKET
        self.download_path = settings.DOWNLOAD_PATH
        self.mongodb = mongodb_service
        
        # Create download directory if it doesn't exist
        os.makedirs(self.download_path, exist_ok=True)
        
        logger.info(f"Initialized S3 service with bucket: {self.source_bucket}")
    
    def _get_s3_client(self):
        """Create and return an S3 client with retry configuration."""
        session = boto3.Session(**settings.get_aws_config())
        return session.client('s3', config=boto3.Config(
            retries=dict(
                max_attempts=settings.MAX_RETRIES,
                mode='standard'
            )
        ))
    
    def _get_object_size(self, key: str) -> int:
        """Get the size of an S3 object."""
        try:
            response = self.s3_client.head_object(Bucket=self.source_bucket, Key=key)
            return response['ContentLength']
        except ClientError as e:
            logger.error(f"Error getting object size for {key}: {str(e)}")
            raise
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    async def download_file(self, file_record: FileRecord) -> bool:
        """Download a single file from S3."""
        try:
            # Create local directory structure
            local_dir = os.path.join(
                self.download_path,
                file_record.lane_id,
                file_record.timestamp.strftime("%Y/%m/%d/%H")
            )
            os.makedirs(local_dir, exist_ok=True)
            
            # Generate local file path
            local_path = os.path.join(local_dir, os.path.basename(file_record.file_path))
            
            # Get file size for progress bar
            size = self._get_object_size(file_record.file_path)
            logger.info(f"Downloading {file_record.file_path} ({self._format_size(size)})")
            
            # Download file with progress bar
            with tqdm(total=size, unit='B', unit_scale=True, desc=f"Downloading {os.path.basename(file_record.file_path)}") as pbar:
                self.s3_client.download_file(
                    self.source_bucket,
                    file_record.file_path,
                    local_path,
                    Callback=lambda bytes_transferred: pbar.update(bytes_transferred)
                )
            
            # Update file record with local path and status
            file_record.local_path = local_path
            file_record.status = "downloaded"
            await self.mongodb.update_file_status(
                file_record.file_path,
                "downloaded",
                local_path
            )
            
            logger.info(f"Successfully downloaded {file_record.file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {file_record.file_path}: {str(e)}")
            file_record.status = "failed"
            await self.mongodb.update_file_status(file_record.file_path, "failed")
            return False
    
    async def download_files_by_lane_and_hour(
        self,
        lane_id: str,
        hour: int,
        date: datetime
    ) -> DownloadResponse:
        """Download files for a specific lane and hour."""
        # Get files from MongoDB
        files = await self.mongodb.get_files_by_lane_and_hour(lane_id, hour, date)
        
        results = DownloadResponse(
            successful=[],
            failed=[],
            total_files=len(files),
            success_count=0,
            failure_count=0
        )
        
        # Download each file
        for file_record in files:
            if await self.download_file(file_record):
                results.successful.append(file_record)
                results.success_count += 1
            else:
                results.failed.append(file_record.file_path)
                results.failure_count += 1
        
        return results 