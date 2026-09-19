"""
Unit Tests for RAG Knowledge Base and Vector Store
"""

import unittest
from rag.vector_store import get_rag_store

class TestRAGRetriever(unittest.TestCase):
    def setUp(self):
        self.store = get_rag_store()

    def test_knowledge_base_indexing(self):
        self.assertTrue(self.store.is_indexed)
        self.assertGreater(len(self.store.chunks), 0)

    def test_retrieve_runoff_coefficient_query(self):
        query = "What is the runoff coefficient of a concrete roof?"
        results = self.store.retrieve_relevant_bylaws(query, top_k=3)
        self.assertGreater(len(results), 0)
        
        # At least one result should mention concrete or runoff coefficient
        combined_text = " ".join([r["text"] for r in results]).lower()
        self.assertTrue("concrete" in combined_text or "runoff" in combined_text)

    def test_retrieve_first_flush_query(self):
        query = "How much water is diverted during first flush?"
        results = self.store.retrieve_relevant_bylaws(query, top_k=2)
        self.assertGreater(len(results), 0)
        combined_text = " ".join([r["text"] for r in results]).lower()
        self.assertTrue("flush" in combined_text)

    def test_retrieve_bylaw_mandates_query(self):
        query = "What are the rainwater harvesting penalties in Bangalore BBMP?"
        results = self.store.retrieve_relevant_bylaws(query, top_k=3)
        self.assertGreater(len(results), 0)
        combined_text = " ".join([r["text"] for r in results]).lower()
        self.assertTrue("bangalore" in combined_text or "bbmp" in combined_text or "mandatory" in combined_text)

if __name__ == "__main__":
    unittest.main()
