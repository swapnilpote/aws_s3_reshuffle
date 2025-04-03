# AWS S3 File Download API

A FastAPI-based REST API for downloading files from AWS S3 buckets based on lane ID and hour, with MongoDB integration for file tracking.

## Features

- REST API endpoints for S3 file downloads
- Download files from AWS S3 buckets
- MongoDB integration for file tracking
- Progress tracking and comprehensive logging
- Environment variable configuration
- Error handling and retries
- Support for large files
- OpenAPI documentation
- Health check endpoint

## Prerequisites

- Python 3.8 or higher
- AWS credentials configured (either through AWS CLI or environment variables)
- MongoDB instance
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

2. Update the `.env` file with your credentials and settings:
```
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
SOURCE_BUCKET=your-source-bucket-name

# MongoDB Settings
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=s3_files
MONGODB_COLLECTION=file_records

# Download Settings
DOWNLOAD_PATH=./downloads
```

## Running the API

Start the API server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```
GET /api/v1/health
```
Returns the health status of the API.

### Download Files
```
POST /api/v1/download
```
Request body:
```json
{
    "lane_id": "lane1",
    "hour": 14,
    "date": "2024-02-14T00:00:00Z"
}
```

The API will:
1. Query MongoDB for files matching the lane ID and hour
2. Download matching files to the local filesystem
3. Update file status in MongoDB
4. Return download results

## File Organization

Downloaded files are organized in the following structure:
```
downloads/
└── {lane_id}/
    └── {year}/
        └── {month}/
            └── {day}/
                └── {hour}/
                    └── {filename}
```

## Best Practices Implemented

1. **API Design**: RESTful API design with proper request/response models
2. **Error Handling**: Comprehensive error handling with proper HTTP status codes
3. **Logging**: Detailed logging using loguru for better debugging
4. **Configuration Management**: Environment variable based configuration
5. **Security**: Secure credential management and CORS configuration
6. **Modularity**: Well-structured, modular code design
7. **Documentation**: OpenAPI documentation with Swagger UI and ReDoc
8. **Type Safety**: Pydantic models for request/response validation
9. **Dependency Injection**: FastAPI dependency injection for services
10. **Database Integration**: MongoDB integration for file tracking
11. **File Organization**: Structured local file storage

## License

MIT License 