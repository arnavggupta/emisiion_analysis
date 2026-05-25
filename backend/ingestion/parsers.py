import json
from datetime import datetime
from .normalization import normalize_to_co2e
import math

# --- 1. SAP Parser ---
def parse_sap_data(raw_data_list, tenant):
    """
    Handles German headers, obscure date formats, and plant codes.
    Expects dict like: {"Menge": "100", "Einheit": "Litre", "Datum": "15.04.2023", "Werk": "P-01"}
    """
    records = []
    plant_lookup = {"P-01": "Berlin HQ", "P-02": "Munich Factory"}
    
    for row in raw_data_list:
        try:
            # Handle German Headers
            amount = row.get('Menge', row.get('Amount', 0))
            unit = row.get('Einheit', row.get('Unit', 'L'))
            
            # Fix inconsistent units
            if unit.lower() in ['litre', 'litres', 'l']: unit = 'L'
            elif unit.lower() in ['gallons', 'gallon', 'gal']: unit = 'GAL'
            
            # Handle obscure date format (DD.MM.YYYY)
            date_str = row.get('Datum', row.get('Date'))
            date_obj = None
            if date_str:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
                
            # Relational Plant lookup
            plant_code = row.get('Werk', '')
            plant_name = plant_lookup.get(plant_code, "Unknown Plant")
            
            # Normalize
            co2e = normalize_to_co2e('fuel', unit, amount)
            status = 'PENDING' if co2e is not None else 'REJECTED' # Rejected if we can't parse it
            
            records.append({
                "source_system": "SAP",
                "raw_data": row,
                "normalized_unit": "kg CO2e",
                "normalized_value": co2e,
                "scope": "Scope 1",
                "status": status,
                "description": f"Fuel consumption at {plant_name}",
                "date_of_activity": date_obj,
                "tenant": tenant
            })
        except Exception as e:
            # Failed to parse row
            records.append({
                "source_system": "SAP",
                "raw_data": row,
                "scope": "Scope 1",
                "status": "REJECTED",
                "description": f"Failed to parse: {str(e)}",
                "tenant": tenant
            })
    return records


# --- 2. Utility Data Parser ---
def parse_utility_data(raw_data_list, tenant):
    """
    Handles varying units, complex tariffs (peak/off-peak), and overlapping billing periods.
    Expects dict like: {"period_start": "2023-01-15", "period_end": "2023-02-14", "peak_kwh": "5000", "offpeak_kwh": "2000"}
    """
    records = []
    
    for row in raw_data_list:
        try:
            peak = float(row.get('peak_kwh', 0))
            offpeak = float(row.get('offpeak_kwh', 0))
            total_kwh = peak + offpeak
            
            # Normalize (1 kWh = 0.4 kg CO2e)
            co2e = normalize_to_co2e('electricity', 'KWH', total_kwh)
            
            # Detect overlapping/weird periods
            start_date = datetime.strptime(row.get('period_start'), "%Y-%m-%d").date()
            end_date = datetime.strptime(row.get('period_end'), "%Y-%m-%d").date()
            days = (end_date - start_date).days
            
            status = 'PENDING'
            if days > 35 or days < 25:
                # Flag as suspicious if billing period is not ~1 month
                status = 'PENDING' # Will highlight on UI
                
            records.append({
                "source_system": "Utility Portal",
                "raw_data": row,
                "normalized_unit": "kg CO2e",
                "normalized_value": co2e,
                "scope": "Scope 2",
                "status": status,
                "description": f"Electricity ({days} days) - {total_kwh} kWh",
                "date_of_activity": start_date,
                "tenant": tenant
            })
        except Exception as e:
            records.append({
                "source_system": "Utility Portal",
                "raw_data": row,
                "scope": "Scope 2",
                "status": "REJECTED",
                "description": f"Failed to parse: {str(e)}",
                "tenant": tenant
            })
    return records


# --- 3. Corporate Travel Parser ---
# Simple IATA distance mocker (in km)
IATA_DB = {
    ("SFO", "JFK"): 4150,
    ("JFK", "SFO"): 4150,
    ("LHR", "JFK"): 5540,
    ("JFK", "LHR"): 5540,
    ("SFO", "LAX"): 540,
}

def parse_travel_data(raw_data_list, tenant):
    """
    Handles calculating distance from IATA codes.
    Expects dict like: {"origin": "SFO", "destination": "JFK", "travel_class": "Economy"}
    """
    records = []
    
    for row in raw_data_list:
        try:
            origin = row.get('origin', '').upper()
            dest = row.get('destination', '').upper()
            
            # Lookup distance
            distance_km = IATA_DB.get((origin, dest)) or IATA_DB.get((dest, origin))
            
            if distance_km:
                # Add multiplier based on class
                multiplier = 1.5 if row.get('travel_class', '').lower() == 'business' else 1.0
                co2e = normalize_to_co2e('travel', 'KM', distance_km) * multiplier
                status = 'PENDING'
                desc = f"Flight {origin}-{dest} ({distance_km} km)"
            else:
                co2e = None
                status = 'REJECTED'
                desc = f"Unknown route {origin}-{dest}"
                
            date_str = row.get('flight_date')
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

            records.append({
                "source_system": "Concur",
                "raw_data": row,
                "normalized_unit": "kg CO2e",
                "normalized_value": co2e,
                "scope": "Scope 3",
                "status": status,
                "description": desc,
                "date_of_activity": date_obj,
                "tenant": tenant
            })
        except Exception as e:
            records.append({
                "source_system": "Concur",
                "raw_data": row,
                "scope": "Scope 3",
                "status": "REJECTED",
                "description": f"Failed to parse: {str(e)}",
                "tenant": tenant
            })
    return records
