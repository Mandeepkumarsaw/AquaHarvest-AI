"""
AquaHarvest AI - Embeddings and Text Chunking Engine
Zero-cost, local text processing for CGWB and Indian Standards RAG.
"""

import re
import math
from typing import List, Dict, Any

def chunk_text_by_sections(text: str, source_name: str, max_words: int = 150) -> List[Dict[str, Any]]:
    """
    Chunks sustainability documents into coherent topic sections and bullet points.
    Filters out dangling single-line headers.
    """
    raw_sections = re.split(r'\n(?=[0-9]+\.|\b[A-Z\s]{4,}:|\s*-\s+[A-Z])', text)
    chunks = []
    
    for idx, sec in enumerate(raw_sections):
        cleaned = sec.strip()
        # Skip pure title headers or tiny snippets
        if not cleaned or len(cleaned) < 50 or cleaned.startswith("# "):
            continue
            
        first_line = cleaned.split('\n')[0][:80].strip()
        words = cleaned.split()
        if len(words) > max_words:
            for i in range(0, len(words), max_words - 25):
                sub_text = " ".join(words[i:i + max_words])
                chunks.append({
                    "id": f"{source_name}_sec{idx}_sub{i}",
                    "text": sub_text,
                    "source": source_name,
                    "heading": first_line
                })
        else:
            chunks.append({
                "id": f"{source_name}_sec{idx}",
                "text": cleaned,
                "source": source_name,
                "heading": first_line
            })
            
    return chunks


class LightweightTfIdfVectorizer:
    """
    A pure-python zero-dependency vectorizer with hybrid semantic and BM25 term overlap.
    Guarantees zero-cost, instant offline startup without requiring heavy downloads.
    """
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_vectors: List[List[float]] = []
        self.doc_tokens_list: List[set] = []
        self.is_fitted = False

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-z0-9_]{2,}\b', text.lower())
        stopwords = {
            "the", "and", "is", "in", "to", "of", "for", "with", "a", "an", "on", 
            "at", "by", "from", "up", "about", "into", "over", "after", "it", "this", "are", "what"
        }
        return [w for w in words if w not in stopwords]

    def fit_transform(self, documents: List[str]) -> List[List[float]]:
        doc_tokens = [self._tokenize(doc) for doc in documents]
        self.doc_tokens_list = [set(t) for t in doc_tokens]
        num_docs = len(documents)
        
        # Build vocabulary
        doc_freq: Dict[str, int] = {}
        for tokens in doc_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freq[token] = doc_freq.get(token, 0) + 1
                
        self.vocabulary = {term: idx for idx, term in enumerate(sorted(doc_freq.keys()))}
        self.idf = {
            term: math.log((num_docs + 1) / (df + 1)) + 1.0 
            for term, df in doc_freq.items()
        }
        
        # Transform documents
        self.doc_vectors = [self._transform_tokens(tokens) for tokens in doc_tokens]
        self.is_fitted = True
        return self.doc_vectors

    def _transform_tokens(self, tokens: List[str]) -> List[float]:
        vec = [0.0] * len(self.vocabulary)
        if not tokens:
            return vec
            
        tf: Dict[str, int] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
            
        total_tokens = len(tokens)
        for term, count in tf.items():
            if term in self.vocabulary:
                idx = self.vocabulary[term]
                tf_val = count / total_tokens
                vec[idx] = tf_val * self.idf[term]
                
        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def transform(self, query: str) -> List[float]:
        tokens = self._tokenize(query)
        return self._transform_tokens(tokens)

    def score_query(self, query: str) -> List[float]:
        """Hybrid scoring: Cosine similarity + exact keyword match bonus"""
        q_tokens = self._tokenize(query)
        q_vec = self._transform_tokens(q_tokens)
        scores = []
        q_set = set(q_tokens)
        
        for idx, d_vec in enumerate(self.doc_vectors):
            dot = sum(q * d for q, d in zip(q_vec, d_vec))
            # Exact keyword overlap bonus
            overlap = len(q_set.intersection(self.doc_tokens_list[idx]))
            bonus = (overlap / len(q_set)) * 0.4 if q_set else 0.0
            scores.append(dot + bonus)
            
        return scores

