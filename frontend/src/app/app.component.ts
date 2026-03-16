import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FleetService, Vehicle, Driver, VehicleModel, EngineType, VehicleStatus, Depot, Parcel, UrgencyLevel } from './fleet.service';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import { fromLonLat } from 'ol/proj';
import { Style, Icon } from 'ol/style';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, AfterViewInit {
  vehicles: Vehicle[] = [];
  drivers: Driver[] = [];
  vehicleModels: VehicleModel[] = [];
  depots: Depot[] = [];
  parcels: Parcel[] = [];
  currentView: string = 'dashboard';

  private map?: Map;
  private vectorSource = new VectorSource();
  
  newModel: VehicleModel = {
    brand: '',
    model_name: ''
  };

  newVehicle: Vehicle = {
    license_plate: '',
    engine_type: EngineType.DIESEL,
    status: VehicleStatus.AVAILABLE,
    capacity_m3: 0,
    purchase_price: 0,
    estimated_residual_value: 0
  };

  newDriver: Driver = {
    name: '',
    email: '',
    phone: '',
    home_address: '',
    takes_van_home: true
  };

  newDepot: Depot = {
    name: '',
    lat: 0,
    lon: 0
  };

  newParcel: Parcel = {
    weight_kg: 0,
    urgency: UrgencyLevel.STANDARD,
    delivery_address: '',
    lat: 0,
    lon: 0
  };

  showForm = false;
  showVehicleForm = false;
  showDriverForm = false;
  showDepotForm = false;
  showParcelForm = false;

  engineTypes = Object.values(EngineType);
  vehicleStatuses = Object.values(VehicleStatus);
  urgencyLevels = Object.values(UrgencyLevel);

  private depotAddressSubject = new Subject<string>();
  private parcelAddressSubject = new Subject<string>();

  constructor(private fleetService: FleetService) { }

  ngOnInit(): void {
    this.refreshData();
    this.initGeocodingDebounce();
  }

  private initGeocodingDebounce(): void {
    this.depotAddressSubject.pipe(
      debounceTime(800),
      distinctUntilChanged()
    ).subscribe(address => {
      if (address) {
        this.fleetService.geocodeAddress(address).subscribe(results => {
          if (results && results.length > 0) {
            this.newDepot.lat = parseFloat(results[0].lat);
            this.newDepot.lon = parseFloat(results[0].lon);
          }
        });
      }
    });

    this.parcelAddressSubject.pipe(
      debounceTime(800),
      distinctUntilChanged()
    ).subscribe(address => {
      if (address) {
        this.fleetService.geocodeAddress(address).subscribe(results => {
          if (results && results.length > 0) {
            this.newParcel.lat = parseFloat(results[0].lat);
            this.newParcel.lon = parseFloat(results[0].lon);
          }
        });
      }
    });
  }

  ngAfterViewInit(): void {
    this.initMap();
  }

  refreshData(): void {
    this.fleetService.getVehicles().subscribe(data => this.vehicles = data);
    this.fleetService.getDrivers().subscribe(data => this.drivers = data);
    this.fleetService.getVehicleModels().subscribe(data => this.vehicleModels = data);
    this.fleetService.getDepots().subscribe(data => {
      this.depots = data;
      if (this.currentView === 'dashboard' || this.currentView === 'maps' || this.currentView === 'tournees') {
        this.updateMapMarkers();
      }
    });
    this.fleetService.getParcels().subscribe(data => {
      this.parcels = data;
      if (this.currentView === 'dashboard' || this.currentView === 'maps' || this.currentView === 'tournees') {
        this.updateMapMarkers();
      }
    });
  }

  setView(view: string): void {
    this.currentView = view;
    if (view === 'dashboard' || view === 'maps' || view === 'tournees') {
      setTimeout(() => {
        if (!this.map) {
          this.initMap();
        } else {
          this.map.setTarget('map');
          this.map.updateSize();
        }
        this.updateMapMarkers();
      }, 0);
    }
  }

  private initMap(): void {
    this.map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        new VectorLayer({
          source: this.vectorSource
        })
      ],
      view: new View({
        center: fromLonLat([4.3517, 50.8503]), // Brussels
        zoom: 8
      })
    });
  }

  private updateMapMarkers(): void {
    if (!this.map) return;
    
    this.vectorSource.clear();
    
    // Depot Markers
    const depotMarkers = this.depots.map(depot => {
      const feature = new Feature({
        geometry: new Point(fromLonLat([depot.lon ?? 0, depot.lat ?? 0])),
        name: depot.name,
        type: 'depot'
      });
      
      feature.setStyle(new Style({
        image: new Icon({
          anchor: [0.5, 1],
          src: 'https://openlayers.org/en/latest/examples/data/icon.png',
          scale: 0.6
        })
      }));
      
      return feature;
    });

    // Parcel Markers
    const parcelMarkers = this.parcels.filter(p => p.lat && p.lon).map(parcel => {
      const feature = new Feature({
        geometry: new Point(fromLonLat([parcel.lon ?? 0, parcel.lat ?? 0])),
        name: parcel.delivery_address,
        type: 'parcel'
      });
      
      feature.setStyle(new Style({
        image: new Icon({
          anchor: [0.5, 1],
          src: 'https://cdn-icons-png.flaticon.com/512/684/684908.png', // Blue marker icon
          scale: 0.05
        })
      }));
      
      return feature;
    });
    
    this.vectorSource.addFeatures([...depotMarkers, ...parcelMarkers]);
  }

  onSubmitModel(): void {
    if (this.newModel.brand && this.newModel.model_name) {
      this.fleetService.createVehicleModel(this.newModel).subscribe(() => {
        this.newModel = { brand: '', model_name: '' };
        this.showForm = false;
        this.refreshData();
      });
    }
  }

  onSubmitVehicle(): void {
    if (this.newVehicle.license_plate && this.newVehicle.engine_type) {
      this.fleetService.createVehicle(this.newVehicle).subscribe(() => {
        this.newVehicle = {
          license_plate: '',
          engine_type: EngineType.DIESEL,
          status: VehicleStatus.AVAILABLE,
          capacity_m3: 0,
          purchase_price: 0,
          estimated_residual_value: 0
        };
        this.showVehicleForm = false;
        this.refreshData();
      });
    }
  }
  onSubmitDriver(): void {
    if (this.newDriver.name) {
      this.fleetService.createDriver(this.newDriver).subscribe(() => {
        this.newDriver = {
          name: '',
          email: '',
          phone: '',
          home_address: '',
          takes_van_home: true
        };
        this.showDriverForm = false;
        this.refreshData();
      });
    }
  }

  onSubmitDepot(): void {
    if (this.newDepot.name && this.newDepot.lat && this.newDepot.lon) {
      this.fleetService.createDepot(this.newDepot).subscribe(() => {
        this.newDepot = { name: '', lat: 0, lon: 0 };
        this.showDepotForm = false;
        this.refreshData();
      });
    }
  }

  onSubmitParcel(): void {
    if (this.newParcel.delivery_address && this.newParcel.weight_kg) {
      this.fleetService.createParcel(this.newParcel).subscribe(() => {
        this.newParcel = {
          weight_kg: 0,
          urgency: UrgencyLevel.STANDARD,
          delivery_address: '',
          lat: 0,
          lon: 0
        };
        this.showParcelForm = false;
        this.refreshData();
      });
    }
  }

  onGeocodeDepot(): void {
    if (this.newDepot.name) {
      this.fleetService.geocodeAddress(this.newDepot.name).subscribe(results => {
        if (results && results.length > 0) {
          this.newDepot.lat = parseFloat(results[0].lat);
          this.newDepot.lon = parseFloat(results[0].lon);
        }
      });
    }
  }

  onGeocodeParcel(): void {
    if (this.newParcel.delivery_address) {
      this.fleetService.geocodeAddress(this.newParcel.delivery_address).subscribe(results => {
        if (results && results.length > 0) {
          this.newParcel.lat = parseFloat(results[0].lat);
          this.newParcel.lon = parseFloat(results[0].lon);
        }
      });
    }
  }

  onDepotAddressChange(address: string): void {
    this.depotAddressSubject.next(address);
  }

  onParcelAddressChange(address: string): void {
    this.parcelAddressSubject.next(address);
  }
}
