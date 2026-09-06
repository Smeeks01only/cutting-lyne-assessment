import json
import os
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import logging

logger = logging.getLogger(__name__)

class KnowledgeRetriever:
    def __init__(self, kb_path: str = None, tfidf_weight: float = 0.35, semantic_weight: float = 0.65, threshold: float = 0.25):
        """
        Initializes the Hybrid Retriever, loading the KB and pre-computing both the TF-IDF matrix
        and the Semantic Embeddings so they do not have to be rebuilt on every request.
        """
        self.tfidf_weight = tfidf_weight
        self.semantic_weight = semantic_weight
        self.threshold = threshold
        
        if not kb_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(current_dir, "../../data/knowledge_base.json")
            
        self.knowledge_base = self._load_kb(kb_path)
        
        # 1. Initialize Lexical Engine
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # 2. Initialize Semantic Engine (lightweight local CPU-friendly model)
        logger.info("Loading SentenceTransformer model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.corpus_texts = []
        
        for entry in self.knowledge_base:
            # We strictly index the variations, questions, titles, and synonyms.
            # We omit the raw answer text to prevent false positive matches on common words.
            canonical = entry.get('canonical_question', '')
            variations = " ".join(entry.get('query_variations', []))
            synonyms = " ".join(entry.get('synonyms', []))
            title = entry.get('title', '')
            
            combined_text = f"{title} {canonical} {variations} {synonyms}"
            self.corpus_texts.append(combined_text)
            
        logger.info("Pre-computing lexical and semantic matrices...")
        # Fit and transform lexical matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_texts)
        
        # Pre-compute semantic embeddings as PyTorch tensors for speed
        self.semantic_embeddings = self.embedder.encode(self.corpus_texts, convert_to_tensor=True)

    def _load_kb(self, kb_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(kb_path):
            raise FileNotFoundError(f"Knowledge base file not found at {kb_path}")
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def retrieve(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Calculates hybrid similarity (lexical + semantic) against the knowledge base.
        Returns the top_k relevant entries that meet the minimum threshold.
        """
        if not query or not query.strip():
            return []
            
        # 1. Lexical Scoring (TF-IDF)
        query_vec_tfidf = self.vectorizer.transform([query])
        lexical_scores = cosine_similarity(query_vec_tfidf, self.tfidf_matrix).flatten()
        
        # 2. Semantic Scoring (Sentence Transformers)
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        # cosine_similarity returns a 2D tensor, extract 1D scores and move to CPU numpy array
        semantic_scores = util.cos_sim(query_embedding, self.semantic_embeddings)[0].cpu().numpy()
        
        results = []
        
        # 3. Combine scores and filter by threshold
        for idx in range(len(self.knowledge_base)):
            lex_score = float(lexical_scores[idx])
            sem_score = float(semantic_scores[idx])
            combined_score = (self.tfidf_weight * lex_score) + (self.semantic_weight * sem_score)
            
            if combined_score >= self.threshold:
                entry = dict(self.knowledge_base[idx])
                entry['score'] = combined_score
                entry['lexical_score'] = lex_score
                entry['semantic_score'] = sem_score
                results.append(entry)
                
        # 4. Sort strictly by combined score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]

# Initialize a singleton instance so models are loaded into RAM exactly once
retriever = KnowledgeRetriever()
