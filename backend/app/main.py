"""Main FastAPI application for philosophical AI companion."""

import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import check_db_connection, create_tables
from app.nlp import nlp_pipeline
from app.philosophy import PhilosophicalAIEngine
from app.api.routes import auth, chat, conversations, philosophy, wisdom, users

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting Philosophy Chat API...")
    
    try:
        # Check database connection
        if not await check_db_connection():
            logger.error("Failed to connect to database")
            raise Exception("Database connection failed")
        
        # Create tables if they don't exist
        await create_tables()
        
        # Initialize NLP pipeline
        await nlp_pipeline.initialize()
        
        # Initialize AI engine
        ai_engine = PhilosophicalAIEngine()
        await ai_engine.initialize()
        
        # Store in app state
        app.state.ai_engine = ai_engine
        
        logger.info("Philosophy Chat API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Philosophy Chat API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Advanced NLP backend for philosophical AI companion with multi-tradition support",
    version=settings.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Response:
    """Add response time header."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    """Log incoming requests."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} - {process_time:.3f}s - {request.url.path}"
    )
    
    return response


# Exception handlers
@app.exception_handler(500)
async def internal_server_error(request: Request, exc: Exception) -> JSONResponse:
    """Handle internal server errors."""
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred while processing your request."
        }
    )


@app.exception_handler(404)
async def not_found_error(request: Request, exc: Exception) -> JSONResponse:
    """Handle not found errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "detail": f"The requested resource was not found."
        }
    )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint."""
    db_healthy = await check_db_connection()
    nlp_healthy = nlp_pipeline._initialized
    
    return {
        "status": "healthy" if db_healthy and nlp_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "nlp_pipeline": "ready" if nlp_healthy else "not_ready",
        "version": settings.version,
        "environment": "development" if settings.debug else "production"
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check() -> dict:
    """Detailed health check with component status."""
    db_healthy = await check_db_connection()
    nlp_healthy = nlp_pipeline._initialized
    ai_engine_healthy = hasattr(app.state, 'ai_engine') and app.state.ai_engine._initialized
    
    return {
        "status": "healthy" if all([db_healthy, nlp_healthy, ai_engine_healthy]) else "unhealthy",
        "components": {
            "database": {
                "status": "healthy" if db_healthy else "unhealthy",
                "url": settings.database_url.split("@")[-1] if db_healthy else "unavailable"
            },
            "nlp_pipeline": {
                "status": "healthy" if nlp_healthy else "unhealthy",
                "models_loaded": nlp_healthy
            },
            "ai_engine": {
                "status": "healthy" if ai_engine_healthy else "unhealthy",
                "traditions_loaded": ai_engine_healthy
            }
        },
        "performance": {
            "max_concurrent_requests": settings.max_concurrent_requests,
            "request_timeout": settings.request_timeout,
            "ai_response_timeout": settings.ai_response_timeout
        },
        "version": settings.version,
        "environment": "development" if settings.debug else "production"
    }


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Philosophy Chat API",
        "description": "Advanced NLP backend for philosophical AI companion",
        "version": settings.version,
        "documentation": "/docs" if settings.debug else "Contact administrator",
        "health": "/health"
    }


# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(philosophy.router, prefix="/api/philosophy", tags=["Philosophy"])
app.include_router(wisdom.router, prefix="/api/wisdom", tags=["Wisdom"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )