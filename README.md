# travel-planner-pro-50904-50914

Backend (FastAPI) now includes REST endpoints for:
- Trips (CRUD, pagination)
- Destinations (CRUD, pagination) + mock search at GET /destinations/search?q=...
- Itinerary items (CRUD, pagination)
- Accommodations (CRUD, pagination)
- Transport (CRUD, pagination)
- Notes (CRUD, pagination)

Quick start (backend):
1) cd travel_planner_backend
2) (optional) copy .env.example to .env and adjust:
   - TRAVEL_PLANNER_DB_URL (default is sqlite:///./travel_planner.db)
3) Install dependencies (if not already): pip install -r requirements.txt
4) Start: uvicorn src.api.main:app --host 0.0.0.0 --port 3001
5) Health check: GET http://localhost:3001/ should return {"message":"Healthy"}
6) Swagger docs: http://localhost:3001/docs

Environment:
- TRAVEL_PLANNER_DB_URL optional (defaults to sqlite:///./travel_planner.db)

CORS:
- Configured open to all origins for development (allow_origins=["*"]). For production, restrict to the frontend URL (e.g., http://localhost:3000).

Regenerate OpenAPI JSON:
- From backend root (travel_planner_backend): python -m src.api.generate_openapi
- Output is saved to interfaces/openapi.json