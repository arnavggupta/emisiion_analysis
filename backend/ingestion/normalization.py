# A simple Mock Normalization Engine for Emissions
# Real-world scenarios would use an external API like Climatiq or EPA factors DB.

EMISSION_FACTORS = {
    'fuel': {
        'L': 2.68,       # 1 Liter Diesel = 2.68 kg CO2e
        'GAL': 10.15,    # 1 Gallon Diesel = 10.15 kg CO2e
        'KG': 3.1,       # 1 KG Coal = 3.1 kg CO2e
    },
    'electricity': {
        'KWH': 0.4,      # 1 kWh = ~0.4 kg CO2e
        'MWH': 400.0,    # 1 MWh = 400 kg CO2e
    },
    'travel': {
        'KM': 0.15,      # 1 KM Flight = 0.15 kg CO2e
        'MI': 0.24,      # 1 Mile Flight = 0.24 kg CO2e
    }
}

def normalize_to_co2e(category, unit, value):
    """
    Normalizes a given value and unit into standard kg CO2e.
    Category: 'fuel', 'electricity', or 'travel'
    Unit: e.g., 'L', 'KWH', 'KM'
    Value: numeric amount
    Returns a float representing kg CO2e, or None if unknown unit.
    """
    if not value or pd_is_nan(value):
        return None
        
    try:
        val = float(value)
    except (ValueError, TypeError):
        return None

    cat_factors = EMISSION_FACTORS.get(category.lower())
    if not cat_factors:
        return None

    factor = cat_factors.get(unit.upper())
    if not factor:
        return None

    return round(val * factor, 2)

def pd_is_nan(val):
    # simple check to avoid pandas dependency if not needed
    try:
        import math
        return math.isnan(val)
    except TypeError:
        return False
