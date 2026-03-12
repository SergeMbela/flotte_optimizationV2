"""
Belgian Fleet Optimizer — Entry Point
======================================
Initialise la base de données et lance l'application.

Usage:
    python main.py                  # Démarre l'app (crée les tables si absentes)
    python main.py --init-db        # Force la (re)création des tables
    python main.py --seed           # Peuple la DB avec des données de test
"""

import argparse
import sys

from db.database import engine, SessionLocal
from db.models import (
    Base,
    Depot, Driver, Vehicle, LeasingContract,
    Parcel, Competitor, CompetitorPrice,
    EngineType, VehicleStatus, ParcelStatus, UrgencyLevel,
)


# ---------------------------------------------------------------------------
# Initialisation DB
# ---------------------------------------------------------------------------

def init_db():
    """Crée toutes les tables définies dans models.py (si elles n'existent pas)."""
    print("📦 Création des tables en base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès.")


# ---------------------------------------------------------------------------
# Données de test (seed)
# ---------------------------------------------------------------------------

def seed_db():
    """Insère un jeu de données minimal pour tester l'application."""
    db = SessionLocal()
    try:
        # Vérifie si des données existent déjà
        if db.query(Depot).count() > 0:
            print("⚠️  La base contient déjà des données. Seed annulé.")
            return

        print("🌱 Insertion des données de test...")

        # --- Dépôts ---
        depots = [
            Depot(name="Dépôt Bruxelles", lat=50.8503, lon=4.3517),
            Depot(name="Dépôt Liège",     lat=50.6326, lon=5.5797),
            Depot(name="Dépôt Gand",      lat=51.0543, lon=3.7174),
        ]
        db.add_all(depots)

        # --- Chauffeurs ---
        drivers = [
            Driver(
                name="Jean Dupont",
                email="jean.dupont@flotte.be",
                phone="+32 477 11 22 33",
                home_address="Rue de la Loi 1, 1000 Bruxelles",
                home_lat=50.8462, home_lon=4.3525,
                takes_van_home=True,
            ),
            Driver(
                name="Marie Lecomte",
                email="marie.lecomte@flotte.be",
                phone="+32 477 44 55 66",
                home_address="Quai de Rome 12, 4000 Liège",
                home_lat=50.6258, home_lon=5.5736,
                takes_van_home=False,
            ),
        ]
        db.add_all(drivers)

        # --- Véhicules ---
        van1 = Vehicle(
            license_plate="1-ABC-123",
            engine_type=EngineType.DIESEL,
            status=VehicleStatus.AVAILABLE,
            capacity_m3=12.5,
            purchase_price=45000.0,
            estimated_residual_value=15000.0,
        )
        van2 = Vehicle(
            license_plate="2-XYZ-456",
            engine_type=EngineType.ELECTRIC,
            status=VehicleStatus.AVAILABLE,
            capacity_m3=10.0,
            purchase_price=65000.0,
            estimated_residual_value=30000.0,
        )
        db.add_all([van1, van2])
        db.flush()  # génère les IDs

        # --- Contrats de leasing ---
        db.add(LeasingContract(
            vehicle_id=van1.id,
            monthly_fee=650.0,
            max_monthly_km=3000,
            penalty_per_km_eur=0.12,
        ))

        # --- Colis ---
        parcels = [
            Parcel(
                weight_kg=2.5, length_cm=30, width_cm=20, height_cm=15,
                urgency=UrgencyLevel.STANDARD,
                delivery_address="Avenue Louise 54, 1050 Bruxelles",
                price_charged=8.50,
            ),
            Parcel(
                weight_kg=0.8, length_cm=20, width_cm=15, height_cm=10,
                urgency=UrgencyLevel.EXPRESS,
                delivery_address="Rue Neuve 12, 1000 Bruxelles",
                price_charged=14.90,
            ),
        ]
        db.add_all(parcels)

        # --- Concurrent ---
        bpost = Competitor(name="Bpost")
        db.add(bpost)
        db.flush()

        db.add_all([
            CompetitorPrice(
                competitor_id=bpost.id,
                urgency=UrgencyLevel.STANDARD,
                base_fee=3.50, per_kg_fee=0.80,
            ),
            CompetitorPrice(
                competitor_id=bpost.id,
                urgency=UrgencyLevel.EXPRESS,
                base_fee=7.00, per_kg_fee=1.20,
            ),
        ])

        db.commit()
        print("✅ Données de test insérées avec succès.")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors du seed : {e}")
        raise
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Point d'entrée principal
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Belgian Fleet Optimizer")
    parser.add_argument("--init-db", action="store_true", help="Crée les tables SQL")
    parser.add_argument("--seed",    action="store_true", help="Insère des données de test")
    args = parser.parse_args()

    # Toujours s'assurer que les tables existent
    init_db()

    if args.seed:
        seed_db()

    if not args.init_db and not args.seed:
        print("\n🚀 Belgian Fleet Optimizer — prêt.")
        print("   Utilisez --seed pour insérer des données de test.")
        print("   Connectez-vous à Adminer sur http://localhost:8082\n")


if __name__ == "__main__":
    main()
