"""
Unit Tests for Multimodal Computer Vision Classifier
Verifies accurate discrimination between genuine catchments and solid waste/garbage.
"""

import unittest
from core.multimodal_vision import analyze_rooftop_image, ensure_sample_roof_image

class TestVisionClassifier(unittest.TestCase):
    def setUp(self):
        self.sample_roof = ensure_sample_roof_image()
        self.test_garbage = "assets/test_garbage_crop.png"

    def test_clean_concrete_roof_classified_correctly(self):
        res = analyze_rooftop_image(self.sample_roof)
        self.assertTrue(res["is_valid_catchment"])
        self.assertEqual(res["surface_type"], "Concrete Flat Slab")
        self.assertEqual(res["runoff_coefficient"], 0.85)
        self.assertGreater(res["confidence_pct"], 80.0)
        self.assertGreater(res["surface_integrity_score"], 70)
        self.assertIsNone(res["safety_alert"])

    def test_garbage_image_rejected_as_hazard(self):
        import os
        if os.path.exists(self.test_garbage):
            res = analyze_rooftop_image(self.test_garbage)
            self.assertFalse(res["is_valid_catchment"])
            self.assertEqual(res["runoff_coefficient"], 0.0)
            self.assertGreater(res["waste_detection_confidence_pct"], 85.0)
            self.assertLess(res["surface_integrity_score"], 30)
            self.assertIsNotNone(res["safety_alert"])
            self.assertIn("Solid Waste", res["surface_type"])

if __name__ == "__main__":
    unittest.main()
