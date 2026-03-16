from db import models

def calculate_tco(contract_data):
    """
    Calculates the Total Cost of Ownership (TCO) per month.
    
    Formula:
    Operational Costs: Loyer + Maintenance + Assurance + Remplacement
    Fiscalité (mensualisée): (CO2 tax + Age tax) / 12
    Énergie & Indirects: Energy + Indirects
    """
    operational_costs = (
        (contract_data.monthly_fee or 0.0) +
        (contract_data.monthly_maintenance_eur or 0.0) +
        (contract_data.monthly_insurance_eur or 0.0) +
        (contract_data.monthly_replacement_veh_eur or 0.0)
    )
    
    taxes = (
        (contract_data.co2_tax_annual_eur or 0.0) / 12.0 +
        (contract_data.age_tax_annual_eur or 0.0) / 12.0
    )
    
    other_costs = (
        (contract_data.monthly_energy_eur or 0.0) +
        (contract_data.monthly_indirect_costs_eur or 0.0)
    )
    
    return operational_costs + taxes + other_costs
