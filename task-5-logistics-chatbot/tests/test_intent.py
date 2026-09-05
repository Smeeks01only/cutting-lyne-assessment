import pytest
from app.services.intent_classifier import classify_intent

def test_classify_shipment_tracking():
    # Direct from examples
    res = classify_intent("Where is my cargo?")
    assert res["intent"] == "SHIPMENT_TRACKING"
    assert res["confidence"] == 0.90

    res = classify_intent("Track CLF-2026-002")
    assert res["intent"] == "SHIPMENT_TRACKING"
    assert res["confidence"] == 0.85

def test_classify_customs_duties():
    res = classify_intent("What duties do I pay?")
    assert res["intent"] == "CUSTOMS_DUTIES"
    assert res["confidence"] == 0.95

def test_classify_import_documents():
    res = classify_intent("What documents do I need to import?")
    assert res["intent"] == "IMPORT_DOCUMENTS"
    assert res["confidence"] == 0.90

def test_classify_export_documents():
    res = classify_intent("What paperwork is required for export?")
    assert res["intent"] == "EXPORT_DOCUMENTS"
    assert res["confidence"] == 0.90

def test_classify_customs_clearance():
    res = classify_intent("How long does customs clearance take?")
    assert res["intent"] == "CUSTOMS_CLEARANCE"
    assert res["confidence"] == 0.95

def test_classify_general_logistics():
    res = classify_intent("Tell me about incoterms.")
    assert res["intent"] == "GENERAL_LOGISTICS"
    assert res["confidence"] == 0.85

    res = classify_intent("What is a bill of lading?")
    assert res["intent"] == "GENERAL_LOGISTICS"
    assert res["confidence"] == 0.85

def test_classify_unknown():
    res = classify_intent("What is the capital of France?")
    assert res["intent"] == "UNKNOWN"
    assert res["confidence"] == 0.0
