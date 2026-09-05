import os
import re
import httpx
from typing import Dict, Any, Optional

# Read from environment variables, fallback to local development port for Task 3
SHIPMENT_API_URL = os.getenv("SHIPMENT_API_URL", "http://127.0.0.1:8000")

def extract_tracking_number(message: str) -> Optional[str]:
    """
    Extracts a tracking number from the user's message using clear regex patterns.
    Matches CLF-YYYY-NNN format and legacy TRK- format from Task 3.
    """
    # Look for CLF-2026-001 or TRK-URGENT-02 formats, ignoring case during search but returning upper
    match = re.search(r'\b(CLF-\d{4}-\d{3}|TRK-[A-Za-z0-9-]+)\b', message, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None

def fetch_shipment_details(tracking_number: str) -> Dict[str, Any]:
    """
    Calls the Task 3 REST API to retrieve shipment information.
    Handles HTTP timeouts, not found, and connection errors safely.
    """
    url = f"{SHIPMENT_API_URL}/api/shipments/{tracking_number}"
    
    try:
        # Enforce a 5 second timeout to prevent the chatbot from hanging
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("status", "UNKNOWN"),
                    "estimated_delivery_date": data.get("estimated_delivery_date"),
                    "risk_flags": data.get("risk_flags", [])
                }
            elif response.status_code == 404:
                return {"success": False, "error": f"Tracking number '{tracking_number}' was not found in the system."}
            elif response.status_code == 422:
                return {"success": False, "error": "Invalid tracking number format provided."}
            else:
                return {"success": False, "error": f"Shipment API returned an unexpected error (HTTP {response.status_code})."}
                
    except httpx.TimeoutException:
        return {"success": False, "error": "Connection to the shipment tracking API timed out."}
    except httpx.RequestError:
        return {"success": False, "error": "The shipment tracking API is currently unavailable."}
    except Exception as e:
        return {"success": False, "error": "An unexpected error occurred while communicating with the tracking system."}

def process_tracking_request(user_message: str) -> str:
    """
    Orchestrates the tracking flow:
    1. Extracts tracking number
    2. Prompts user if missing
    3. Fetches live data if present
    4. Formats human-readable response string
    """
    tracking_number = extract_tracking_number(user_message)
    
    if not tracking_number:
        return "I can help you track your cargo. Please provide your tracking number (e.g., CLF-2026-001)."
        
    details = fetch_shipment_details(tracking_number)
    
    if not details["success"]:
        return f"Sorry, I couldn't retrieve your shipment: {details['error']}"
        
    status = details["status"]
    
    # Format dates nicely if they exist
    eta = details.get("estimated_delivery_date")
    eta_str = eta.split("T")[0] if eta else "Not available"
    
    # Format a clean string response
    response_text = f"Shipment {tracking_number} is currently {status}. Estimated delivery: {eta_str}."
    
    # Append any critical risk flags
    risks = details.get("risk_flags", [])
    if risks:
        response_text += "\n\n**Risk Alerts:**"
        for risk in risks:
            response_text += f"\n- [{risk.get('severity', 'WARNING')}] {risk.get('message', 'Unknown risk')}"
            
    return response_text
