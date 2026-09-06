import json
import os
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class KnowledgeRetriever:
    def __init__(self, kb_path: str = None, threshold: float = 0.20):
        """
        Initializes the TF-IDF Retriever, loading the KB and pre-computing the TF-IDF matrix.
        (Semantic BERT engine removed to accommodate Render 512MB RAM limits)
        """
        self.threshold = threshold
        
        if not kb_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(current_dir, "../../data/knowledge_base.json")
            
        self.knowledge_base = self._load_kb(kb_path)
        
        # 1. Initialize Lexical Engine
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        self.corpus_texts = []
        
        for entry in self.knowledge_base:
            canonical = entry.get('canonical_question', '')
            variations = " ".join(entry.get('query_variations', []))
            synonyms = " ".join(entry.get('synonyms', []))
            title = entry.get('title', '')
            
            combined_text = f"{title} {canonical} {variations} {synonyms}"
            self.corpus_texts.append(combined_text)
            
        logger.info("Pre-computing lexical matrix...")
        # Fit and transform lexical matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_texts)

    def _load_kb(self, kb_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(kb_path):
            raise FileNotFoundError(f"Knowledge base file not found at {kb_path}")
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def retrieve(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Calculates lexical similarity (TF-IDF) against the knowledge base.
        Returns the top_k relevant entries that meet the minimum threshold.
        """
        if not query or not query.strip():
            return []
            
        # Lexical Scoring (TF-IDF)
        query_vec_tfidf = self.vectorizer.transform([query])
        lexical_scores = cosine_similarity(query_vec_tfidf, self.tfidf_matrix).flatten()
        
        results = []
        
        for idx in range(len(self.knowledge_base)):
            score = float(lexical_scores[idx])
            
            if score >= self.threshold:
                entry = dict(self.knowledge_base[idx])
                entry['score'] = score
                entry['lexical_score'] = score
                results.append(entry)
                
        # Sort strictly by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]

# Initialize a singleton instance
retriever = KnowledgeRetriever()
