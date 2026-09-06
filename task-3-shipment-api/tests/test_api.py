import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from app.main import app
from app.database import Base, get_db
from app.models import Shipment

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the FastAPI dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_test_db():
    """
    Sets up isolated test data in the in-memory SQLite DB.
    """
    db = TestingSessionLocal()
    now = datetime.utcnow()
    
    shipments = [
        Shipment(
            tracking_number="TRK-NORMAL",
            client_name="Test Client",
            origin="Test Origin",
            destination="Test Dest",
            cargo_type="Test Cargo",
            weight_kg=100.0,
            value_usd=1000.0,
            status="IN_TRANSIT",
            booking_date=now,
            documents_lodged=True,
            vessel_berth_date=now + timedelta(days=10)
        ),
        Shipment(
            tracking_number="TRK-NOLODGE",
            client_name="Test Client",
            origin="Test Origin",
            destination="Test Dest",
            cargo_type="Test Cargo",
            weight_kg=100.0,
            value_usd=1000.0,
            status="IN_TRANSIT",
            booking_date=now,
            documents_lodged=False,
            vessel_berth_date=now + timedelta(days=2) # triggers risk rule 1
        ),
        Shipment(
            tracking_number="TRK-DELAYED",
            client_name="Test Client",
            origin="Test Origin",
            destination="Test Dest",
            cargo_type="Test Cargo",
            weight_kg=100.0,
            value_usd=1000.0,
            status="DELAYED",
            booking_date=now,
            documents_lodged=True,
        )
    ]
    db.add_all(shipments)
    db.commit()
    
    yield  # Tests execute here
    
    # Teardown
    for s in shipments:
        db.delete(s)
    db.commit()
    db.close()


def test_get_existing_shipment(setup_test_db):
    """Test requirement 1, 2, 3, 4"""
    response = client.get("/api/shipments/TRK-NORMAL")
    assert response.status_code == 200
    data = response.json()
    assert data["tracking_number"] == "TRK-NORMAL"
    assert data["status"] == "IN_TRANSIT"
    assert "estimated_delivery_date" in data
    assert "risk_flags" in data

def test_documents_not_lodged_risk(setup_test_db):
    """Test requirement 5, 6"""
    response = client.get("/api/shipments/TRK-NOLODGE")
    assert response.status_code == 200
    data = response.json()
    assert len(data["risk_flags"]) > 0
    codes = [flag["code"] for flag in data["risk_flags"]]
    assert "DOCUMENTS_NOT_LODGED" in codes

def test_delayed_risk(setup_test_db):
    """Test requirement 7"""
    response = client.get("/api/shipments/TRK-DELAYED")
    assert response.status_code == 200
    data = response.json()
    assert len(data["risk_flags"]) > 0
    codes = [flag["code"] for flag in data["risk_flags"]]
    assert "SHIPMENT_DELAYED" in codes

def test_shipment_no_risks(setup_test_db):
    """Test requirement 8"""
    response = client.get("/api/shipments/TRK-NORMAL")
    assert response.status_code == 200
    data = response.json()
    assert len(data["risk_flags"]) == 0

def test_unknown_tracking_number(setup_test_db):
    """Test requirement 9"""
    response = client.get("/api/shipments/TRK-UNKNOWN")
    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment with tracking number 'TRK-UNKNOWN' not found."

def test_invalid_tracking_number(setup_test_db):
    """Test requirement 10"""
    # Tracking number is < 3 characters (defined in route validation)
    response = client.get("/api/shipments/AB")
    assert response.status_code == 422
    assert "detail" in response.json()
