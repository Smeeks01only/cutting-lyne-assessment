from datetime import datetime, timedelta
from .. import models

def calculate_eta(shipment: models.Shipment) -> datetime:
    """
    Calculates estimated delivery based on the shipment's current state.
    
    NOTE: This is a transparent, deterministic rules-based prototype, 
    NOT a production-grade predictive machine learning ETA model.
    """
    # Handle missing dates safely by defaulting to current UTC time
    base_date = shipment.updated_at if shipment.updated_at else datetime.utcnow()
    
    status = shipment.status.upper() if shipment.status else ""

    # If already delivered and we have the actual date, return it
    if status == "DELIVERED" and shipment.actual_delivery_date:
        return shipment.actual_delivery_date

    # Define transparent rules for additional delivery time in days
    eta_rules_days = {
        "BOOKED": 30,
        "DOCUMENTS_PENDING": 30,
        "DOCUMENTS_LODGED": 28,
        "IN_TRANSIT": 14,
        "ARRIVED_AT_PORT": 5,
        "CUSTOMS_CLEARANCE": 3,
        "OUT_FOR_DELIVERY": 1,
        "DELIVERED": 0,
        "DELAYED": 21  # Prototype delay buffer
    }

    # Fallback to 14 days if the status is unknown or invalid
    days_to_add = eta_rules_days.get(status, 14)
    
    return base_date + timedelta(days=days_to_add)
