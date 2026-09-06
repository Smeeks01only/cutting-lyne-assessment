from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from .. import schemas
from ..services import shipment_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/shipments",
    tags=["shipments"]
)

@router.get(
    "/{tracking_number}", 
    response_model=schemas.ShipmentResponse,
    summary="Get Shipment Details",
    description="""
Retrieve the current status, estimated delivery date, and risk flags for a given shipment.

- **Purpose**: To provide a unified shipment tracking view integrating basic ETA and Risk systems.
- **Path Parameter**: `tracking_number` (string, min length 3) - The unique identifier of the shipment.
- **Risk Flag Structure**: A list of objects containing a `code`, `severity`, and `message`.

**Note**: This is a technical-assessment prototype. ETAs and risk flags are rules-based. Sample data is completely fictional.
    """,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "tracking_number": "TRK-URGENT-02",
                        "client_name": "Global Trade LLC",
                        "origin": "Rotterdam, Netherlands",
                        "destination": "New York, USA",
                        "cargo_type": "Machinery Parts",
                        "weight_kg": 2500.5,
                        "value_usd": 85000.0,
                        "status": "DOCUMENTS_PENDING",
                        "booking_date": "2023-01-01T12:00:00",
                        "vessel_berth_date": "2023-01-05T12:00:00",
                        "documents_lodged": False,
                        "estimated_arrival_date": "2023-01-15T12:00:00",
                        "estimated_delivery_date": "2023-01-18T12:00:00",
                        "risk_flags": [
                            {
                                "code": "DOCUMENTS_NOT_LODGED",
                                "severity": "HIGH",
                                "message": "Required documents have not been lodged and vessel berths in 4 days."
                            }
                        ]
                    }
                }
            }
        },
        404: {
            "description": "Shipment Not Found",
            "content": {
                "application/json": {
                    "example": {"detail": "Shipment with tracking number 'TRK99999' not found."}
                }
            }
        },
        422: {
            "description": "Validation Error (e.g., tracking number too short)"
        }
    }
)
def get_shipment_status(
    tracking_number: str = Path(..., min_length=3, description="The unique tracking number of the shipment"),
    db: Session = Depends(get_db)
):
    """
    Retrieve the current status, estimated delivery date, and risk flags for a given shipment.
    """
    try:
        shipment_resp = shipment_service.get_shipment(db, tracking_number)
        
        if not shipment_resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with tracking number '{tracking_number}' not found."
            )
        
        return shipment_resp

    except HTTPException:
        # Re-raise HTTPExceptions (like 404) so they aren't caught by the generic Exception block
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving shipment {tracking_number}: {str(e)}")
        # Return 500 without exposing internal stack traces
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the request."
        )
