from sqlalchemy.orm import Session
from db import models
from . import schemas
from .services.tco_service import calculate_tco
from .services.pricing_service import calculate_parcel_price

# --- Depot CRUD ---
def get_depots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Depot).offset(skip).limit(limit).all()

def create_depot(db: Session, depot: schemas.DepotCreate):
    db_depot = models.Depot(**depot.model_dump())
    db.add(db_depot)
    db.commit()
    db.refresh(db_depot)
    return db_depot

def delete_depot(db: Session, depot_id: int):
    db_depot = db.query(models.Depot).filter(models.Depot.id == depot_id).first()
    if db_depot:
        db.delete(db_depot)
        db.commit()
    return db_depot

# --- Vehicle Model CRUD ---
def get_vehicle_model(db: Session, model_id: int):
    return db.query(models.VehicleModel).filter(models.VehicleModel.id == model_id).first()

def get_vehicle_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VehicleModel).offset(skip).limit(limit).all()

def create_vehicle_model(db: Session, model: schemas.VehicleModelCreate):
    db_model = models.VehicleModel(**model.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

# --- Vehicle CRUD ---
def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# --- Driver CRUD ---
def get_driver(db: Session, driver_id: int):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()

def get_drivers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Driver).offset(skip).limit(limit).all()

def create_driver(db: Session, driver: schemas.DriverCreate):
    db_driver = models.Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

# --- Leave CRUD ---
def get_leaves(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Leave).offset(skip).limit(limit).all()

def get_driver_leaves(db: Session, driver_id: int):
    return db.query(models.Leave).filter(models.Leave.driver_id == driver_id).all()

def create_leave(db: Session, leave: schemas.LeaveCreate):
    db_leave = models.Leave(**leave.model_dump())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def update_leave_status(db: Session, leave_id: int, status: str):
    db_leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if db_leave:
        db_leave.status = status
        db.commit()
        db.refresh(db_leave)
    return db_leave

# --- Leasing Contract CRUD ---
def get_leasing_contracts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LeasingContract).offset(skip).limit(limit).all()

def get_vehicle_leasing(db: Session, vehicle_id: int):
    return db.query(models.LeasingContract).filter(models.LeasingContract.vehicle_id == vehicle_id).first()

def update_all_tco(db: Session):
    contracts = db.query(models.LeasingContract).all()
    for contract in contracts:
        contract.tco_monthly_eur = calculate_tco(contract)
    db.commit()
    return len(contracts)

def create_leasing_contract(db: Session, contract: schemas.LeasingContractCreate):
    db_contract = models.LeasingContract(**contract.model_dump())
    # Note: TCO calculation happens here
    db_contract.tco_monthly_eur = calculate_tco(db_contract)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

# --- Parcel CRUD ---
def get_parcel(db: Session, parcel_id: int):
    return db.query(models.Parcel).filter(models.Parcel.id == parcel_id).first()

def get_parcels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parcel).offset(skip).limit(limit).all()

def create_parcel(db: Session, parcel: schemas.ParcelCreate):
    db_parcel = models.Parcel(**parcel.model_dump())
    
    # calculate price automatically if not provided
    if db_parcel.price_charged is None:
        db_parcel.price_charged = calculate_parcel_price(db, db_parcel.weight_kg, db_parcel.urgency)
        
    db.add(db_parcel)
    db.commit()
    db.refresh(db_parcel)
    return db_parcel

# --- Mileage Log CRUD ---
def create_mileage_log(db: Session, log: schemas.MileageLogCreate):
    db_log = models.MileageLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_mileage_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MileageLog).offset(skip).limit(limit).all()

# --- Competitor CRUD ---
def get_competitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competitor).offset(skip).limit(limit).all()

def create_competitor(db: Session, competitor: schemas.CompetitorCreate):
    db_competitor = models.Competitor(**competitor.model_dump())
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    return db_competitor

def create_competitor_price(db: Session, price: schemas.CompetitorPriceCreate):
    db_price = models.CompetitorPrice(**price.model_dump())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

