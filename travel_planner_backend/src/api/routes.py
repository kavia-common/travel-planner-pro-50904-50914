from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.db import get_db
from src.api.schemas import (
    TripCreate,
    TripUpdate,
    TripOut,
    DestinationCreate,
    DestinationUpdate,
    DestinationOut,
    ItineraryItemCreate,
    ItineraryItemUpdate,
    ItineraryItemOut,
    AccommodationCreate,
    AccommodationUpdate,
    AccommodationOut,
    TransportCreate,
    TransportUpdate,
    TransportOut,
    NoteCreate,
    NoteUpdate,
    NoteOut,
    DestinationSearchResults,
    DestinationSearchResult,
    PageMeta,
)
from src.api import services

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/trips", response_model=dict, tags=["Trips"], summary="List trips", description="List trips with pagination support.")
def list_trips(
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Limit for pagination"),
):
    """List trips with pagination."""
    items, total = services.list_trips(db, offset, limit)
    return {"items": [TripOut.model_validate(i) for i in items], "meta": PageMeta(total=total, offset=offset, limit=limit)}


# PUBLIC_INTERFACE
@router.post("/trips", response_model=TripOut, status_code=status.HTTP_201_CREATED, tags=["Trips"], summary="Create trip", description="Create a new trip.")
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    """Create a trip."""
    trip = services.create_trip(db, payload.model_dump())
    return TripOut.model_validate(trip)


# PUBLIC_INTERFACE
@router.get("/trips/{trip_id}", response_model=TripOut, tags=["Trips"], summary="Get trip", description="Retrieve a trip by ID.")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = services.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripOut.model_validate(trip)


# PUBLIC_INTERFACE
@router.put("/trips/{trip_id}", response_model=TripOut, tags=["Trips"], summary="Update trip", description="Update a trip by ID.")
def update_trip(trip_id: int, payload: TripUpdate, db: Session = Depends(get_db)):
    trip = services.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    updated = services.update_trip(db, trip, payload.model_dump(exclude_unset=True))
    return TripOut.model_validate(updated)


# PUBLIC_INTERFACE
@router.delete("/trips/{trip_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Trips"], summary="Delete trip", description="Delete a trip by ID.")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = services.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    services.delete_trip(db, trip)
    return None


# Destination CRUD (database-backed)
# PUBLIC_INTERFACE
@router.get("/destinations", response_model=dict, tags=["Destinations"], summary="List destinations", description="List destinations with pagination and optional filtering by trip_id.")
def list_destinations(
    db: Session = Depends(get_db),
    trip_id: Optional[int] = Query(None, description="Filter by trip id"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Limit for pagination"),
):
    items, total = services.list_destinations(db, trip_id, offset, limit)
    return {"items": [DestinationOut.model_validate(i) for i in items], "meta": PageMeta(total=total, offset=offset, limit=limit)}


# PUBLIC_INTERFACE
@router.post("/destinations", response_model=DestinationOut, status_code=status.HTTP_201_CREATED, tags=["Destinations"], summary="Create destination", description="Create a destination for a trip.")
def create_destination(payload: DestinationCreate, db: Session = Depends(get_db)):
    # ensure trip exists
    trip = services.get_trip(db, payload.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    dest = services.create_destination(db, payload.model_dump())
    return DestinationOut.model_validate(dest)


# PUBLIC_INTERFACE
@router.get("/destinations/{destination_id}", response_model=DestinationOut, tags=["Destinations"], summary="Get destination", description="Retrieve a destination by ID.")
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    dest = services.get_destination(db, destination_id)
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    return DestinationOut.model_validate(dest)


# PUBLIC_INTERFACE
@router.put("/destinations/{destination_id}", response_model=DestinationOut, tags=["Destinations"], summary="Update destination", description="Update a destination by ID.")
def update_destination(destination_id: int, payload: DestinationUpdate, db: Session = Depends(get_db)):
    dest = services.get_destination(db, destination_id)
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    updated = services.update_destination(db, dest, payload.model_dump(exclude_unset=True))
    return DestinationOut.model_validate(updated)


# PUBLIC_INTERFACE
@router.delete("/destinations/{destination_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Destinations"], summary="Delete destination", description="Delete a destination by ID.")
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    dest = services.get_destination(db, destination_id)
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    services.delete_destination(db, dest)
    return None


# Itinerary Items
# PUBLIC_INTERFACE
@router.get("/itinerary", response_model=dict, tags=["Itinerary"], summary="List itinerary items", description="List itinerary items with pagination and optional filtering by trip_id or destination_id.")
def list_itinerary(
    db: Session = Depends(get_db),
    trip_id: Optional[int] = Query(None, description="Filter by trip id"),
    destination_id: Optional[int] = Query(None, description="Filter by destination id"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Limit for pagination"),
):
    items, total = services.list_itinerary_items(db, trip_id, destination_id, offset, limit)
    return {"items": [ItineraryItemOut.model_validate(i) for i in items], "meta": PageMeta(total=total, offset=offset, limit=limit)}


# PUBLIC_INTERFACE
@router.post("/itinerary", response_model=ItineraryItemOut, status_code=status.HTTP_201_CREATED, tags=["Itinerary"], summary="Create itinerary item", description="Create a new itinerary item for a trip.")
def create_itinerary(payload: ItineraryItemCreate, db: Session = Depends(get_db)):
    if not services.get_trip(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    if payload.destination_id and not services.get_destination(db, payload.destination_id):
        raise HTTPException(status_code=404, detail="Destination not found")
    item = services.create_itinerary_item(db, payload.model_dump())
    return ItineraryItemOut.model_validate(item)


# PUBLIC_INTERFACE
@router.get("/itinerary/{item_id}", response_model=ItineraryItemOut, tags=["Itinerary"], summary="Get itinerary item", description="Retrieve an itinerary item by ID.")
def get_itinerary(item_id: int, db: Session = Depends(get_db)):
    item = services.get_itinerary_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")
    return ItineraryItemOut.model_validate(item)


# PUBLIC_INTERFACE
@router.put("/itinerary/{item_id}", response_model=ItineraryItemOut, tags=["Itinerary"], summary="Update itinerary item", description="Update an itinerary item by ID.")
def update_itinerary(item_id: int, payload: ItineraryItemUpdate, db: Session = Depends(get_db)):
    item = services.get_itinerary_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")
    data = payload.model_dump(exclude_unset=True)
    if "trip_id" in data and data["trip_id"] and not services.get_trip(db, data["trip_id"]):
        raise HTTPException(status_code=404, detail="Trip not found")
    if "destination_id" in data and data["destination_id"] and not services.get_destination(db, data["destination_id"]):
        raise HTTPException(status_code=404, detail="Destination not found")
    updated = services.update_itinerary_item(db, item, data)
    return ItineraryItemOut.model_validate(updated)


# PUBLIC_INTERFACE
@router.delete("/itinerary/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Itinerary"], summary="Delete itinerary item", description="Delete an itinerary item by ID.")
def delete_itinerary(item_id: int, db: Session = Depends(get_db)):
    item = services.get_itinerary_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")
    services.delete_itinerary_item(db, item)
    return None


# Accommodations
# PUBLIC_INTERFACE
@router.get("/accommodations", response_model=dict, tags=["Accommodations"], summary="List accommodations", description="List accommodations with pagination and optional filtering by trip_id.")
def list_accommodations(
    db: Session = Depends(get_db),
    trip_id: Optional[int] = Query(None, description="Filter by trip id"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Limit for pagination"),
):
    items, total = services.list_accommodations(db, trip_id, offset, limit)
    return {"items": [AccommodationOut.model_validate(i) for i in items], "meta": PageMeta(total=total, offset=offset, limit=limit)}


# PUBLIC_INTERFACE
@router.post("/accommodations", response_model=AccommodationOut, status_code=status.HTTP_201_CREATED, tags=["Accommodations"], summary="Create accommodation", description="Create a new accommodation for a trip.")
def create_accommodation(payload: AccommodationCreate, db: Session = Depends(get_db)):
    if not services.get_trip(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    acc = services.create_accommodation(db, payload.model_dump())
    return AccommodationOut.model_validate(acc)


# PUBLIC_INTERFACE
@router.get("/accommodations/{acc_id}", response_model=AccommodationOut, tags=["Accommodations"], summary="Get accommodation", description="Retrieve an accommodation by ID.")
def get_accommodation(acc_id: int, db: Session = Depends(get_db)):
    acc = services.get_accommodation(db, acc_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return AccommodationOut.model_validate(acc)


# PUBLIC_INTERFACE
@router.put("/accommodations/{acc_id}", response_model=AccommodationOut, tags=["Accommodations"], summary="Update accommodation", description="Update an accommodation by ID.")
def update_accommodation(acc_id: int, payload: AccommodationUpdate, db: Session = Depends(get_db)):
    acc = services.get_accommodation(db, acc_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    data = payload.model_dump(exclude_unset=True)
    if "trip_id" in data and data["trip_id"] and not services.get_trip(db, data["trip_id"]):
        raise HTTPException(status_code=404, detail="Trip not found")
    updated = services.update_accommodation(db, acc, data)
    return AccommodationOut.model_validate(updated)


# PUBLIC_INTERFACE
@router.delete("/accommodations/{acc_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Accommodations"], summary="Delete accommodation", description="Delete an accommodation by ID.")
def delete_accommodation(acc_id: int, db: Session = Depends(get_db)):
    acc = services.get_accommodation(db, acc_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    services.delete_accommodation(db, acc)
    return None


# Transport
# PUBLIC_INTERFACE
@router.get("/transport", response_model=dict, tags=["Transport"], summary="List transport items", description="List transport items with pagination and optional filtering by trip_id.")
def list_transport(
    db: Session = Depends(get_db),
    trip_id: Optional[int] = Query(None, description="Filter by trip id"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Limit for pagination"),
):
    items, total = services.list_transport(db, trip_id, offset, limit)
    return {"items": [TransportOut.model_validate(i) for i in items], "meta": PageMeta(total=total, offset=offset, limit=limit)}


# PUBLIC_INTERFACE
@router.post("/transport", response_model=TransportOut, status_code=status.HTTP_201_CREATED, tags=["Transport"], summary="Create transport", description="Create a new transport entry for a trip.")
def create_transport(payload: TransportCreate, db: Session = Depends(get_db)):
    if not services.get_trip(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    t = services.create_transport(db, payload.model_dump())
    return TransportOut.model_validate(t)


# PUBLIC_INTERFACE
@router.get("/transport/{transport_id}", response_model=TransportOut, tags=["Transport"], summary="Get transport", description="Retrieve a transport entry by ID.")
def get_transport(transport_id: int, db: Session = Depends(get_db)):
    t = services.get_transport(db, transport_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transport not found")
    return TransportOut.model_validate(t)


# PUBLIC_INTERFACE
@router.put("/transport/{transport_id}", response_model=TransportOut, tags=["Transport"], summary="Update transport", description="Update a transport entry by ID.")
def update_transport(transport_id: int, payload: TransportUpdate, db: Session = Depends(get_db)):
    t = services.get_transport(db, transport_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transport not found")
    data = payload.model_dump(exclude_unset=True)
    if "trip_id" in data and data["trip_id"] and not services.get_trip(db, data["trip_id"]):
        raise HTTPException(status_code=404, detail="Trip not found")
    updated = services.update_transport(db, t, data)
    return TransportOut.model_validate(updated)


# PUBLIC_INTERFACE
@router.delete("/transport/{transport_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Transport"], summary="Delete transport", description="Delete a transport entry by ID.")
def delete_transport(transport_id: int, db: Session = Depends(get_db)):
    t = services.get_transport(db, transport_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transport not found")
    services.delete_transport(db, t)
    return None


# Notes
# PUBLIC_INTERFACE
@router.get("/notes", response_model=dict, tags=["Notes"], summary="List notes", description="List notes with pagination and optional filtering by trip_id.")
def list_notes(
    db: Session = Depends(get_db),
    trip_id: Optional[int] = Query(None, description="Filter by trip id"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(25, ge=1, le=100, description="Limit for pagination"),
):
    items, total = services.list_notes(db, trip_id, offset, limit)
    return {"items": [NoteOut.model_validate(i) for i in items], "meta": PageMeta(total=total, offset=offset, limit=limit)}


# PUBLIC_INTERFACE
@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED, tags=["Notes"], summary="Create note", description="Create a new note for a trip.")
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    if not services.get_trip(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    n = services.create_note(db, payload.model_dump())
    return NoteOut.model_validate(n)


# PUBLIC_INTERFACE
@router.get("/notes/{note_id}", response_model=NoteOut, tags=["Notes"], summary="Get note", description="Retrieve a note by ID.")
def get_note(note_id: int, db: Session = Depends(get_db)):
    n = services.get_note(db, note_id)
    if not n:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut.model_validate(n)


# PUBLIC_INTERFACE
@router.put("/notes/{note_id}", response_model=NoteOut, tags=["Notes"], summary="Update note", description="Update a note by ID.")
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    n = services.get_note(db, note_id)
    if not n:
        raise HTTPException(status_code=404, detail="Note not found")
    data = payload.model_dump(exclude_unset=True)
    if "trip_id" in data and data["trip_id"] and not services.get_trip(db, data["trip_id"]):
        raise HTTPException(status_code=404, detail="Trip not found")
    updated = services.update_note(db, n, data)
    return NoteOut.model_validate(updated)


# PUBLIC_INTERFACE
@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notes"], summary="Delete note", description="Delete a note by ID.")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    n = services.get_note(db, note_id)
    if not n:
        raise HTTPException(status_code=404, detail="Note not found")
    services.delete_note(db, n)
    return None


# Mock destination search endpoint
MOCK_DESTINATIONS = [
    {"name": "Paris", "country": "France", "region": "Île-de-France", "iata": "CDG"},
    {"name": "Lyon", "country": "France", "region": "Auvergne-Rhône-Alpes", "iata": None},
    {"name": "New York", "country": "USA", "region": "NY", "iata": "JFK"},
    {"name": "San Francisco", "country": "USA", "region": "CA", "iata": "SFO"},
    {"name": "Tokyo", "country": "Japan", "region": "Kanto", "iata": "HND"},
    {"name": "Kyoto", "country": "Japan", "region": "Kansai", "iata": None},
]


# PUBLIC_INTERFACE
@router.get(
    "/destinations/search",
    response_model=DestinationSearchResults,
    tags=["Destinations"],
    summary="Search destinations (mock)",
    description="Search destinations using a mock dataset by query string and optional country.",
)
def search_destinations(q: str = Query(..., min_length=1, description="Search query"), country: Optional[str] = Query(None, description="Country filter")):
    q_lower = q.lower()
    filtered = [
        d
        for d in MOCK_DESTINATIONS
        if (q_lower in d["name"].lower() or (d["iata"] and q_lower in d["iata"].lower()))
        and (country.lower() in d["country"].lower() if country else True)
    ]
    results = [DestinationSearchResult(**d) for d in filtered]
    return DestinationSearchResults(results=results, total=len(results))
