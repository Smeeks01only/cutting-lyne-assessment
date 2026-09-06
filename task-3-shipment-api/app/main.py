from fastapi import FastAPI
from datetime import datetime, timedelta
from .database import engine, Base, SessionLocal
from .routes import shipments
from . import models
import logging

# Create the database tables
Base.metadata.create_all(bind=engine)

description = """
Shipment Tracking API is a **technical-assessment prototype** for Cutting Lyne Freight & Logistics.

## Important Disclaimers
* **Prototype Status**: This is a technical-assessment prototype only.
* **ETA Calculations**: The estimated delivery dates are derived from simple rules-based estimates, NOT production predictive models.
* **Risk Engine**: The risk flags generated are based entirely on deterministic business rules.
* **Sample Data**: All shipment data and records returned by this API are strictly fictional demonstration data.
"""

# Initialize the FastAPI app
app = FastAPI(
    title="Cutting Lyne - Task 3 Shipment API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Cutting Lyne AI Assessment",
    }
)

# Include routes
app.include_router(shipments.router)

@app.on_event("startup")
def populate_mock_data():
    """
    Utility function to populate the database with realistic sample shipments
    on startup if they don't already exist.
    """
    db = SessionLocal()
    existing = db.query(models.Shipment).first()
    
    if not existing:
        now = datetime.utcnow()
        
        mock_shipments = [
            # 1. Normal shipment in transit
            models.Shipment(
                tracking_number="TRK-TRANSIT-01",
                client_name="Acme Corp",
                origin="Shanghai, China",
                destination="Los Angeles, USA",
                cargo_type="Electronics",
                weight_kg=5000.0,
                value_usd=150000.0,
                status="IN_TRANSIT",
                booking_date=now - timedelta(days=14),
                vessel_berth_date=now - timedelta(days=2),
                documents_lodged=True,
                estimated_arrival_date=now + timedelta(days=10)
            ),
            # 2. Documents not lodged and vessel berth is within 7 days
            models.Shipment(
                tracking_number="TRK-URGENT-02",
                client_name="Global Trade LLC",
                origin="Rotterdam, Netherlands",
                destination="New York, USA",
                cargo_type="Machinery Parts",
                weight_kg=2500.5,
                value_usd=85000.0,
                status="DOCUMENTS_PENDING",
                booking_date=now - timedelta(days=20),
                vessel_berth_date=now + timedelta(days=4), # Berth in 4 days
                documents_lodged=False,
                estimated_arrival_date=now + timedelta(days=14)
            ),
            # 3. Shipment undergoing customs clearance
            models.Shipment(
                tracking_number="TRK-CUSTOMS-03",
                client_name="Tech Imports Inc",
                origin="Shenzhen, China",
                destination="Seattle, USA",
                cargo_type="Computer Peripherals",
                weight_kg=1200.0,
                value_usd=45000.0,
                status="CUSTOMS_CLEARANCE",
                booking_date=now - timedelta(days=30),
                vessel_berth_date=now - timedelta(days=15),
                documents_lodged=True,
                estimated_arrival_date=now - timedelta(days=1)
            ),
            # 4. Delayed shipment
            models.Shipment(
                tracking_number="TRK-DELAYED-04",
                client_name="FastTrack Logistics",
                origin="Mumbai, India",
                destination="London, UK",
                cargo_type="Textiles",
                weight_kg=8000.0,
                value_usd=120000.0,
                status="DELAYED",
                booking_date=now - timedelta(days=40),
                vessel_berth_date=now - timedelta(days=35),
                documents_lodged=True,
                estimated_arrival_date=now - timedelta(days=5) # Missed ETA
            ),
            # 5. Delivered shipment
            models.Shipment(
                tracking_number="TRK-DELIVERED-05",
                client_name="Retail Giants Co",
                origin="Sydney, Australia",
                destination="Tokyo, Japan",
                cargo_type="Agricultural Products",
                weight_kg=15000.0,
                value_usd=200000.0,
                status="DELIVERED",
                booking_date=now - timedelta(days=50),
                vessel_berth_date=now - timedelta(days=40),
                documents_lodged=True,
                estimated_arrival_date=now - timedelta(days=10),
                actual_delivery_date=now - timedelta(days=9)
            ),
        ]
        db.add_all(mock_shipments)
        db.commit()
    db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the Shipment Tracking API! Visit /docs for the API documentation."}
