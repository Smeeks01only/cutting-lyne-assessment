from datetime import datetime
from .. import models

def evaluate_risk(shipment: models.Shipment) -> list[dict]:
    """
    Evaluates a shipment for potential risks based on deterministic business rules.
    Returns a list of structured risk flags. No LLM or ML is used here.
    """
    flags = []
    added_codes = set()
    
    def add_flag(code: str, severity: str, message: str):
        # Prevent generating duplicate risk flags
        if code not in added_codes:
            flags.append({
                "code": code,
                "severity": severity,
                "message": message
            })
            added_codes.add(code)

    now = datetime.utcnow()
    status = shipment.status.upper() if shipment.status else ""
    
    # RULE 1: Required documents have not been lodged AND vessel berth date is within 7 days
    if shipment.vessel_berth_date and not shipment.documents_lodged:
        days_to_berth = (shipment.vessel_berth_date - now).total_seconds() / 86400.0
        if 0 <= days_to_berth <= 7:
            add_flag(
                code="DOCUMENTS_NOT_LODGED",
                severity="HIGH",
                message=f"Required documents have not been lodged and vessel berths in {int(days_to_berth)} days."
            )
            
    # RULE 2: If the shipment status is DELAYED
    if status == "DELAYED":
        add_flag(
            code="SHIPMENT_DELAYED",
            severity="HIGH",
            message="Shipment has been marked as delayed."
        )

    # RULE 3: If shipment is at ARRIVED_AT_PORT or CUSTOMS_CLEARANCE and documents have not been lodged
    if status in ["ARRIVED_AT_PORT", "CUSTOMS_CLEARANCE"] and not shipment.documents_lodged:
        add_flag(
            code="MISSING_CUSTOMS_DOCUMENTS",
            severity="CRITICAL",
            message=f"Shipment is at {status} but required documents are missing."
        )

    # RULE 4: If the vessel berth date has already passed while the shipment is still in a pre-arrival status
    pre_arrival_statuses = ["BOOKED", "DOCUMENTS_PENDING", "DOCUMENTS_LODGED", "IN_TRANSIT"]
    if status in pre_arrival_statuses and shipment.vessel_berth_date:
        if (now - shipment.vessel_berth_date).total_seconds() > 0:
            add_flag(
                code="VESSEL_BERTH_MISMATCH",
                severity="MEDIUM",
                message="Vessel berth date has passed but shipment is still in pre-arrival status."
            )

    return flags
