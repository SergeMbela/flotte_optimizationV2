from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from db.models import EngineType, VehicleStatus, ParcelStatus, UrgencyLevel, MileageEntryType

# --- Schemas for Base Models ---

class DepotBase(BaseModel):
    name: str
    lat: float
    lon: float

class DepotCreate(DepotBase):
    pass

class Depot(DepotBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Driver Schemas ---
class DriverBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    home_address: Optional[str] = None
    home_lat: Optional[float] = None
    home_lon: Optional[float] = None
    takes_van_home: bool = True

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    id: int
    driven_minutes_today: int
    model_config = ConfigDict(from_attributes=True)

# --- Vehicle Schemas ---
class VehicleBase(BaseModel):
    license_plate: str
    engine_type: EngineType
    status: VehicleStatus = VehicleStatus.AVAILABLE
    capacity_m3: float
    purchase_price: float
    estimated_residual_value: float

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Parcel Schemas ---
class ParcelBase(BaseModel):
    weight_kg: float
    length_cm: Optional[float] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None
    urgency: UrgencyLevel = UrgencyLevel.STANDARD
    delivery_address: str

class ParcelCreate(ParcelBase):
    pass

class Parcel(ParcelBase):
    id: int
    status: ParcelStatus
    price_charged: Optional[float] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Mileage Log Schemas ---
class MileageLogBase(BaseModel):
    driver_id: int
    vehicle_id: int
    mileage: float
    entry_type: MileageEntryType

class MileageLogCreate(MileageLogBase):
    pass

class MileageLog(MileageLogBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
