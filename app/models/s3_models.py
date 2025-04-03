from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class DownloadRequest(BaseModel):
    """Request model for file download operations."""
    lane_id: str = Field(..., description="Lane ID to filter files")
    hour: int = Field(..., description="Hour of the day (0-23)", ge=0, le=23)
    date: datetime = Field(..., description="Date to download files for")

class FileRecord(BaseModel):
    """MongoDB document model for file records."""
    file_path: str = Field(..., description="S3 file path")
    lane_id: str = Field(..., description="Lane ID")
    timestamp: datetime = Field(..., description="File timestamp")
    local_path: str = Field(..., description="Local download path")
    size: int = Field(..., description="File size in bytes")
    status: str = Field(..., description="Download status")

class DownloadResponse(BaseModel):
    """Response model for download operations."""
    successful: List[FileRecord] = Field(default_factory=list, description="List of successfully downloaded files")
    failed: List[str] = Field(default_factory=list, description="List of failed downloads")
    total_files: int = Field(..., description="Total number of files processed")
    success_count: int = Field(..., description="Number of successful downloads")
    failure_count: int = Field(..., description="Number of failed downloads")

class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version") 