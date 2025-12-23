from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.db import init_db
from src.api.routes import router as api_router

openapi_tags = [
    {"name": "Health", "description": "Health checks and service status."},
    {"name": "Trips", "description": "Trip management endpoints."},
    {"name": "Destinations", "description": "Destination management endpoints."},
    {"name": "Itinerary", "description": "Itinerary item management endpoints."},
    {"name": "Accommodations", "description": "Accommodation management endpoints."},
    {"name": "Transport", "description": "Transport management endpoints."},
    {"name": "Notes", "description": "Notes management endpoints."},
]

app = FastAPI(
    title="Travel Planner Backend",
    description="FastAPI backend for the Travel Planner app with SQLite persistence via SQLAlchemy.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Keep existing CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on service startup if they do not exist."""
    init_db()


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check", operation_id="health_check_root_get")
def health_check():
    """Health check endpoint.

    Returns:
        dict: Simple status message indicating the service is healthy.
    """
    return {"message": "Healthy"}


# Include API routes
app.include_router(api_router)
