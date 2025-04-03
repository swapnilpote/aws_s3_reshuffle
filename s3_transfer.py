from typing import List, Optional
from loguru import logger
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm

from config import Config
from utils import (
    setup_logger,
    get_s3_client,
    list_bucket_objects,
    get_object_size,
    format_size
)

class S3Transfer:
    """Class to handle S3 file transfers between buckets."""
    
    def __init__(self):
        """Initialize the S3 transfer utility."""
        setup_logger()
        Config.validate()
        self.s3_client = get_s3_client()
        self.source_bucket = Config.SOURCE_BUCKET
        self.destination_bucket = Config.DESTINATION_BUCKET
        logger.info(f"Initialized S3 transfer from {self.source_bucket} to {self.destination_bucket}")
    
    def transfer_file(self, key: str) -> bool:
        """
        Transfer a single file from source to destination bucket.
        
        Args:
            key: The key of the file to transfer
            
        Returns:
            bool: True if transfer was successful, False otherwise
        """
        try:
            # Get object size for progress bar
            size = get_object_size(self.source_bucket, key)
            
            # Create progress bar
            pbar = tqdm(
                total=size,
                unit='B',
                unit_scale=True,
                desc=f"Transferring {key}"
            )
            
            # Copy object
            self.s3_client.copy_object(
                CopySource={'Bucket': self.source_bucket, 'Key': key},
                Bucket=self.destination_bucket,
                Key=key
            )
            
            pbar.close()
            logger.info(f"Successfully transferred {key} ({format_size(size)})")
            return True
            
        except ClientError as e:
            logger.error(f"Error transferring {key}: {str(e)}")
            return False
    
    def transfer_files(self, keys: List[str]) -> dict:
        """
        Transfer multiple files from source to destination bucket.
        
        Args:
            keys: List of file keys to transfer
            
        Returns:
            dict: Summary of transfer results
        """
        results = {
            'successful': [],
            'failed': []
        }
        
        for key in keys:
            if self.transfer_file(key):
                results['successful'].append(key)
            else:
                results['failed'].append(key)
        
        logger.info(f"Transfer complete. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")
        return results
    
    def transfer_all_files(self, prefix: Optional[str] = None) -> dict:
        """
        Transfer all files from source to destination bucket.
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            dict: Summary of transfer results
        """
        keys = list_bucket_objects(self.source_bucket, prefix)
        logger.info(f"Found {len(keys)} files to transfer")
        return self.transfer_files(keys)
    
    def transfer_files_with_prefix(self, prefix: str) -> dict:
        """
        Transfer files with a specific prefix from source to destination bucket.
        
        Args:
            prefix: Prefix to filter files
            
        Returns:
            dict: Summary of transfer results
        """
        return self.transfer_all_files(prefix)

def main():
    """Main function to demonstrate usage."""
    try:
        transfer = S3Transfer()
        
        # Example: Transfer all files
        results = transfer.transfer_all_files()
        print(f"Transfer complete. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")
        
        # Example: Transfer specific files
        # results = transfer.transfer_files(['file1.txt', 'file2.txt'])
        
        # Example: Transfer files with prefix
        # results = transfer.transfer_files_with_prefix('data/')
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 