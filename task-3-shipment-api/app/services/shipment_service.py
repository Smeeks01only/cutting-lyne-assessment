from sqlalchemy.orm import Session
from .. import models, schemas
from .risk_engine import evaluate_risk
from .eta_service import calculate_eta

def get_shipment(db: Session, tracking_number: str) -> schemas.ShipmentResponse:
    """
    Retrieves a shipment and generates the full response with ETA and Risk Flags.
    """
    shipment_obj = db.query(models.Shipment).filter(models.Shipment.tracking_number == tracking_number).first()

    if not shipment_obj:
        return None

    # Calculate ETA and Risk Flags dynamically
    eta = calculate_eta(shipment_obj)
    risk_flags = evaluate_risk(shipment_obj)

    # Use from_orm to parse the SQLAlchemy object into a Pydantic model
    # Using from_orm (deprecated in v2) but keeping it for backward compatibility
    response = schemas.ShipmentResponse.from_orm(shipment_obj)
    response.estimated_delivery_date = eta
    response.risk_flags = [schemas.RiskFlag(**flag) for flag in risk_flags]

    return response
