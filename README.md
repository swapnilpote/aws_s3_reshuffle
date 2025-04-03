# AWS S3 File Transfer Tool

A Python utility for transferring files between AWS S3 buckets with best practices and robust error handling.

## Features

- Transfer files between AWS S3 buckets
- Progress bar for transfer monitoring
- Comprehensive logging
- Environment variable configuration
- Error handling and retries
- Support for large files

## Prerequisites

- Python 3.8 or higher
- AWS credentials configured (either through AWS CLI or environment variables)
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update the `.env` file with your AWS credentials and bucket information:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
SOURCE_BUCKET=source-bucket-name
DESTINATION_BUCKET=destination-bucket-name
```

## Usage

```python
from s3_transfer import S3Transfer

# Initialize the transfer utility
transfer = S3Transfer()

# Transfer all files from source to destination bucket
transfer.transfer_all_files()

# Transfer specific files
transfer.transfer_files(['file1.txt', 'file2.txt'])

# Transfer files with specific prefix
transfer.transfer_files_with_prefix('data/')
```

## Best Practices Implemented

1. **Error Handling**: Comprehensive error handling with retries for transient failures
2. **Logging**: Detailed logging using loguru for better debugging
3. **Progress Tracking**: Visual progress bars for long-running transfers
4. **Configuration Management**: Environment variable based configuration
5. **Security**: Secure credential management
6. **Modularity**: Well-structured, modular code design
7. **Documentation**: Comprehensive documentation and type hints

## License

MIT License 