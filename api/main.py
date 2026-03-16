from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from .dependencies import get_db

app = FastAPI(
    title="Belgian Fleet Optimizer API",
    description="API for managing vehicles, drivers, parcels, and mileage logs.",
    version="1.0.0"
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. Change to specific origins in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Belgian Fleet Optimizer API"}

# --- Vehicles ---
@app.get("/vehicles/", response_model=List[schemas.Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = crud.get_vehicles(db, skip=skip, limit=limit)
    return vehicles

@app.post("/vehicles/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db=db, vehicle=vehicle)

@app.get("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

# --- Drivers ---
@app.get("/drivers/", response_model=List[schemas.Driver])
def read_drivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    drivers = crud.get_drivers(db, skip=skip, limit=limit)
    return drivers

@app.post("/drivers/", response_model=schemas.Driver)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    return crud.create_driver(db=db, driver=driver)

@app.get("/drivers/{driver_id}", response_model=schemas.Driver)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = crud.get_driver(db, driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

# --- Parcels ---
@app.get("/parcels/", response_model=List[schemas.Parcel])
def read_parcels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parcels = crud.get_parcels(db, skip=skip, limit=limit)
    return parcels

@app.post("/parcels/", response_model=schemas.Parcel)
def create_parcel(parcel: schemas.ParcelCreate, db: Session = Depends(get_db)):
    return crud.create_parcel(db=db, parcel=parcel)

# --- Mileage Logs ---
@app.get("/mileage_logs/", response_model=List[schemas.MileageLog])
def read_mileage_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_mileage_logs(db, skip=skip, limit=limit)
    return logs

@app.post("/mileage_logs/", response_model=schemas.MileageLog)
def create_mileage_log(log: schemas.MileageLogCreate, db: Session = Depends(get_db)):
    return crud.create_mileage_log(db=db, log=log)
