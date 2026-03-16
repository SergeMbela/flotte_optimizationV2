import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export enum EngineType {
    DIESEL = "DIESEL",
    PETROL = "PETROL",
    ELECTRIC = "ELECTRIC"
}

export enum VehicleStatus {
    AVAILABLE = "AVAILABLE",
    IN_MAINTENANCE = "IN_MAINTENANCE",
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
}

export enum ParcelStatus {
    PENDING = "PENDING",
    IN_TRANSIT = "IN_TRANSIT",
    DELIVERED = "DELIVERED",
    REFUSED = "REFUSED",
    LOST = "LOST"
}

export enum UrgencyLevel {
    STANDARD = "STANDARD",
    EXPRESS = "EXPRESS",
    SAME_DAY = "SAME_DAY"
}

export enum MileageEntryType {
    DEPOT_DEPARTURE = "DEPOT_DEPARTURE",
    LAST_DELIVERY = "LAST_DELIVERY"
}

export enum LeaveType {
    PAID = "CONGÉ PAYÉ",
    SICK = "MALADIE",
    UNPAID = "SANS SOLDE",
    RECOVERY = "RÉCUPÉRATION"
}

export enum LeaveStatus {
    PENDING = "EN ATTENTE",
    APPROVED = "APPROUVÉ",
    REJECTED = "REFUSÉ"
}

export interface Depot {
    id?: number;
    name: string;
    lat: number;
    lon: number;
}

export interface VehicleModel {
    id?: number;
    brand: string;
    model_name: string;
}

export interface Driver {
    id?: number;
    name: string;
    email?: string;
    phone?: string;
    home_address?: string;
    home_lat?: number;
    home_lon?: number;
    driven_minutes_today?: number;
    takes_van_home: boolean;
}

export interface Leave {
    id?: number;
    driver_id: number;
    leave_type: LeaveType;
    start_date: string; // ISO format
    end_date: string;   // ISO format
    status?: LeaveStatus;
    reason?: string;
}

export interface Vehicle {
    id?: number;
    license_plate: string;
    model_id?: number;
    engine_type: EngineType;
    status: VehicleStatus;
    capacity_m3: number;
    purchase_price: number;
    estimated_residual_value: number;
    vehicle_model?: VehicleModel;
}

export interface LeasingContract {
    id?: number;
    vehicle_id: number;
    contract_months: number;
    max_monthly_km: number;
    annual_rate_pct: number;
    monthly_fee: number;
    penalty_per_km_eur: number;
    monthly_maintenance_eur: number;
    monthly_insurance_eur: number;
    monthly_replacement_veh_eur: number;
    vat_recovery_pct: number;
    co2_tax_annual_eur: number;
    age_tax_annual_eur: number;
    non_deductible_pct: number;
    monthly_energy_eur: number;
    monthly_indirect_costs_eur: number;
    notes?: string;
    tco_monthly_eur?: number;
    created_at?: string;
    updated_at?: string;
}

export interface Parcel {
    id?: number;
    weight_kg: number;
    length_cm?: number;
    width_cm?: number;
    height_cm?: number;
    urgency: UrgencyLevel;
    delivery_address: string;
    lat?: number;
    lon?: number;
    status?: ParcelStatus;
    price_charged?: number;
    created_at?: string;
}

export interface MileageLog {
    id?: number;
    driver_id: number;
    vehicle_id: number;
    mileage: number;
    entry_type: MileageEntryType;
    timestamp?: string;
}

export interface CompetitorPrice {
    id?: number;
    competitor_id: number;
    urgency: UrgencyLevel;
    base_fee: number;
    per_kg_fee: number;
    updated_at?: string;
}

export interface Competitor {
    id?: number;
    name: string;
    prices?: CompetitorPrice[];
}

@Injectable({
    providedIn: 'root'
})
export class FleetService {
    private apiUrl = 'http://localhost:8000'; // Matches backend in docker-compose

    constructor(private http: HttpClient) { }

    // Depots
    getDepots(skip = 0, limit = 100): Observable<Depot[]> {
        return this.http.get<Depot[]>(`${this.apiUrl}/depots/`, { params: { skip, limit } });
    }

    createDepot(depot: Depot): Observable<Depot> {
        return this.http.post<Depot>(`${this.apiUrl}/depots/`, depot);
    }

    // Vehicle Models
    getVehicleModels(skip = 0, limit = 100): Observable<VehicleModel[]> {
        return this.http.get<VehicleModel[]>(`${this.apiUrl}/vehicle_models/`, { params: { skip, limit } });
    }

    createVehicleModel(model: VehicleModel): Observable<VehicleModel> {
        return this.http.post<VehicleModel>(`${this.apiUrl}/vehicle_models/`, model);
    }

    // Vehicles
    getVehicles(skip = 0, limit = 100): Observable<Vehicle[]> {
        return this.http.get<Vehicle[]>(`${this.apiUrl}/vehicles/`, { params: { skip, limit } });
    }

    getVehicle(id: number): Observable<Vehicle> {
        return this.http.get<Vehicle>(`${this.apiUrl}/vehicles/${id}`);
    }

    createVehicle(vehicle: Vehicle): Observable<Vehicle> {
        return this.http.post<Vehicle>(`${this.apiUrl}/vehicles/`, vehicle);
    }

    // Drivers
    getDrivers(skip = 0, limit = 100): Observable<Driver[]> {
        return this.http.get<Driver[]>(`${this.apiUrl}/drivers/`, { params: { skip, limit } });
    }

    getDriver(id: number): Observable<Driver> {
        return this.http.get<Driver>(`${this.apiUrl}/drivers/${id}`);
    }

    createDriver(driver: Driver): Observable<Driver> {
        return this.http.post<Driver>(`${this.apiUrl}/drivers/`, driver);
    }

    // Parcels
    getParcels(skip = 0, limit = 100): Observable<Parcel[]> {
        return this.http.get<Parcel[]>(`${this.apiUrl}/parcels/`, { params: { skip, limit } });
    }

    createParcel(parcel: Parcel): Observable<Parcel> {
        return this.http.post<Parcel>(`${this.apiUrl}/parcels/`, parcel);
    }

    // Mileage Logs
    getMileageLogs(skip = 0, limit = 100): Observable<MileageLog[]> {
        return this.http.get<MileageLog[]>(`${this.apiUrl}/mileage_logs/`, { params: { skip, limit } });
    }

    createMileageLog(log: MileageLog): Observable<MileageLog> {
        return this.http.post<MileageLog>(`${this.apiUrl}/mileage_logs/`, log);
    }

    // Leaves
    getLeaves(skip = 0, limit = 100): Observable<Leave[]> {
        return this.http.get<Leave[]>(`${this.apiUrl}/leaves/`, { params: { skip, limit } });
    }

    createLeave(leave: Leave): Observable<Leave> {
        return this.http.post<Leave>(`${this.apiUrl}/leaves/`, leave);
    }

    updateLeaveStatus(leaveId: number, status: LeaveStatus): Observable<Leave> {
        return this.http.patch<Leave>(`${this.apiUrl}/leaves/${leaveId}`, { status });
    }

    // Leasing Contracts
    getLeasingContracts(skip = 0, limit = 100): Observable<LeasingContract[]> {
        return this.http.get<LeasingContract[]>(`${this.apiUrl}/leasing_contracts/`, { params: { skip, limit } });
    }

    createLeasingContract(contract: LeasingContract): Observable<LeasingContract> {
        return this.http.post<LeasingContract>(`${this.apiUrl}/leasing_contracts/`, contract);
    }

    // Competitors
    getCompetitors(skip = 0, limit = 100): Observable<Competitor[]> {
        return this.http.get<Competitor[]>(`${this.apiUrl}/competitors/`, { params: { skip, limit } });
    }

    createCompetitor(competitor: Competitor): Observable<Competitor> {
        return this.http.post<Competitor>(`${this.apiUrl}/competitors/`, competitor);
    }

    createCompetitorPrice(price: CompetitorPrice): Observable<CompetitorPrice> {
        return this.http.post<CompetitorPrice>(`${this.apiUrl}/competitor_prices/`, price);
    }

    // Geocoding
    geocodeAddress(address: string): Observable<any[]> {
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`;
        return this.http.get<any[]>(url);
    }
}
