import pytest
from datetime import datetime, timedelta
from app.services.risk_engine import evaluate_risk
from app.models import Shipment

def test_documents_not_lodged_within_7_days():
    # RULE 1
    now = datetime.utcnow()
    shipment = Shipment(
        status="IN_TRANSIT",
        documents_lodged=False,
        vessel_berth_date=now + timedelta(days=4)
    )
    flags = evaluate_risk(shipment)
    assert len(flags) == 1
    assert flags[0]["code"] == "DOCUMENTS_NOT_LODGED"
    assert flags[0]["severity"] == "HIGH"

def test_documents_lodged_no_risk():
    now = datetime.utcnow()
    shipment = Shipment(
        status="IN_TRANSIT",
        documents_lodged=True,
        vessel_berth_date=now + timedelta(days=4)
    )
    flags = evaluate_risk(shipment)
    assert len(flags) == 0

def test_delayed_shipment():
    # RULE 2
    shipment = Shipment(
        status="DELAYED",
        documents_lodged=True
    )
    flags = evaluate_risk(shipment)
    assert len(flags) == 1
    assert flags[0]["code"] == "SHIPMENT_DELAYED"
    assert flags[0]["severity"] == "HIGH"

def test_customs_clearance_missing_documents():
    # RULE 3
    shipment = Shipment(
        status="CUSTOMS_CLEARANCE",
        documents_lodged=False
    )
    flags = evaluate_risk(shipment)
    assert len(flags) == 1
    assert flags[0]["code"] == "MISSING_CUSTOMS_DOCUMENTS"
    assert flags[0]["severity"] == "CRITICAL"

def test_vessel_berth_date_passed():
    # RULE 4
    now = datetime.utcnow()
    shipment = Shipment(
        status="IN_TRANSIT",
        documents_lodged=True,
        vessel_berth_date=now - timedelta(days=2) # passed
    )
    flags = evaluate_risk(shipment)
    assert len(flags) == 1
    assert flags[0]["code"] == "VESSEL_BERTH_MISMATCH"
    assert flags[0]["severity"] == "MEDIUM"

def test_shipment_with_no_risks():
    now = datetime.utcnow()
    shipment = Shipment(
        status="DELIVERED",
        documents_lodged=True,
        vessel_berth_date=now - timedelta(days=5)
    )
    flags = evaluate_risk(shipment)
    assert len(flags) == 0

def test_multiple_risks_and_no_duplicates():
    # RULE 2 and RULE 4
    now = datetime.utcnow()
    shipment = Shipment(
        status="DELAYED",
        documents_lodged=True,
        vessel_berth_date=now - timedelta(days=2) 
    )
    flags = evaluate_risk(shipment)
    # Status is DELAYED, so rule 2 triggers.
    # delayed is not in pre-arrival statuses, so rule 4 does NOT trigger.
    assert len(flags) == 1
    assert flags[0]["code"] == "SHIPMENT_DELAYED"

def test_rule_1_and_rule_4_mutex():
    now = datetime.utcnow()
    shipment = Shipment(
        status="IN_TRANSIT",
        documents_lodged=False,
        vessel_berth_date=now - timedelta(days=2) 
    )
    flags = evaluate_risk(shipment)
    # vessel_berth_date passed, so Rule 1 (-2 is not between 0 and 7) does not trigger.
    # Rule 4 triggers.
    assert len(flags) == 1
    assert flags[0]["code"] == "VESSEL_BERTH_MISMATCH"
