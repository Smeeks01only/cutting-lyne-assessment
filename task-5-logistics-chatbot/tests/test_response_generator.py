import pytest
from app.services.response_generator import generate_response

def test_generate_response_tracking():
    intent_data = {"intent": "SHIPMENT_TRACKING", "confidence": 0.9}
    res = generate_response(intent_data, [], "Track my cargo")
    assert res["intent"] == "SHIPMENT_TRACKING"
    assert "tracking request" in res["answer"]
    assert len(res["sources"]) == 0

def test_generate_response_below_threshold():
    # Simulated scenario where retriever returns nothing because score < threshold
    intent_data = {"intent": "CUSTOMS_DUTIES", "confidence": 0.8}
    res = generate_response(intent_data, [], "Tell me about quantum physics taxes")
    assert "don't have enough information" in res["answer"]
    assert len(res["sources"]) == 0

def test_generate_response_unknown_intent():
    intent_data = {"intent": "UNKNOWN", "confidence": 0.0}
    res = generate_response(intent_data, [], "Hi")
    assert "don't have enough information" in res["answer"]

def test_generate_response_valid_knowledge():
    intent_data = {"intent": "GENERAL_LOGISTICS", "confidence": 0.85}
    retrieval_results = [{
        "id": "log_001",
        "answer": "Incoterms define responsibilities of buyers and sellers.",
        "score": 0.92
    }]
    res = generate_response(intent_data, retrieval_results, "What are incoterms?")
    assert "Incoterms define responsibilities" in res["answer"]
    assert res["confidence"] == 0.92
    assert "log_001" in res["sources"]

def test_generate_response_adds_customs_disclaimer():
    intent_data = {"intent": "CUSTOMS_DUTIES", "confidence": 0.95}
    retrieval_results = [{
        "id": "duty_001",
        "answer": "Duties are calculated based on HS codes.",
        "score": 0.88
    }]
    res = generate_response(intent_data, retrieval_results, "What duties do I pay?")
    # Because intent is CUSTOMS_DUTIES, it should append the specific disclaimer
    assert "verified with the relevant customs authority" in res["answer"].lower()
    assert res["confidence"] == 0.88
    assert "duty_001" in res["sources"]
