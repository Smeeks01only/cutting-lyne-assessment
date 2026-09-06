from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ShipmentBase(BaseModel):
    tracking_number: str
    client_name: str
    origin: str
    destination: str
    cargo_type: str
    weight_kg: float
    value_usd: float
    status: str
    booking_date: datetime
    vessel_berth_date: Optional[datetime] = None
    documents_lodged: bool
    estimated_arrival_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None

class ShipmentCreate(ShipmentBase):
    pass

class RiskFlag(BaseModel):
    code: str
    severity: str
    message: str

class ShipmentResponse(ShipmentBase):
    risk_flags: List[RiskFlag] = []
    
    # Computed ETA field returned by the API
    estimated_delivery_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        # For Pydantic v2 support
        from_attributes = True
