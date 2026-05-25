import os
import django
import sys
import random
from datetime import datetime, timedelta

# Set up Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Tenant, EmissionRecord
from ingestion.parsers import parse_sap_data, parse_utility_data, parse_travel_data

def generate():
    Tenant.objects.all().delete()
    EmissionRecord.objects.all().delete()
    
    t1 = Tenant.objects.create(name="Acme Corp (Demo)")
    t2 = Tenant.objects.create(name="Globex Inc (Demo)")

    # 1. SAP Data (Messy)
    sap_raw = [
        {"Menge": "1500.5", "Einheit": "Litre", "Datum": "10.01.2023", "Werk": "P-01"},
        {"Menge": "500", "Einheit": "Gallon", "Datum": "15.02.2023", "Werk": "P-02"},
        {"Amount": "INVALID_NUM", "Unit": "L", "Date": "20.02.2023", "Werk": "P-01"}, # Intentional fail
        {"Menge": "300", "Einheit": "UnknownUnit", "Datum": "10.03.2023", "Werk": "P-01"}, # Unit not recognized
    ]
    sap_records = parse_sap_data(sap_raw, t1)
    
    # 2. Utility Data (Messy)
    utility_raw = [
        {"period_start": "2023-01-01", "period_end": "2023-01-31", "peak_kwh": "4500", "offpeak_kwh": "2100"},
        {"period_start": "2023-02-01", "period_end": "2023-04-30", "peak_kwh": "15000", "offpeak_kwh": "8000"}, # Suspiciously long period
        {"period_start": "2023-05-01", "period_end": "2023-05-31", "peak_kwh": "5000"}, # Missing offpeak
    ]
    utility_records = parse_utility_data(utility_raw, t1)
    
    # 3. Travel Data (Messy)
    travel_raw = [
        {"origin": "SFO", "destination": "JFK", "travel_class": "Economy", "flight_date": "2023-03-15"},
        {"origin": "lhr", "destination": "jfk", "travel_class": "Business", "flight_date": "2023-03-20"},
        {"origin": "XXX", "destination": "YYY", "travel_class": "Economy", "flight_date": "2023-04-10"}, # Unknown route
    ]
    travel_records = parse_travel_data(travel_raw, t1)

    all_records = sap_records + utility_records + travel_records

    for r in all_records:
        EmissionRecord.objects.create(**r)

    print(f"Generated {len(all_records)} records for {t1.name}")

if __name__ == '__main__':
    generate()
