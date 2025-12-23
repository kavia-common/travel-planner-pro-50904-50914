"""
SQLAlchemy ORM models for the Travel Planner backend.

Entities:
- Trip: Represents a travel plan.
- Destination: A place associated with a trip.
- ItineraryItem: Items on the itinerary (activities, events).
- Accommodation: Lodging details for a trip.
- Transport: Transportation details related to a trip.
- Note: General notes for a trip.

All models include created_at and updated_at timestamps where applicable.
"""
from __future__ import annotations

from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import (
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.api.db import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    destinations: Mapped[List["Destination"]] = relationship("Destination", back_populates="trip", cascade="all, delete-orphan")
    itinerary_items: Mapped[List["ItineraryItem"]] = relationship("ItineraryItem", back_populates="trip", cascade="all, delete-orphan")
    accommodations: Mapped[List["Accommodation"]] = relationship("Accommodation", back_populates="trip", cascade="all, delete-orphan")
    transports: Mapped[List["Transport"]] = relationship("Transport", back_populates="trip", cascade="all, delete-orphan")
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="trip", cascade="all, delete-orphan")


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    arrival_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    departure_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="destinations")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), index=True, nullable=False)
    destination_id: Mapped[Optional[int]] = mapped_column(ForeignKey("destinations.id", ondelete="SET NULL"), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    start_time: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # store as HH:MM (local)
    end_time: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="itinerary_items")
    destination: Mapped[Optional["Destination"]] = relationship("Destination")


class Accommodation(Base):
    __tablename__ = "accommodations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    check_in: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    check_out: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    booking_ref: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="accommodations")


class Transport(Base):
    __tablename__ = "transports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)  # flight, train, car, bus, etc.
    provider: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    departure_location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    arrival_location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    departure_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    arrival_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    booking_ref: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="transports")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="notes")
