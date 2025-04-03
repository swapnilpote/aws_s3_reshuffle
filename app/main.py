from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.api.endpoints import router

# Configure logging
logger.add(
    "s3_transfer.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Log startup event."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown event."""
    logger.info(f"Shutting down {settings.PROJECT_NAME}") 