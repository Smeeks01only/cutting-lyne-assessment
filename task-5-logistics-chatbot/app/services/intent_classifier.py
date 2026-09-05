import re
from typing import Dict, Any

def classify_intent(message: str) -> Dict[str, Any]:
    """
    Classifies a logistics query into one of the predefined intents using
    a deterministic, keyword/rules-based mechanism.
    
    Intents:
    - SHIPMENT_TRACKING
    - CUSTOMS_DUTIES
    - IMPORT_DOCUMENTS
    - EXPORT_DOCUMENTS
    - CUSTOMS_CLEARANCE
    - GENERAL_LOGISTICS
    - UNKNOWN

    Returns: {"intent": str, "confidence": float}
    """
    msg_lower = message.lower()
    
    # 1. CUSTOMS_CLEARANCE
    if re.search(r'\b(clearance|clear customs)\b', msg_lower):
        return {"intent": "CUSTOMS_CLEARANCE", "confidence": 0.95}

    # 2. CUSTOMS_DUTIES
    if re.search(r'\b(duties|duty|tax|taxes|tariff)\b', msg_lower):
        return {"intent": "CUSTOMS_DUTIES", "confidence": 0.95}

    # 3. IMPORT / EXPORT DOCUMENTS
    if re.search(r'\b(document|documents|paperwork|certificate|permit|invoice|form)\b', msg_lower):
        if 'import' in msg_lower:
            return {"intent": "IMPORT_DOCUMENTS", "confidence": 0.90}
        if 'export' in msg_lower:
            return {"intent": "EXPORT_DOCUMENTS", "confidence": 0.90}
        # Fallback to general logistics if they just ask about documents
        return {"intent": "GENERAL_LOGISTICS", "confidence": 0.60}

    # 4. SHIPMENT_TRACKING
    # Checks for tracking combinations like 'where is my cargo' or 'track shipment'
    if re.search(r'\b(track|tracking|status|where is|locate)\b', msg_lower) and \
       re.search(r'\b(cargo|shipment|package|container|order|my)\b', msg_lower):
        return {"intent": "SHIPMENT_TRACKING", "confidence": 0.90}
    # Direct checks for tracking identifiers or the explicit word 'track'
    if re.search(r'\btrack\b', msg_lower) or re.search(r'clf-\d{4}-\d{3}', msg_lower):
        return {"intent": "SHIPMENT_TRACKING", "confidence": 0.85}
        
    # 5. GENERAL_LOGISTICS
    # Broad catch-all for logistics terms
    if re.search(r'\b(incoterm|incoterms|fcl|lcl|freight|insurance|demurrage|detention|packing list|bill of lading|awb|hs code)\b', msg_lower):
        return {"intent": "GENERAL_LOGISTICS", "confidence": 0.85}

    # 6. UNKNOWN
    return {"intent": "UNKNOWN", "confidence": 0.0}
