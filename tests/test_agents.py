"""
Unit Tests for Multi-Agent Orchestration Pipeline
"""

import unittest
from ai.orchestrator import AgenticOrchestrator
from ai.granite_client import GraniteClient

class TestAgentPipeline(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AgenticOrchestrator(granite_client=GraniteClient())

    def test_multi_agent_sequential_execution(self):
        output = self.orchestrator.run_pipeline(
            area_sqm=2000,
            surface_type="Concrete Flat Slab",
            city="Chennai",
            annual_rainfall_mm=1400,
            population=1200,
            tanker_cost_inr=1500.0
        )
        
        # Check pipeline success
        self.assertEqual(output["status"], "success")
        self.assertEqual(len(output["execution_trace"]), 5)
        
        # Verify Agent 1 output
        self.assertIn("agent1", output)
        self.assertGreater(output["agent1"]["annual_harvest_liters"], 0)
        
        # Verify Agent 2 output
        self.assertIn("agent2", output)
        self.assertEqual(output["agent2"]["city"], "Chennai")
        
        # Verify Agent 3 output
        self.assertIn("agent3", output)
        self.assertGreater(output["agent3"]["tank_specs"]["tank_capacity_liters"], 0)
        
        # Verify Agent 4 output
        self.assertIn("agent4", output)
        self.assertGreater(output["agent4"]["financials"]["tankers_saved_annual"], 0)
        self.assertGreater(output["agent4"]["financials"]["payback_months"], 0)
        
        # Verify Agent 5 output
        self.assertIn("agent5", output)
        self.assertIn("Passed", output["agent5"]["overall_safety_rating"])

if __name__ == "__main__":
    unittest.main()
