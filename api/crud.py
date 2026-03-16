from sqlalchemy.orm import Session
from db import models
from . import schemas

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

# --- Parcel CRUD ---
def get_parcel(db: Session, parcel_id: int):
    return db.query(models.Parcel).filter(models.Parcel.id == parcel_id).first()

def get_parcels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parcel).offset(skip).limit(limit).all()

def create_parcel(db: Session, parcel: schemas.ParcelCreate):
    db_parcel = models.Parcel(**parcel.model_dump())
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
