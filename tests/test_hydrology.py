"""
Unit Tests for Deterministic Hydrological Engine
"""

import unittest
from core.hydrology_math import (
    calculate_harvestable_yield,
    calculate_first_flush_volume,
    calculate_campus_demand,
    calculate_optimal_storage_tank,
    calculate_financials_and_carbon,
    run_full_hydrology_pipeline
)

class TestHydrologyMath(unittest.TestCase):
    def test_harvestable_yield_formula(self):
        # Area = 1000 sqm, Rainfall = 1000 mm, C = 0.85, eta = 0.90
        # Expected = 1000 * 1000 * 0.85 * 0.90 = 765,000 Liters
        val = calculate_harvestable_yield(1000, 1000, 0.85, 0.90)
        self.assertAlmostEqual(val, 765000.0, places=1)

    def test_zero_and_negative_inputs(self):
        self.assertEqual(calculate_harvestable_yield(-50, 1000, 0.85), 0.0)
        self.assertEqual(calculate_harvestable_yield(1000, -100, 0.85), 0.0)
        self.assertEqual(calculate_harvestable_yield(1000, 1000, -0.5), 0.0)

    def test_first_flush_volume(self):
        # Area = 2000 sqm * 1.5 mm = 3000 Liters
        ff = calculate_first_flush_volume(2000, factor_mm=1.5)
        self.assertEqual(ff, 3000.0)

    def test_campus_demand(self):
        demand = calculate_campus_demand(1000, per_capita_lpd=25.0)
        self.assertEqual(demand["daily_demand_liters"], 25000.0)
        self.assertEqual(demand["annual_demand_liters"], 25000.0 * 365.0)

    def test_optimal_tank_sizing(self):
        # Harvest = 1,000,000 L, Daily Demand = 20,000 L
        # Inflow cap = 250,000 L; Demand 21 days = 420,000 L -> min is 250,000 L
        tank = calculate_optimal_storage_tank(1000000.0, 20000.0, buffer_days=21)
        self.assertEqual(tank["tank_capacity_liters"], 250000.0)
        self.assertGreater(tank["diameter_m"], 0.0)
        self.assertEqual(tank["height_m"], 2.5)

    def test_financial_payback_validity(self):
        fin = calculate_financials_and_carbon(
            harvestable_yield_l=1500000.0,
            tank_capacity_l=300000.0,
            recharge_depth_m=9.0,
            tanker_cost_inr=1400.0
        )
        self.assertGreater(fin["tankers_saved_annual"], 0)
        self.assertGreater(fin["annual_gross_savings_inr"], 0)
        self.assertGreater(fin["total_capex_inr"], 0)
        self.assertGreater(fin["payback_months"], 0)
        self.assertGreater(fin["avoided_co2_kg"], 0)

    def test_full_pipeline_execution(self):
        res = run_full_hydrology_pipeline(
            area_sqm=2500,
            surface_type="Concrete Flat Slab",
            city_name="Bangalore",
            population=1500
        )
        self.assertIn("harvestable_yield_liters", res)
        self.assertGreater(res["harvestable_yield_liters"], 1000000)
        self.assertEqual(len(res["monthly_chart_data"]), 12)

if __name__ == "__main__":
    unittest.main()
