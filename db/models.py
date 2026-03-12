from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from .database import Base

# --- ENUMÉRATIONS (LOGIQUE MÉTIER) ---

class EngineType(str, enum.Enum):
    DIESEL = "DIESEL"
    PETROL = "PETROL"
    ELECTRIC = "ELECTRIC"

class VehicleStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    IN_MAINTENANCE = "IN_MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

class ParcelStatus(str, enum.Enum):
    PENDING = "PENDING"      # En attente
    IN_TRANSIT = "IN_TRANSIT" # En cours de livraison
    DELIVERED = "DELIVERED"  # Livré
    REFUSED = "REFUSED"      # Refusé (Retour dépôt)
    LOST = "LOST"            # Perdu

class UrgencyLevel(str, enum.Enum):
    STANDARD = "STANDARD"
    EXPRESS = "EXPRESS"
    SAME_DAY = "SAME_DAY"

class LeaveType(str, enum.Enum):
    PAID = "CONGÉ PAYÉ"
    SICK = "MALADIE"
    UNPAID = "SANS SOLDE"
    RECOVERY = "RÉCUPÉRATION"

class LeaveStatus(str, enum.Enum):
    PENDING = "EN ATTENTE"
    APPROVED = "APPROUVÉ"
    REJECTED = "REFUSÉ"

# --- MODÈLES DE TABLES ---

class Depot(Base):
    __tablename__ = "depots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # Coordonnées de contact (Ajoutées pour l'ERP)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    
    # RH & Logistique
    home_address = Column(String)
    home_lat = Column(Float)
    home_lon = Column(Float)
    driven_minutes_today = Column(Integer, default=0) # Pour la règle des 9h
    takes_van_home = Column(Boolean, default=True)    # Avantage en nature (ATN)
    
    # Relations
    leaves = relationship("Leave", back_populates="driver")

class Leave(Base):
    """Gestion des absences chauffeurs"""
    __tablename__ = "leaves"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    
    leave_type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    reason = Column(String, nullable=True)
    
    driver = relationship("Driver", back_populates="leaves")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, index=True) # Plaque belge
    engine_type = Column(Enum(EngineType), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.AVAILABLE)
    
    # Capacité et Finance
    capacity_m3 = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    estimated_residual_value = Column(Float, nullable=False) # Valeur de revente
    
    # Relation 1-to-1 avec le leasing
    leasing_contract = relationship("LeasingContract", back_populates="vehicle", uselist=False)

class LeasingContract(Base):
    __tablename__ = "leasing_contracts"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), unique=True)
    
    monthly_fee = Column(Float, nullable=False)      # Loyer mensuel
    max_monthly_km = Column(Integer, nullable=False) # Forfait km
    penalty_per_km_eur = Column(Float, nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="leasing_contract")

class Parcel(Base):
    __tablename__ = "parcels"
    id = Column(Integer, primary_key=True, index=True)
    
    # Physique et Pricing
    weight_kg = Column(Float, nullable=False)
    length_cm = Column(Float)
    width_cm = Column(Float)
    height_cm = Column(Float)
    urgency = Column(Enum(UrgencyLevel), default=UrgencyLevel.STANDARD)
    price_charged = Column(Float) # Calculé via PricingService
    
    # Statut et Dates (pour historique 30j)
    status = Column(Enum(ParcelStatus), default=ParcelStatus.PENDING)
    delivery_address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Competitor(Base):
    """Référence des concurrents (Bpost, PostNL, etc.)"""
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    prices = relationship("CompetitorPrice", back_populates="competitor")

class CompetitorPrice(Base):
    """Benchmark des tarifs du marché"""
    __tablename__ = "competitor_prices"
    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"))
    
    urgency = Column(Enum(UrgencyLevel), nullable=False)
    base_fee = Column(Float, nullable=False)   # Prise en charge
    per_kg_fee = Column(Float, nullable=False) # Supplément poids
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    competitor = relationship("Competitor", back_populates="prices")