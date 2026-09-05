from typing import Dict, Any, List

def generate_response(
    intent_data: Dict[str, Any], 
    retrieval_results: List[Dict[str, Any]], 
    user_message: str
) -> Dict[str, Any]:
    """
    Generates a deterministic chatbot response based on the classified intent and retrieved knowledge.
    Returns a structured dictionary with the answer, intent, confidence, and sources.
    """
    intent = intent_data.get("intent", "UNKNOWN")
    intent_confidence = intent_data.get("confidence", 0.0)
    
    # Check for Unknown intent
    if intent == "UNKNOWN":
        return _build_fallback(intent, intent_confidence)

    # Handle Shipment Tracking via the isolated Shipment Client
    if intent == "SHIPMENT_TRACKING":
        from .shipment_client import process_tracking_request
        tracking_answer = process_tracking_request(user_message)
        return {
            "answer": tracking_answer,
            "intent": intent,
            "confidence": intent_confidence,
            "sources": []
        }

    # Handle Knowledge Base Queries (Duties, Documents, Clearance, General Logistics)
    # If the retriever returned an empty list, it means the similarity was below the configured threshold.
    if not retrieval_results:
        return _build_fallback(intent, intent_confidence)

    # Use the best matching retrieval result
    best_match = retrieval_results[0]
    retrieval_score = best_match.get("score", 0.0)
    base_answer = best_match.get("answer", "")
    source_id = best_match.get("id", "unknown_source")
    
    # Enforce strict customs disclaimer for relevant intents if not already explicitly stated
    customs_intents = ["CUSTOMS_DUTIES", "CUSTOMS_CLEARANCE", "IMPORT_DOCUMENTS", "EXPORT_DOCUMENTS"]
    if intent in customs_intents:
        disclaimer = " Specific requirements and current tariff information should always be verified with the relevant customs authority or a licensed customs professional."
        if "verified with the relevant customs authority" not in base_answer.lower():
            base_answer += disclaimer
            
    return {
        "answer": base_answer.strip(),
        "intent": intent,
        "confidence": float(round(retrieval_score, 4)),
        "sources": [source_id]
    }

def _build_fallback(intent: str, confidence: float) -> Dict[str, Any]:
    """
    Returns a safe fallback response explaining that the chatbot does not have 
    enough information to answer reliably, preventing hallucination or fabrication.
    """
    return {
        "answer": "I'm sorry, I don't have enough information to answer that reliably. Please consult our support team or a logistics professional.",
        "intent": intent,
        "confidence": confidence,
        "sources": []
    }
