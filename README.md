# travel-planner-pro-50904-50914

Backend (FastAPI) now includes REST endpoints for:
- Trips (CRUD, pagination)
- Destinations (CRUD, pagination) + mock search at GET /destinations/search?q=...
- Itinerary items (CRUD, pagination)
- Accommodations (CRUD, pagination)
- Transport (CRUD, pagination)
- Notes (CRUD, pagination)

Run backend (defaults to SQLite file db):
- Env: TRAVEL_PLANNER_DB_URL optional (defaults to sqlite:///./travel_planner.db)
- Start: uvicorn src.api.main:app --host 0.0.0.0 --port 3001

Regenerate OpenAPI JSON:
- From backend root (travel_planner_backend): python -m src.api.generate_openapi
- Output is saved to interfaces/openapi.json