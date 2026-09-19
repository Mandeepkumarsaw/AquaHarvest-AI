"""
AquaHarvest AI - Core Configuration & Domain Constants
Built for 1M1B AI for Sustainability Virtual Internship (IBM SkillsBuild & AICTE)
"""

from dataclasses import dataclass
from typing import Dict, List

# Indian Major Cities Rainfall Data (Annual in mm & monthly distribution in %)
# Data referenced from IMD (India Meteorological Department) historical normals
CITY_RAINFALL_DATA: Dict[str, Dict] = {
    "Bangalore": {
        "annual_rainfall_mm": 970,
        "monsoon_days": 65,
        "dry_spell_days": 150,
        "monthly_pct": [0.3, 0.5, 1.2, 4.5, 11.2, 8.1, 11.5, 15.2, 20.8, 17.0, 7.8, 1.9],
        "state": "Karnataka",
        "groundwater_stress": "Critical (Over-exploited)"
    },
    "Chennai": {
        "annual_rainfall_mm": 1400,
        "monsoon_days": 55,
        "dry_spell_days": 180,
        "monthly_pct": [1.8, 0.4, 0.3, 1.0, 2.5, 4.0, 7.5, 9.5, 9.0, 24.5, 29.5, 10.0],
        "state": "Tamil Nadu",
        "groundwater_stress": "Severe (Coastal Saline Ingress)"
    },
    "Delhi NCR": {
        "annual_rainfall_mm": 790,
        "monsoon_days": 35,
        "dry_spell_days": 210,
        "monthly_pct": [1.9, 2.3, 1.8, 1.2, 2.5, 8.5, 30.5, 33.0, 15.0, 1.8, 0.5, 1.0],
        "state": "Delhi / Haryana",
        "groundwater_stress": "Critical (Depleting >1m/yr)"
    },
    "Mumbai": {
        "annual_rainfall_mm": 2420,
        "monsoon_days": 75,
        "dry_spell_days": 210,
        "monthly_pct": [0.0, 0.0, 0.0, 0.1, 0.5, 21.0, 36.5, 25.5, 14.0, 2.2, 0.2, 0.0],
        "state": "Maharashtra",
        "groundwater_stress": "Urban Runoff Flooding / Runoff Wastage"
    },
    "Jaipur": {
        "annual_rainfall_mm": 600,
        "monsoon_days": 30,
        "dry_spell_days": 240,
        "monthly_pct": [1.0, 1.2, 0.8, 0.5, 2.0, 11.0, 35.0, 34.0, 13.0, 1.0, 0.3, 0.2],
        "state": "Rajasthan",
        "groundwater_stress": "Extreme Aridity & Aquifer Depletion"
    },
    "Hyderabad": {
        "annual_rainfall_mm": 820,
        "monsoon_days": 50,
        "dry_spell_days": 170,
        "monthly_pct": [0.5, 0.8, 1.5, 2.5, 4.2, 14.5, 20.5, 22.0, 22.5, 8.5, 2.0, 0.5],
        "state": "Telangana",
        "groundwater_stress": "High Hard-rock Aquifer Stress"
    },
    "Pune": {
        "annual_rainfall_mm": 722,
        "monsoon_days": 60,
        "dry_spell_days": 180,
        "monthly_pct": [0.1, 0.1, 0.4, 1.8, 4.2, 17.5, 28.5, 21.5, 18.0, 6.5, 1.2, 0.2],
        "state": "Maharashtra",
        "groundwater_stress": "Moderate to High"
    },
    "Kolkata": {
        "annual_rainfall_mm": 1600,
        "monsoon_days": 80,
        "dry_spell_days": 150,
        "monthly_pct": [0.8, 1.8, 2.5, 4.5, 10.5, 18.5, 22.5, 21.0, 14.5, 3.0, 0.3, 0.1],
        "state": "West Bengal",
        "groundwater_stress": "Arsenic Risk / Surface Runoff Loss"
    },
    "Ahmedabad": {
        "annual_rainfall_mm": 800,
        "monsoon_days": 35,
        "dry_spell_days": 230,
        "monthly_pct": [0.1, 0.1, 0.2, 0.2, 0.8, 12.0, 38.0, 32.0, 15.0, 1.4, 0.1, 0.1],
        "state": "Gujarat",
        "groundwater_stress": "Over-exploited Semi-Arid"
    }
}

MONTH_NAMES: List[str] = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Runoff Coefficients (C) according to Central Ground Water Board (CGWB) & IS 15797:2008
ROOF_MATERIAL_COEFFICIENTS: Dict[str, Dict] = {
    "Concrete Flat Slab": {
        "coefficient": 0.85,
        "description": "Standard RCC reinforced cement concrete roof. Durable, very high yield.",
        "pre_filtration_need": "Dual-media sand & gravel filter"
    },
    "Terracotta / Clay Tiles": {
        "coefficient": 0.75,
        "description": "Sloped clay or Mangalore tile roofing. Good yield with minor absorption.",
        "pre_filtration_need": "Leaf screen + Dual-media gravel filter"
    },
    "Corrugated GI Sheets": {
        "coefficient": 0.90,
        "description": "Galvanized iron / metal industrial sheeting. Excellent rapid runoff yield.",
        "pre_filtration_need": "First-flush diverter + sediment trap"
    },
    "Grass / Green Roof": {
        "coefficient": 0.20,
        "description": "Vegetated substrate. High water retention, suitable for runoff slowing.",
        "pre_filtration_need": "Specialized bio-retention and multi-layer filter"
    }
}

# Civil Engineering Constants
FIRST_FLUSH_FACTOR_MM = 1.5  # 1.5 mm of rain diverted for dust washing (IS 15797)
FILTER_EFFICIENCY = 0.90     # 90% filtration conveyance efficiency
DAILY_NON_POTABLE_L_PER_CAPITA = 25.0  # Liters per student/staff for flushing & gardening

# Financial & Carbon Constants
DEFAULT_TANKER_CAPACITY_L = 10000
DEFAULT_TANKER_COST_INR = 1400.0  # Standard commercial water tanker cost in Indian metros
CAPEX_COST_PER_LITER_INR = 4.5    # Ferro-cement / masonry modular storage tank cost per liter
BASE_PIPING_COST_INR = 45000.0    # PVC gutters, downspouts, first-flush diverter valve
BASE_FILTER_COST_INR = 35000.0    # Stainless-steel leaf mesh & dual-media filter chamber
RECHARGE_WELL_COST_PER_MTR = 6500.0 # Deep recharge shaft boring & perforated casing per meter

# Emissions
DIESEL_TANKER_ROUND_TRIP_KM = 16.0
CO2_EMISSION_KG_PER_KM = 0.85     # Standard medium diesel truck emissions

# SDG Alignments for 1M1B
SDG_ALIGNMENT = {
    "SDG 6": {
        "title": "Clean Water and Sanitation",
        "target": "Target 6.1 (Safe water access), 6.4 (Water-use efficiency), 6.6 (Aquifer recharge)"
    },
    "SDG 11": {
        "title": "Sustainable Cities and Communities",
        "target": "Target 11.5 (Urban flood risk mitigation), 11.b (Climate resilience)"
    },
    "SDG 12": {
        "title": "Responsible Consumption and Production",
        "target": "Target 12.2 (Efficient circular harvesting of atmospheric precipitation)"
    },
    "SDG 13": {
        "title": "Climate Action",
        "target": "Target 13.1 (Adaptive resilience to severe drought & erratic monsoon shifts)"
    }
}
