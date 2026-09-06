from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from .database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True, nullable=False)
    client_name = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    cargo_type = Column(String, nullable=False)
    weight_kg = Column(Float, nullable=False)
    value_usd = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # BOOKED, DOCUMENTS_PENDING, etc.
    booking_date = Column(DateTime, nullable=False)
    vessel_berth_date = Column(DateTime, nullable=True)
    documents_lodged = Column(Boolean, default=False, nullable=False)
    estimated_arrival_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
