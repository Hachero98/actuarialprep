"""
FastAPI application factory for ActuarialPrep backend.

This module sets up the FastAPI application with all routes, middleware,
and startup/shutdown events.
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.core.database import engine
from app.models import Base  # use the models' Base so all tables are discovered
from app.api import auth, questions, adaptive, analytics, study_plan, video_lessons, admin
from app.api import question_set, tutor
from app.api.video_lessons import api_router as video_api_router
from app.api import v1_video

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.

    Startup:
        - Initialize database tables

    Shutdown:
        - Close database connections
    """
    # Startup
    logger.info("Initializing database...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down...")
    await engine.dispose()
    logger.info("Database connections closed")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Adaptive actuarial exam preparation platform",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router)
    app.include_router(questions.router)
    app.include_router(adaptive.router)
    app.include_router(analytics.router)
    app.include_router(study_plan.router)
    app.include_router(video_lessons.router)
    app.include_router(admin.router)
    app.include_router(question_set.router)
    app.include_router(tutor.router)
    app.include_router(video_api_router)   # GET /api/get-contextual-video
    app.include_router(v1_video.router)   # GET /api/v1/contextual-video, /api/v1/contextual-content

    # Health check endpoint
    @app.get(
        "/health",
        status_code=status.HTTP_200_OK,
        tags=["health"],
        summary="Health check",
    )
    async def health_check() -> dict:
        """
        Health check endpoint.

        Returns:
            Status information
        """
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
        }

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
