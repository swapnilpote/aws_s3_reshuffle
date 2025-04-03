from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime

from app.models.s3_models import TransferRequest, TransferResponse, HealthCheck, DownloadRequest, DownloadResponse
from app.services.s3_service import S3Service
from app.services.mongodb_service import MongoDBService
from app.core.config import settings

router = APIRouter()

def get_mongodb_service() -> MongoDBService:
    """Dependency to get MongoDBService instance."""
    return MongoDBService()

def get_s3_service(mongodb_service: MongoDBService = Depends(get_mongodb_service)) -> S3Service:
    """Dependency to get S3Service instance."""
    return S3Service(mongodb_service)

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=settings.VERSION
    )

@router.post("/transfer", response_model=TransferResponse)
async def transfer_files(
    request: TransferRequest,
    s3_service: S3Service = Depends(get_s3_service)
) -> TransferResponse:
    """
    Transfer files between S3 buckets.
    
    - If file_keys is provided, transfers only those specific files
    - If prefix is provided, transfers all files with that prefix
    - If neither is provided, transfers all files
    """
    try:
        if request.file_keys:
            return s3_service.transfer_files(request.file_keys)
        elif request.prefix:
            return s3_service.transfer_files_with_prefix(request.prefix)
        else:
            return s3_service.transfer_all_files()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during file transfer: {str(e)}"
        )

@router.post("/download", response_model=DownloadResponse)
async def download_files(
    request: DownloadRequest,
    s3_service: S3Service = Depends(get_s3_service)
) -> DownloadResponse:
    """
    Download files from S3 based on lane ID and hour.
    
    - Downloads files for the specified lane ID
    - Filters files by the specified hour
    - Files are downloaded to a local directory structure
    - Download status is tracked in MongoDB
    """
    try:
        return await s3_service.download_files_by_lane_and_hour(
            request.lane_id,
            request.hour,
            request.date
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during file download: {str(e)}"
        ) 