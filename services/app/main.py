"""Main FastAPI application."""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from app.config import get_settings
from app.routers import seasons, tournaments, players, decks, matches, statistics, tournament_types

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## MTG Tournament Tracker API
    
    RESTful API for tracking Magic the Gathering tournament matches, including:
    - **Best-of-3 match tracking** with individual game results
    - **Player statistics** (wins, draws, losses, win rates)
    - **Deck archetype analysis** (performance metrics)
    - **Matchup statistics** (deck vs deck win rates)
    - **Batch operations** for efficient data entry
    
    ### Features
    - Complete CRUD operations for all entities
    - Dedicated statistics endpoints using optimized database views
    - Batch match insertion with transaction support
    - Automatic API documentation (you're reading it!)
    
    ### Database Schema
    - **Seasons** → **Tournaments** → **Matches** → **Games**
    - **Players** and **Deck Archetypes** used in matches
    - Materialized views for statistics calculations
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
origins = settings.cors_origins.split(",") if settings.cors_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(seasons.router, prefix="/api/v1")
app.include_router(tournaments.router, prefix="/api/v1")
app.include_router(tournament_types.router, prefix="/api/v1")
app.include_router(players.router, prefix="/api/v1")
app.include_router(decks.router, prefix="/api/v1")
app.include_router(matches.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")


# Exception handlers

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": "Invalid input data",
            "errors": errors
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (foreign keys, unique constraints)."""
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Determine specific error type
    if "foreign key" in error_msg.lower():
        detail = "Referenced resource does not exist"
    elif "unique" in error_msg.lower():
        detail = "Resource with this value already exists"
    elif "check" in error_msg.lower():
        detail = "Data violates database constraints"
    else:
        detail = "Database integrity error"
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Integrity Error",
            "detail": detail,
            "database_error": error_msg if settings.debug else None
        }
    )


@app.exception_handler(OperationalError)
async def operational_exception_handler(request: Request, exc: OperationalError):
    """Handle database operational errors (connection issues)."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service Unavailable",
            "detail": "Database connection error. Please try again later."
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "exception": str(exc) if settings.debug else None
        }
    )


# Health check endpoint

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the API status and version.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug
    )
