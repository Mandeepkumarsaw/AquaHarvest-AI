"""
AquaHarvest AI - Hydrological Civil Engineering Math Engine
Deterministic calculations based on Central Ground Water Board (CGWB)
and Bureau of Indian Standards IS 15797:2008
"""

import math
from typing import Dict, List, Any
from core.config import (
    CITY_RAINFALL_DATA,
    ROOF_MATERIAL_COEFFICIENTS,
    MONTH_NAMES,
    FIRST_FLUSH_FACTOR_MM,
    FILTER_EFFICIENCY,
    DAILY_NON_POTABLE_L_PER_CAPITA,
    DEFAULT_TANKER_CAPACITY_L,
    DEFAULT_TANKER_COST_INR,
    CAPEX_COST_PER_LITER_INR,
    BASE_PIPING_COST_INR,
    BASE_FILTER_COST_INR,
    RECHARGE_WELL_COST_PER_MTR,
    DIESEL_TANKER_ROUND_TRIP_KM,
    CO2_EMISSION_KG_PER_KM
)

def calculate_harvestable_yield(
    area_sqm: float,
    annual_rainfall_mm: float,
    runoff_coefficient: float,
    filter_efficiency: float = FILTER_EFFICIENCY
) -> float:
    """
    Computes annual gross harvestable rainwater volume in Liters using the Rational Method:
    V_harvest = Area (m^2) * Rainfall (mm) * Runoff_Coeff (C) * Filter_Efficiency (eta)
    Note: 1 m^2 * 1 mm of rain = 1 Liter of water.
    """
    if area_sqm < 0 or annual_rainfall_mm < 0 or runoff_coefficient < 0:
        return 0.0
    return float(area_sqm * annual_rainfall_mm * runoff_coefficient * filter_efficiency)


def calculate_first_flush_volume(area_sqm: float, factor_mm: float = FIRST_FLUSH_FACTOR_MM) -> float:
    """
    Computes first-flush diversion volume in Liters per rain event.
    IS 15797:2008 recommends diverting the first 1.0 - 2.0 mm of rainfall to remove debris and dust.
    V_first_flush = Area (m^2) * 1.5 mm
    """
    return float(max(0.0, area_sqm * factor_mm))


def calculate_campus_demand(population: int, per_capita_lpd: float = DAILY_NON_POTABLE_L_PER_CAPITA) -> Dict[str, float]:
    """
    Computes daily and annual non-potable campus water demand (flushing, gardening, grounds maintenance).
    """
    daily = max(0, population) * per_capita_lpd
    annual = daily * 365.0
    return {
        "daily_demand_liters": float(daily),
        "annual_demand_liters": float(annual)
    }


def calculate_optimal_storage_tank(
    harvestable_yield_l: float,
    daily_demand_l: float,
    buffer_days: int = 21
) -> Dict[str, Any]:
    """
    Optimal storage tank sizing using the Cumulative Inflow Deficit method.
    Balances peak monsoon capture vs. 21-day dry season buffer:
    V_tank = min(V_harvest * 0.25, Daily_Demand * buffer_days)
    """
    # 25% of annual harvest or 21 days of operational buffer
    recommended_l = min(harvestable_yield_l * 0.25, daily_demand_l * buffer_days)
    # Ensure a reasonable minimum if campus is small
    recommended_l = max(5000.0, recommended_l) if harvestable_yield_l > 0 else 0.0
    
    vol_m3 = recommended_l / 1000.0
    
    # Physical dimensions assuming standard cylinder of height 2.5m
    tank_height_m = 2.5
    if vol_m3 > 0:
        radius_m = math.sqrt(vol_m3 / (math.pi * tank_height_m))
        diameter_m = 2.0 * radius_m
    else:
        radius_m = 0.0
        diameter_m = 0.0
        
    return {
        "tank_capacity_liters": round(recommended_l, 0),
        "tank_capacity_m3": round(vol_m3, 2),
        "height_m": tank_height_m,
        "diameter_m": round(diameter_m, 2),
        "buffer_days_provided": round(recommended_l / daily_demand_l, 1) if daily_demand_l > 0 else 0
    }


def calculate_aquifer_recharge_potential(
    harvestable_yield_l: float,
    tank_capacity_l: float,
    area_sqm: float
) -> Dict[str, Any]:
    """
    Excess monsoon runoff diverted into engineered groundwater recharge pit.
    """
    # Excess water that exceeds tank cyclical retention capacity goes to recharge
    annual_recharge_l = max(0.0, harvestable_yield_l - tank_capacity_l)
    
    # Recommended recharge shaft depth: min 6m, scaling with campus size
    depth_m = 6.0 if area_sqm < 2000 else (9.0 if area_sqm < 5000 else 12.0)
    filter_diameter_m = 1.5 if area_sqm < 3000 else 2.5
    
    return {
        "annual_recharge_liters": round(annual_recharge_l, 0),
        "annual_recharge_m3": round(annual_recharge_l / 1000.0, 2),
        "recharge_shaft_depth_m": depth_m,
        "filter_chamber_dia_m": filter_diameter_m,
        "filtration_layers": [
            {"layer": "Bottom", "material": "Clean River Boulders (50-100 mm)", "thickness_cm": 50},
            {"layer": "Middle", "material": "Coarse Gravel (10-20 mm)", "thickness_cm": 40},
            {"layer": "Top", "material": "Coarse Silica Sand (1.5-2 mm)", "thickness_cm": 40}
        ]
    }


def calculate_financials_and_carbon(
    harvestable_yield_l: float,
    tank_capacity_l: float,
    recharge_depth_m: float,
    tanker_cost_inr: float = DEFAULT_TANKER_COST_INR
) -> Dict[str, Any]:
    """
    Financial Return on Investment (ROI) and Carbon Offset calculations.
    """
    # Tankers replaced annually (10,000L per commercial tanker)
    tankers_saved = harvestable_yield_l / DEFAULT_TANKER_CAPACITY_L
    annual_savings_inr = tankers_saved * tanker_cost_inr
    
    # Capital Expenditure (CapEx)
    tank_cost = tank_capacity_l * CAPEX_COST_PER_LITER_INR
    recharge_cost = recharge_depth_m * RECHARGE_WELL_COST_PER_MTR
    total_capex = tank_cost + BASE_PIPING_COST_INR + BASE_FILTER_COST_INR + recharge_cost
    
    # Operating Expenditure (OpEx): ~4% of CapEx for cleaning & filter media replacement
    annual_opex = total_capex * 0.04
    net_annual_savings = max(0.0, annual_savings_inr - annual_opex)
    
    # Payback Period in years
    payback_years = (total_capex / net_annual_savings) if net_annual_savings > 0 else 99.0
    payback_months = round(payback_years * 12.0, 1)
    
    # 5-Year Cumulative Savings
    five_year_savings = (net_annual_savings * 5.0) - total_capex
    
    # Carbon Offset (diesel truck transport avoided)
    avoided_km = tankers_saved * DIESEL_TANKER_ROUND_TRIP_KM
    avoided_co2_kg = avoided_km * CO2_EMISSION_KG_PER_KM
    
    return {
        "tankers_saved_annual": round(tankers_saved, 1),
        "annual_gross_savings_inr": round(annual_savings_inr, 2),
        "annual_opex_inr": round(annual_opex, 2),
        "net_annual_savings_inr": round(net_annual_savings, 2),
        "total_capex_inr": round(total_capex, 2),
        "payback_years": round(payback_years, 2),
        "payback_months": payback_months,
        "five_year_net_savings_inr": round(five_year_savings, 2),
        "avoided_co2_kg": round(avoided_co2_kg, 1),
        "avoided_diesel_km": round(avoided_km, 1)
    }


def compute_monthly_distribution(
    annual_yield_l: float,
    monthly_demand_l: float,
    city_name: str
) -> List[Dict[str, Any]]:
    """
    Computes month-by-month inflow, demand, and storage balance for plotting.
    """
    city_info = CITY_RAINFALL_DATA.get(city_name, CITY_RAINFALL_DATA["Bangalore"])
    monthly_pct = city_info["monthly_pct"]
    
    results = []
    for i, month in enumerate(MONTH_NAMES):
        inflow = annual_yield_l * (monthly_pct[i] / 100.0)
        net_balance = inflow - monthly_demand_l
        results.append({
            "month": month,
            "rainfall_pct": monthly_pct[i],
            "inflow_liters": round(inflow, 0),
            "demand_liters": round(monthly_demand_l, 0),
            "balance_liters": round(net_balance, 0),
            "status": "Surplus" if net_balance >= 0 else "Deficit"
        })
    return results


def run_full_hydrology_pipeline(
    area_sqm: float,
    surface_type: str,
    city_name: str,
    population: int,
    custom_rainfall_mm: float = None,
    tanker_cost_inr: float = DEFAULT_TANKER_COST_INR
) -> Dict[str, Any]:
    """
    Master pipeline executing the full hydrological and civil engineering calculation.
    """
    # Retrieve city parameters
    city_data = CITY_RAINFALL_DATA.get(city_name, CITY_RAINFALL_DATA["Bangalore"])
    rainfall_mm = custom_rainfall_mm if custom_rainfall_mm and custom_rainfall_mm > 0 else city_data["annual_rainfall_mm"]
    
    # Runoff coefficient
    coeff_data = ROOF_MATERIAL_COEFFICIENTS.get(surface_type, ROOF_MATERIAL_COEFFICIENTS["Concrete Flat Slab"])
    c_coeff = coeff_data["coefficient"]
    
    # 1. Harvestable yield
    yield_l = calculate_harvestable_yield(area_sqm, rainfall_mm, c_coeff)
    first_flush_l = calculate_first_flush_volume(area_sqm)
    
    # 2. Demand
    demand = calculate_campus_demand(population)
    daily_demand_l = demand["daily_demand_liters"]
    annual_demand_l = demand["annual_demand_liters"]
    
    # 3. Storage Tank Sizing
    tank = calculate_optimal_storage_tank(yield_l, daily_demand_l)
    
    # 4. Aquifer Recharge
    recharge = calculate_aquifer_recharge_potential(yield_l, tank["tank_capacity_liters"], area_sqm)
    
    # 5. Financials & Carbon
    finance = calculate_financials_and_carbon(
        yield_l,
        tank["tank_capacity_liters"],
        recharge["recharge_shaft_depth_m"],
        tanker_cost_inr
    )
    
    # 6. Monthly distribution
    monthly = compute_monthly_distribution(yield_l, daily_demand_l * 30.4, city_name)
    
    # Water security percentage
    security_pct = min(100.0, (yield_l / annual_demand_l * 100.0)) if annual_demand_l > 0 else 0.0
    
    return {
        "inputs": {
            "area_sqm": area_sqm,
            "surface_type": surface_type,
            "runoff_coefficient": c_coeff,
            "city": city_name,
            "annual_rainfall_mm": rainfall_mm,
            "population": population,
            "tanker_cost_inr": tanker_cost_inr
        },
        "harvestable_yield_liters": round(yield_l, 0),
        "harvestable_yield_m3": round(yield_l / 1000.0, 2),
        "first_flush_liters": round(first_flush_l, 0),
        "daily_demand_liters": round(daily_demand_l, 0),
        "annual_demand_liters": round(annual_demand_l, 0),
        "water_security_pct": round(security_pct, 1),
        "tank_specs": tank,
        "recharge_specs": recharge,
        "financials": finance,
        "monthly_chart_data": monthly
    }
