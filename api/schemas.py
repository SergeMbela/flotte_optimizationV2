from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from db.models import EngineType, VehicleStatus, ParcelStatus, UrgencyLevel, MileageEntryType, LeaveType, LeaveStatus

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

# --- Leave Schemas ---
class LeaveBase(BaseModel):
    driver_id: int
    leave_type: LeaveType
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(BaseModel):
    status: LeaveStatus

class Leave(LeaveBase):
    id: int
    status: LeaveStatus
    model_config = ConfigDict(from_attributes=True)

# --- Vehicle Model Schemas ---
class VehicleModelBase(BaseModel):
    brand: str
    model_name: str

class VehicleModelCreate(VehicleModelBase):
    pass

class VehicleModel(VehicleModelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Vehicle Schemas ---
class VehicleBase(BaseModel):
    license_plate: str
    model_id: Optional[int] = None
    engine_type: EngineType
    status: VehicleStatus = VehicleStatus.AVAILABLE
    capacity_m3: float
    purchase_price: float
    estimated_residual_value: float

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    vehicle_model: Optional[VehicleModel] = None
    model_config = ConfigDict(from_attributes=True)

# --- Leasing Contract Schemas ---
class LeasingContractBase(BaseModel):
    vehicle_id: int
    contract_months: int = 36
    max_monthly_km: int
    annual_rate_pct: float = 4.5
    monthly_fee: float
    penalty_per_km_eur: float
    monthly_maintenance_eur: float = 0.0
    monthly_insurance_eur: float = 0.0
    monthly_replacement_veh_eur: float = 0.0
    vat_recovery_pct: float = 100.0
    co2_tax_annual_eur: float = 0.0
    age_tax_annual_eur: float = 0.0
    non_deductible_pct: float = 0.0
    monthly_energy_eur: float = 0.0
    monthly_indirect_costs_eur: float = 0.0
    notes: Optional[str] = None

class LeasingContractCreate(LeasingContractBase):
    pass

class LeasingContract(LeasingContractBase):
    id: int
    tco_monthly_eur: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Parcel Schemas ---
class ParcelBase(BaseModel):
    weight_kg: float
    length_cm: Optional[float] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None
    urgency: UrgencyLevel = UrgencyLevel.STANDARD
    delivery_address: str
    lat: Optional[float] = None
    lon: Optional[float] = None

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

# --- Competitor Schemas ---
class CompetitorPriceBase(BaseModel):
    urgency: UrgencyLevel
    base_fee: float
    per_kg_fee: float

class CompetitorPriceCreate(CompetitorPriceBase):
    competitor_id: int

class CompetitorPrice(CompetitorPriceBase):
    id: int
    competitor_id: int
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CompetitorBase(BaseModel):
    name: str

class CompetitorCreate(CompetitorBase):
    pass

class Competitor(CompetitorBase):
    id: int
    prices: List[CompetitorPrice] = []
    model_config = ConfigDict(from_attributes=True)

