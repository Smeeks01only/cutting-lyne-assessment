import pytest
from datetime import datetime
from app.services.eta_service import calculate_eta
from app.models import Shipment

def test_calculate_eta_booked():
    base = datetime(2023, 1, 1, 12, 0)
    shipment = Shipment(status="BOOKED", updated_at=base)
    eta = calculate_eta(shipment)
    assert eta == datetime(2023, 1, 31, 12, 0)  # 1 + 30 = 31

def test_calculate_eta_in_transit():
    base = datetime(2023, 1, 1, 12, 0)
    shipment = Shipment(status="IN_TRANSIT", updated_at=base)
    eta = calculate_eta(shipment)
    assert eta == datetime(2023, 1, 15, 12, 0)  # 1 + 14 = 15

def test_calculate_eta_customs():
    base = datetime(2023, 1, 1, 12, 0)
    shipment = Shipment(status="CUSTOMS_CLEARANCE", updated_at=base)
    eta = calculate_eta(shipment)
    assert eta == datetime(2023, 1, 4, 12, 0)  # 1 + 3 = 4

def test_calculate_eta_delayed():
    base = datetime(2023, 1, 1, 12, 0)
    shipment = Shipment(status="DELAYED", updated_at=base)
    eta = calculate_eta(shipment)
    assert eta == datetime(2023, 1, 22, 12, 0)  # 1 + 21 = 22

def test_calculate_eta_delivered():
    actual_delivery = datetime(2023, 1, 5, 12, 0)
    shipment = Shipment(
        status="DELIVERED", 
        actual_delivery_date=actual_delivery, 
        updated_at=datetime(2023, 1, 5, 12, 0)
    )
    eta = calculate_eta(shipment)
    assert eta == actual_delivery

def test_calculate_eta_delivered_missing_actual_date():
    base = datetime(2023, 1, 1, 12, 0)
    shipment = Shipment(status="DELIVERED", updated_at=base)
    eta = calculate_eta(shipment)
    assert eta == datetime(2023, 1, 1, 12, 0)  # 0 days added

def test_calculate_eta_missing_updated_at():
    # Test handling of missing dates gracefully (defaults to utcnow)
    shipment = Shipment(status="OUT_FOR_DELIVERY", updated_at=None)
    eta = calculate_eta(shipment)
    now = datetime.utcnow()
    # The calculated eta should be exactly 1 day ahead of `now`
    # We assert the difference is approximately 1 day (using a tiny buffer for execution time)
    diff = eta - now
    assert 0.99 <= diff.total_seconds() / 86400 <= 1.01

def test_calculate_eta_unknown_status():
    base = datetime(2023, 1, 1, 12, 0)
    shipment = Shipment(status="ALIENS_STOLE_CARGO", updated_at=base)
    eta = calculate_eta(shipment)
    assert eta == datetime(2023, 1, 15, 12, 0)  # Default fallback 14 days
