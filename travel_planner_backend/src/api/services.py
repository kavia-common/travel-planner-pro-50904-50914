from __future__ import annotations

from typing import Optional, Tuple, Sequence, List

from sqlalchemy.orm import Session, Query

from src.api import models


def _paginate(q: Query, offset: int, limit: int) -> Tuple[Sequence, int]:
    """
    Internal helper to apply pagination to a SQLAlchemy query.
    Returns the items and total count.
    """
    total = q.count()
    items = q.offset(offset).limit(limit).all()
    return items, total


# PUBLIC_INTERFACE
def list_trips(db: Session, offset: int, limit: int) -> Tuple[List[models.Trip], int]:
    """Return a paginated list of trips ordered by created_at desc."""
    q = db.query(models.Trip).order_by(models.Trip.created_at.desc())
    return _paginate(q, offset, limit)


# PUBLIC_INTERFACE
def create_trip(db: Session, data: dict) -> models.Trip:
    """Create and persist a trip."""
    trip = models.Trip(**data)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


# PUBLIC_INTERFACE
def get_trip(db: Session, trip_id: int) -> Optional[models.Trip]:
    """Get a trip by id."""
    return db.get(models.Trip, trip_id)


# PUBLIC_INTERFACE
def update_trip(db: Session, trip: models.Trip, data: dict) -> models.Trip:
    """Update a trip instance with provided data."""
    for k, v in data.items():
        setattr(trip, k, v)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


# PUBLIC_INTERFACE
def delete_trip(db: Session, trip: models.Trip) -> None:
    """Delete a trip."""
    db.delete(trip)
    db.commit()


# Destinations
# PUBLIC_INTERFACE
def list_destinations(db: Session, trip_id: Optional[int], offset: int, limit: int) -> Tuple[List[models.Destination], int]:
    """Paginated destinations; optional filter by trip_id."""
    q = db.query(models.Destination).order_by(models.Destination.created_at.desc())
    if trip_id:
        q = q.filter(models.Destination.trip_id == trip_id)
    return _paginate(q, offset, limit)


# PUBLIC_INTERFACE
def create_destination(db: Session, data: dict) -> models.Destination:
    """Create a destination. Trip must exist (validate externally)."""
    dest = models.Destination(**data)
    db.add(dest)
    db.commit()
    db.refresh(dest)
    return dest


# PUBLIC_INTERFACE
def get_destination(db: Session, destination_id: int) -> Optional[models.Destination]:
    """Get destination by id."""
    return db.get(models.Destination, destination_id)


# PUBLIC_INTERFACE
def update_destination(db: Session, dest: models.Destination, data: dict) -> models.Destination:
    """Update destination."""
    for k, v in data.items():
        setattr(dest, k, v)
    db.add(dest)
    db.commit()
    db.refresh(dest)
    return dest


# PUBLIC_INTERFACE
def delete_destination(db: Session, dest: models.Destination) -> None:
    """Delete destination."""
    db.delete(dest)
    db.commit()


# Itinerary
# PUBLIC_INTERFACE
def list_itinerary_items(
    db: Session,
    trip_id: Optional[int],
    destination_id: Optional[int],
    offset: int,
    limit: int,
) -> Tuple[List[models.ItineraryItem], int]:
    """Paginated itinerary items; optional filter by trip_id / destination_id."""
    q = db.query(models.ItineraryItem).order_by(models.ItineraryItem.created_at.desc())
    if trip_id:
        q = q.filter(models.ItineraryItem.trip_id == trip_id)
    if destination_id:
        q = q.filter(models.ItineraryItem.destination_id == destination_id)
    return _paginate(q, offset, limit)


# PUBLIC_INTERFACE
def create_itinerary_item(db: Session, data: dict) -> models.ItineraryItem:
    """Create itinerary item."""
    item = models.ItineraryItem(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# PUBLIC_INTERFACE
def get_itinerary_item(db: Session, item_id: int) -> Optional[models.ItineraryItem]:
    """Get itinerary item by id."""
    return db.get(models.ItineraryItem, item_id)


# PUBLIC_INTERFACE
def update_itinerary_item(db: Session, item: models.ItineraryItem, data: dict) -> models.ItineraryItem:
    """Update itinerary item."""
    for k, v in data.items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# PUBLIC_INTERFACE
def delete_itinerary_item(db: Session, item: models.ItineraryItem) -> None:
    """Delete itinerary item."""
    db.delete(item)
    db.commit()


# Accommodations
# PUBLIC_INTERFACE
def list_accommodations(db: Session, trip_id: Optional[int], offset: int, limit: int) -> Tuple[List[models.Accommodation], int]:
    """Paginated accommodations; optional filter by trip_id."""
    q = db.query(models.Accommodation).order_by(models.Accommodation.created_at.desc())
    if trip_id:
        q = q.filter(models.Accommodation.trip_id == trip_id)
    return _paginate(q, offset, limit)


# PUBLIC_INTERFACE
def create_accommodation(db: Session, data: dict) -> models.Accommodation:
    """Create accommodation."""
    acc = models.Accommodation(**data)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc


# PUBLIC_INTERFACE
def get_accommodation(db: Session, acc_id: int) -> Optional[models.Accommodation]:
    """Get accommodation by id."""
    return db.get(models.Accommodation, acc_id)


# PUBLIC_INTERFACE
def update_accommodation(db: Session, acc: models.Accommodation, data: dict) -> models.Accommodation:
    """Update accommodation."""
    for k, v in data.items():
        setattr(acc, k, v)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc


# PUBLIC_INTERFACE
def delete_accommodation(db: Session, acc: models.Accommodation) -> None:
    """Delete accommodation."""
    db.delete(acc)
    db.commit()


# Transport
# PUBLIC_INTERFACE
def list_transport(db: Session, trip_id: Optional[int], offset: int, limit: int) -> Tuple[List[models.Transport], int]:
    """Paginated transport; optional filter by trip_id."""
    q = db.query(models.Transport).order_by(models.Transport.created_at.desc())
    if trip_id:
        q = q.filter(models.Transport.trip_id == trip_id)
    return _paginate(q, offset, limit)


# PUBLIC_INTERFACE
def create_transport(db: Session, data: dict) -> models.Transport:
    """Create transport."""
    t = models.Transport(**data)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


# PUBLIC_INTERFACE
def get_transport(db: Session, transport_id: int) -> Optional[models.Transport]:
    """Get transport by id."""
    return db.get(models.Transport, transport_id)


# PUBLIC_INTERFACE
def update_transport(db: Session, transport: models.Transport, data: dict) -> models.Transport:
    """Update transport."""
    for k, v in data.items():
        setattr(transport, k, v)
    db.add(transport)
    db.commit()
    db.refresh(transport)
    return transport


# PUBLIC_INTERFACE
def delete_transport(db: Session, transport: models.Transport) -> None:
    """Delete transport."""
    db.delete(transport)
    db.commit()


# Notes
# PUBLIC_INTERFACE
def list_notes(db: Session, trip_id: Optional[int], offset: int, limit: int) -> Tuple[List[models.Note], int]:
    """Paginated notes; optional filter by trip_id."""
    q = db.query(models.Note).order_by(models.Note.created_at.desc())
    if trip_id:
        q = q.filter(models.Note.trip_id == trip_id)
    return _paginate(q, offset, limit)


# PUBLIC_INTERFACE
def create_note(db: Session, data: dict) -> models.Note:
    """Create note."""
    n = models.Note(**data)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


# PUBLIC_INTERFACE
def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    """Get note by id."""
    return db.get(models.Note, note_id)


# PUBLIC_INTERFACE
def update_note(db: Session, note: models.Note, data: dict) -> models.Note:
    """Update note."""
    for k, v in data.items():
        setattr(note, k, v)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
def delete_note(db: Session, note: models.Note) -> None:
    """Delete note."""
    db.delete(note)
    db.commit()
