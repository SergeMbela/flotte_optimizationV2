from sqlalchemy.orm import Session
from sqlalchemy import func
from db import models

def calculate_parcel_price(db: Session, weight_kg: float, urgency: models.UrgencyLevel):
    print(f"DEBUG: calculate_parcel_price called with weight={weight_kg}, urgency={urgency} (type={type(urgency)})")
    
    # Ensure urgency is the Enum member if it came as a string
    if isinstance(urgency, str):
        try:
            urgency = models.UrgencyLevel(urgency)
        except ValueError:
            print(f"DEBUG: invalid urgency string '{urgency}', falling back to STANDARD")
            urgency = models.UrgencyLevel.STANDARD
            
    # query for average benchmark
    benchmark = db.query(
        func.avg(models.CompetitorPrice.base_fee).label("avg_base"),
        func.avg(models.CompetitorPrice.per_kg_fee).label("avg_kg")
    ).filter(models.CompetitorPrice.urgency == urgency).first()
    
    if benchmark and benchmark.avg_base is not None:
        base_fee = float(benchmark.avg_base)
        per_kg_fee = float(benchmark.avg_kg)
    else:
        # Fallback values if no benchmark is available
        fallbacks = {
            models.UrgencyLevel.STANDARD: (5.0, 1.0),
            models.UrgencyLevel.EXPRESS: (10.0, 2.0),
            models.UrgencyLevel.SAME_DAY: (20.0, 5.0)
        }
        base_fee, per_kg_fee = fallbacks.get(urgency, (5.0, 1.0))
    
    price = base_fee + (weight_kg * per_kg_fee)
    print(f"DEBUG: Calculated price: {price} (base={base_fee}, per_kg={per_kg_fee})")
    return round(price, 2)
