"""
AquaHarvest AI - RAG Vector Store & Retrieval Manager
Indexes CGWB guidelines, BIS standards, and Municipal Bylaws.
Supports local ChromaDB or fast in-memory TF-IDF semantic vector search.
"""

import os
from typing import List, Dict, Any
from rag.embeddings import chunk_text_by_sections, LightweightTfIdfVectorizer

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class RAGVectorStore:
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.vectorizer = LightweightTfIdfVectorizer()
        self.is_indexed = False
        self._load_and_index_documents()

    def _load_and_index_documents(self):
        """Loads all raw text documents from rag/data and indexes them."""
        doc_files = [
            ("cgwb_rwh_guidelines.txt", "Central Ground Water Board (CGWB) Guidelines"),
            ("is_15797_standards.txt", "Bureau of Indian Standards (BIS IS 15797:2008)"),
            ("municipal_bylaws.txt", "State & Municipal RWH Mandates & Bylaws"),
            ("water_quality_norms.txt", "BIS 10500 Water Quality & Reuse Norms")
        ]
        
        all_chunks = []
        for filename, doc_title in doc_files:
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read()
                    chunks = chunk_text_by_sections(text, doc_title)
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    
        self.chunks = all_chunks
        if self.chunks:
            texts = [c["text"] for c in self.chunks]
            self.vectorizer.fit_transform(texts)
            self.is_indexed = True

    def retrieve_relevant_bylaws(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Performs semantic cosine similarity and keyword search over indexed bylaws and engineering standards.
        Returns top-k matching chunks with similarity score and metadata.
        """
        if not self.is_indexed or not self.chunks:
            return []

        all_scores = self.vectorizer.score_query(query)
        scored_pairs = [(score, idx) for idx, score in enumerate(all_scores)]
        scored_pairs.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, idx in scored_pairs[:top_k]:
            chunk = self.chunks[idx]
            results.append({
                "source": chunk["source"],
                "heading": chunk["heading"],
                "text": chunk["text"],
                "similarity_score": round(score, 3)
            })
            
        return results

    def get_all_sources(self) -> List[str]:
        return list(set(c["source"] for c in self.chunks))


# Global singleton store
_global_rag_store = None

def get_rag_store() -> RAGVectorStore:
    global _global_rag_store
    if _global_rag_store is None:
        _global_rag_store = RAGVectorStore()
    return _global_rag_store
