import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FleetService, Vehicle, Driver } from './fleet.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  vehicles: Vehicle[] = [];
  drivers: Driver[] = [];

  constructor(private fleetService: FleetService) { }

  ngOnInit(): void {
    this.fleetService.getVehicles().subscribe(data => this.vehicles = data);
    this.fleetService.getDrivers().subscribe(data => this.drivers = data);
  }
}
