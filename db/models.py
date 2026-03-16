from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, ForeignKey, DateTime, Text
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

class MileageEntryType(str, enum.Enum):
    DEPOT_DEPARTURE = "DEPOT_DEPARTURE" # Départ du dépôt
    LAST_DELIVERY = "LAST_DELIVERY"     # Dernière livraison

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
    mileage_logs = relationship("MileageLog", back_populates="driver")

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

class VehicleModel(Base):
    __tablename__ = "vehicle_models"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False, index=True)
    model_name = Column(String, nullable=False, index=True)

    vehicles = relationship("Vehicle", back_populates="vehicle_model")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, index=True) # Plaque belge
    
    model_id = Column(Integer, ForeignKey("vehicle_models.id"), nullable=True)
    
    engine_type = Column(Enum(EngineType), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.AVAILABLE)
    
    # Capacité et Finance
    capacity_m3 = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    estimated_residual_value = Column(Float, nullable=False) # Valeur de revente
    
    # Relation 1-to-1 avec le leasing
    leasing_contract = relationship("LeasingContract", back_populates="vehicle", uselist=False)
    mileage_logs = relationship("MileageLog", back_populates="vehicle")
    vehicle_model = relationship("VehicleModel", back_populates="vehicles")

class LeasingContract(Base):
    """
    Contrat de Location Longue Durée (LLD).

    Loyer ≈ (Prix d'achat − Valeur Résiduelle + Intérêts) / Nb mois
    Le TCO (Total Cost of Ownership) intègre le loyer, l'énergie,
    la fiscalité et les coûts indirects.
    """
    __tablename__ = "leasing_contracts"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), unique=True)

    # ── 1. Loyer financier de base ──────────────────────────────────────────
    contract_months = Column(Integer, nullable=False, default=36)    # Durée (mois)
    max_monthly_km  = Column(Integer, nullable=False)                 # Forfait km/mois
    annual_rate_pct = Column(Float,   nullable=False, default=4.5)   # Taux annuel (%)
    monthly_fee     = Column(Float,   nullable=False)                 # Loyer calculé (€/mois)
    penalty_per_km_eur = Column(Float, nullable=False)               # Pénalité dépassement km

    # ── 2. Services LLD (leasing opérationnel) ──────────────────────────────
    monthly_maintenance_eur     = Column(Float, default=0.0)  # Maintenance + pneumatiques
    monthly_insurance_eur       = Column(Float, default=0.0)  # Assurance flotte (quote-part)
    monthly_replacement_veh_eur = Column(Float, default=0.0)  # Véhicule de remplacement

    # ── 3. Fiscalité ────────────────────────────────────────────────────────
    # TVA : 100 % récupérable pour utilitaires, 50 % pour véhicules de tourisme
    vat_recovery_pct            = Column(Float, default=100.0) # % TVA récupérable
    # Taxe CO₂ annuelle (ex-TVS) — basée sur les émissions
    co2_tax_annual_eur          = Column(Float, default=0.0)
    # Taxe ancienneté annuelle (2ᵉ composante ex-TVS)
    age_tax_annual_eur          = Column(Float, default=0.0)
    # Amortissement Non Déductible : part du loyer non déductible fiscalement
    non_deductible_pct          = Column(Float, default=0.0)   # % non déductible

    # ── 4. TCO pré-calculé (snapshot mensuel) ───────────────────────────────
    monthly_energy_eur          = Column(Float, default=0.0)   # Carburant / électricité
    monthly_indirect_costs_eur  = Column(Float, default=0.0)   # Gestion, amendes, sinistralité
    tco_monthly_eur             = Column(Float, nullable=True)  # TCO total calculé (€/mois)

    # Métadonnées
    notes      = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="leasing_contract")

class MileageLog(Base):
    """Suivi des kilomètres par trajet journalier."""
    __tablename__ = "mileage_logs"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    mileage = Column(Float, nullable=False)
    entry_type = Column(Enum(MileageEntryType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    driver = relationship("Driver", back_populates="mileage_logs")
    vehicle = relationship("Vehicle", back_populates="mileage_logs")

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
    lat = Column(Float)
    lon = Column(Float)
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