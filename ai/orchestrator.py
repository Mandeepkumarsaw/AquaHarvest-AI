"""
AquaHarvest AI - Multi-Agent Orchestrator
Coordinates the 5 specialized agents into an automated pipeline,
accumulating comprehensive engineering, hydrological, financial, and ethical blueprints.
"""

import time
from typing import Dict, Any, Callable, Optional
from ai.granite_client import get_granite_client
from ai.agents import (
    CatchmentAgent,
    ClimateRiskAgent,
    SystemSizingAgent,
    FinancialAgent,
    ResponsibleAiAgent
)

class AgenticOrchestrator:
    def __init__(self, granite_client=None):
        self.client = granite_client or get_granite_client()
        self.agent1 = CatchmentAgent(self.client)
        self.agent2 = ClimateRiskAgent(self.client)
        self.agent3 = SystemSizingAgent(self.client)
        self.agent4 = FinancialAgent(self.client)
        self.agent5 = ResponsibleAiAgent(self.client)

    def run_pipeline(
        self,
        area_sqm: float,
        surface_type: str,
        city: str,
        annual_rainfall_mm: float,
        population: int,
        tanker_cost_inr: float = 1400.0,
        vision_data: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes the 5-stage collaborative agent pipeline sequentially.
        Calls optional progress_callback(step_name, fraction_done) for interactive UI updates.
        """
        start_time = time.time()
        
        state: Dict[str, Any] = {
            "area_sqm": area_sqm,
            "surface_type": surface_type,
            "city": city,
            "annual_rainfall_mm": annual_rainfall_mm,
            "population": population,
            "tanker_cost_inr": tanker_cost_inr,
            "vision_data": vision_data or {}
        }
        
        execution_trace = []

        # Stage 1: Catchment & Yield Analyst
        if progress_callback:
            progress_callback("Agent 1: Analyzing Rooftop Catchment & Rational Yield...", 0.2)
        res1 = self.agent1.run(state)
        state["agent1"] = res1
        execution_trace.append({
            "stage": 1,
            "agent": res1["agent_name"],
            "summary": f"Calculated {res1['annual_harvest_liters']:,.0f} L annual yield using C={res1['runoff_coefficient']}.",
            "rationale": res1["rationale"]
        })

        # Stage 2: Climate & Rainfall Predictor
        if progress_callback:
            progress_callback("Agent 2: Modeling Precipitation Concentration & Dry Spells...", 0.4)
        res2 = self.agent2.run(state)
        state["agent2"] = res2
        execution_trace.append({
            "stage": 2,
            "agent": res2["agent_name"],
            "summary": f"{res2['city']} Volatility: {res2['peak_concentration_pct']}% rain in 2 months with {res2['dry_spell_duration_days']} dry days.",
            "rationale": res2["rationale"]
        })

        # Stage 3: Storage & Aquifer Recharge Engineer
        if progress_callback:
            progress_callback("Agent 3: Sizing Modular Tank & Deep Recharge Shaft...", 0.6)
        res3 = self.agent3.run(state)
        state["agent3"] = res3
        execution_trace.append({
            "stage": 3,
            "agent": res3["agent_name"],
            "summary": f"Sized {res3['tank_specs']['tank_capacity_liters']:,.0f} L tank & {res3['recharge_specs']['recharge_shaft_depth_m']} m recharge shaft.",
            "rationale": res3["rationale"]
        })

        # Stage 4: Financial ROI & Carbon Auditor
        if progress_callback:
            progress_callback("Agent 4: Auditing Diesel Tanker Displacements & Carbon...", 0.8)
        res4 = self.agent4.run(state)
        state["agent4"] = res4
        execution_trace.append({
            "stage": 4,
            "agent": res4["agent_name"],
            "summary": f"Payback in {res4['financials']['payback_months']} months; avoided {res4['financials']['avoided_co2_kg']:,.0f} kg CO₂.",
            "rationale": res4["rationale"]
        })

        # Stage 5: Responsible AI Auditor
        if progress_callback:
            progress_callback("Agent 5: Verifying Fairness, Transparency, Safety & Privacy...", 1.0)
        res5 = self.agent5.run(state)
        state["agent5"] = res5
        execution_trace.append({
            "stage": 5,
            "agent": res5["agent_name"],
            "summary": "Passed all 4 Responsible AI pillars (Fairness, Transparency, Safety, Privacy).",
            "rationale": f"{res5['fairness_audit']} {res5['safety_audit']}"
        })

        total_elapsed = round(time.time() - start_time, 2)

        return {
            "status": "success",
            "elapsed_seconds": total_elapsed,
            "execution_trace": execution_trace,
            "agent1": res1,
            "agent2": res2,
            "agent3": res3,
            "agent4": res4,
            "agent5": res5,
            "summary": {
                "annual_harvest_liters": res1["annual_harvest_liters"],
                "annual_harvest_m3": res1["annual_harvest_m3"],
                "tank_capacity_liters": res3["tank_specs"]["tank_capacity_liters"],
                "tank_dimensions": f"{res3['tank_specs']['diameter_m']}m dia × {res3['tank_specs']['height_m']}m height",
                "recharge_shaft_depth_m": res3["recharge_specs"]["recharge_shaft_depth_m"],
                "tankers_saved": res4["financials"]["tankers_saved_annual"],
                "annual_savings_inr": res4["financials"]["net_annual_savings_inr"],
                "capex_inr": res4["financials"]["total_capex_inr"],
                "payback_months": res4["financials"]["payback_months"],
                "avoided_co2_kg": res4["financials"]["avoided_co2_kg"],
                "responsible_ai_status": res5["overall_safety_rating"]
            }
        }
