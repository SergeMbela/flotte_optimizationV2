import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Vehicle {
    id: number;
    license_plate: string;
    engine_type: string;
    status: string;
    capacity_m3: number;
    purchase_price: number;
}

export interface Driver {
    id: number;
    name: string;
    email: string;
    phone: string;
    home_address: string;
    takes_van_home: boolean;
}

@Injectable({
    providedIn: 'root'
})
export class FleetService {
    private apiUrl = 'http://localhost:8000'; // Make sure this matches your backend

    constructor(private http: HttpClient) { }

    getVehicles(): Observable<Vehicle[]> {
        return this.http.get<Vehicle[]>(`${this.apiUrl}/vehicles/`);
    }

    getDrivers(): Observable<Driver[]> {
        return this.http.get<Driver[]>(`${this.apiUrl}/drivers/`);
    }
}
