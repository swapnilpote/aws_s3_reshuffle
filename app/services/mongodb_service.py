from datetime import datetime
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

from app.core.config import settings
from app.models.s3_models import FileRecord

class MongoDBService:
    """Service class to handle MongoDB operations."""
    
    def __init__(self):
        """Initialize MongoDB connection."""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db[settings.MONGODB_COLLECTION]
        logger.info(f"Initialized MongoDB connection to {settings.MONGODB_URL}")
    
    async def save_file_record(self, file_record: FileRecord) -> None:
        """Save a file record to MongoDB."""
        try:
            await self.collection.insert_one(file_record.model_dump())
            logger.info(f"Saved file record for {file_record.file_path}")
        except Exception as e:
            logger.error(f"Error saving file record: {str(e)}")
            raise
    
    async def get_files_by_lane_and_hour(
        self,
        lane_id: str,
        hour: int,
        date: datetime
    ) -> List[FileRecord]:
        """Get files for a specific lane and hour."""
        try:
            # Create start and end datetime for the specified hour
            start_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_time = date.replace(hour=hour, minute=59, second=59, microsecond=999999)
            
            cursor = self.collection.find({
                "lane_id": lane_id,
                "timestamp": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            })
            
            files = []
            async for doc in cursor:
                files.append(FileRecord(**doc))
            
            logger.info(f"Found {len(files)} files for lane {lane_id} at hour {hour}")
            return files
            
        except Exception as e:
            logger.error(f"Error getting files by lane and hour: {str(e)}")
            raise
    
    async def update_file_status(
        self,
        file_path: str,
        status: str,
        local_path: Optional[str] = None
    ) -> None:
        """Update file status in MongoDB."""
        try:
            update_data = {"status": status}
            if local_path:
                update_data["local_path"] = local_path
                
            await self.collection.update_one(
                {"file_path": file_path},
                {"$set": update_data}
            )
            logger.info(f"Updated status for {file_path} to {status}")
        except Exception as e:
            logger.error(f"Error updating file status: {str(e)}")
            raise 