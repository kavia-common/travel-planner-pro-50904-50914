from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


# Shared pagination schema
class PageMeta(BaseModel):
    total: int = Field(..., description="Total count of items available.")
    offset: int = Field(..., description="Offset used for the query.")
    limit: int = Field(..., description="Limit used for the query.")


class Page(BaseModel):
    items: list
    meta: PageMeta


# Trip Schemas
class TripBase(BaseModel):
    name: str = Field(..., description="Name of the trip.", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Description of the trip.")
    start_date: Optional[date] = Field(None, description="Trip start date.")
    end_date: Optional[date] = Field(None, description="Trip end date.")


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated trip name.", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Updated description.")
    start_date: Optional[date] = Field(None, description="Updated start date.")
    end_date: Optional[date] = Field(None, description="Updated end date.")


class TripOut(TripBase):
    id: int = Field(..., description="Trip identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")

    model_config = ConfigDict(from_attributes=True)


# Destination Schemas (DB-backed model exists, search is mock dataset)
class DestinationBase(BaseModel):
    name: str = Field(..., description="Destination name.", min_length=1, max_length=200)
    country: Optional[str] = Field(None, description="Country of the destination.")
    arrival_date: Optional[date] = Field(None, description="Arrival date.")
    departure_date: Optional[date] = Field(None, description="Departure date.")
    notes: Optional[str] = Field(None, description="Notes for the destination.")


class DestinationCreate(DestinationBase):
    trip_id: int = Field(..., description="Trip ID to attach this destination to.", ge=1)


class DestinationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Destination name.")
    country: Optional[str] = Field(None, description="Country.")
    arrival_date: Optional[date] = Field(None, description="Arrival date.")
    departure_date: Optional[date] = Field(None, description="Departure date.")
    notes: Optional[str] = Field(None, description="Notes.")


class DestinationOut(DestinationBase):
    id: int = Field(..., description="Destination identifier.")
    trip_id: int = Field(..., description="Trip identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")

    model_config = ConfigDict(from_attributes=True)


# Itinerary Item Schemas
class ItineraryItemBase(BaseModel):
    title: str = Field(..., description="Item title.", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Item description.")
    date: Optional[date] = Field(None, description="Date of the item.")
    start_time: Optional[str] = Field(None, description="Start time in HH:MM.")
    end_time: Optional[str] = Field(None, description="End time in HH:MM.")
    location: Optional[str] = Field(None, description="Location.")
    cost: Optional[float] = Field(None, description="Estimated cost.")
    destination_id: Optional[int] = Field(None, description="Related destination ID.", ge=1)


class ItineraryItemCreate(ItineraryItemBase):
    trip_id: int = Field(..., description="Trip ID to attach this itinerary item to.", ge=1)


class ItineraryItemUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Item title.")
    description: Optional[str] = Field(None, description="Item description.")
    date: Optional[date] = Field(None, description="Date of the item.")
    start_time: Optional[str] = Field(None, description="Start time.")
    end_time: Optional[str] = Field(None, description="End time.")
    location: Optional[str] = Field(None, description="Location.")
    cost: Optional[float] = Field(None, description="Estimated cost.")
    destination_id: Optional[int] = Field(None, description="Related destination ID.")
    trip_id: Optional[int] = Field(None, description="Trip ID.")


class ItineraryItemOut(ItineraryItemBase):
    id: int = Field(..., description="Itinerary item identifier.")
    trip_id: int = Field(..., description="Trip identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")

    model_config = ConfigDict(from_attributes=True)


# Accommodation Schemas
class AccommodationBase(BaseModel):
    name: str = Field(..., description="Name of the accommodation.", min_length=1, max_length=200)
    address: Optional[str] = Field(None, description="Address.")
    check_in: Optional[date] = Field(None, description="Check-in date.")
    check_out: Optional[date] = Field(None, description="Check-out date.")
    booking_ref: Optional[str] = Field(None, description="Booking reference.")
    notes: Optional[str] = Field(None, description="Notes.")


class AccommodationCreate(AccommodationBase):
    trip_id: int = Field(..., description="Trip ID to attach this accommodation to.", ge=1)


class AccommodationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Accommodation name.")
    address: Optional[str] = Field(None, description="Address.")
    check_in: Optional[date] = Field(None, description="Check-in date.")
    check_out: Optional[date] = Field(None, description="Check-out date.")
    booking_ref: Optional[str] = Field(None, description="Booking reference.")
    notes: Optional[str] = Field(None, description="Notes.")
    trip_id: Optional[int] = Field(None, description="Trip ID.")


class AccommodationOut(AccommodationBase):
    id: int = Field(..., description="Accommodation identifier.")
    trip_id: int = Field(..., description="Trip identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")

    model_config = ConfigDict(from_attributes=True)


# Transport Schemas
class TransportBase(BaseModel):
    type: str = Field(..., description="Transport type (flight, train, car, etc.)", min_length=1, max_length=100)
    provider: Optional[str] = Field(None, description="Transport provider.")
    departure_location: Optional[str] = Field(None, description="Departure location.")
    arrival_location: Optional[str] = Field(None, description="Arrival location.")
    departure_date: Optional[date] = Field(None, description="Departure date.")
    arrival_date: Optional[date] = Field(None, description="Arrival date.")
    booking_ref: Optional[str] = Field(None, description="Booking reference.")
    notes: Optional[str] = Field(None, description="Notes.")


class TransportCreate(TransportBase):
    trip_id: int = Field(..., description="Trip ID to attach this transport to.", ge=1)


class TransportUpdate(BaseModel):
    type: Optional[str] = Field(None, description="Transport type.")
    provider: Optional[str] = Field(None, description="Transport provider.")
    departure_location: Optional[str] = Field(None, description="Departure location.")
    arrival_location: Optional[str] = Field(None, description="Arrival location.")
    departure_date: Optional[date] = Field(None, description="Departure date.")
    arrival_date: Optional[date] = Field(None, description="Arrival date.")
    booking_ref: Optional[str] = Field(None, description="Booking reference.")
    notes: Optional[str] = Field(None, description="Notes.")
    trip_id: Optional[int] = Field(None, description="Trip ID.")


class TransportOut(TransportBase):
    id: int = Field(..., description="Transport identifier.")
    trip_id: int = Field(..., description="Trip identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")

    model_config = ConfigDict(from_attributes=True)


# Note Schemas
class NoteBase(BaseModel):
    title: str = Field(..., description="Note title.", min_length=1, max_length=200)
    content: Optional[str] = Field(None, description="Note content.")


class NoteCreate(NoteBase):
    trip_id: int = Field(..., description="Trip ID to attach this note to.", ge=1)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Note title.")
    content: Optional[str] = Field(None, description="Note content.")
    trip_id: Optional[int] = Field(None, description="Trip ID.")


class NoteOut(NoteBase):
    id: int = Field(..., description="Note identifier.")
    trip_id: int = Field(..., description="Trip identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")

    model_config = ConfigDict(from_attributes=True)


# Mock Destination Search Schemas
class DestinationSearchResult(BaseModel):
    name: str = Field(..., description="Destination name.")
    country: str = Field(..., description="Country.")
    region: Optional[str] = Field(None, description="Region/state.")
    iata: Optional[str] = Field(None, description="IATA code for airports (if applicable).")


class DestinationSearchResults(BaseModel):
    results: List[DestinationSearchResult]
    total: int = Field(..., description="Total results found.")
