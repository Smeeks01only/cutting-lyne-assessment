import pytest
import os
import json
import tempfile
from app.services.retriever import KnowledgeRetriever

@pytest.fixture
def temp_kb():
    """Create a small isolated knowledge base simulating the new advanced schema."""
    mock_data = [
        {
            "id": "1",
            "category": "import_documents",
            "title": "Import Docs",
            "canonical_question": "What documents do I need to import?",
            "query_variations": ["Papers for bringing goods in"],
            "synonyms": ["docs", "paperwork"],
            "answer": "Commercial invoice, B/L.",
            "source": "DB",
            "disclaimer": "Verify locally."
        },
        {
            "id": "2",
            "category": "customs_duties",
            "title": "Duties",
            "canonical_question": "How are customs duties calculated?",
            "query_variations": ["What tax will I pay?"],
            "synonyms": ["tax", "tariff", "charges"],
            "answer": "Depends on HS code.",
            "source": "DB",
            "disclaimer": "Verify locally."
        }
    ]
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump(mock_data, f)
        temp_path = f.name
        
    yield temp_path
    
    os.unlink(temp_path)

def test_retriever_initialization(temp_kb):
    retriever = KnowledgeRetriever(kb_path=temp_kb)
    assert len(retriever.knowledge_base) == 2
    assert retriever.tfidf_matrix.shape[0] == 2
    assert len(retriever.semantic_embeddings) == 2

def test_semantic_match_paraphrased(temp_kb):
    retriever = KnowledgeRetriever(kb_path=temp_kb, threshold=0.3)
    # This query doesn't share exact lexical keywords with the canonical question,
    # but the semantic engine should bridge the gap because of meaning.
    results = retriever.retrieve("What paperwork do I need to bring goods into the country?")
    
    assert len(results) > 0
    assert results[0]["id"] == "1"
    # Ensure semantic score was a strong contributing factor
    assert results[0]["semantic_score"] > 0.4

def test_retrieve_unrelated_fails_threshold(temp_kb):
    retriever = KnowledgeRetriever(kb_path=temp_kb, threshold=0.4)
    # Ensure this doesn't match anything strongly
    results = retriever.retrieve("How fast does a cheetah run?")
    assert len(results) == 0

def test_real_kb_initialization():
    # Test that the default initialization with the real expanded KB works
    from app.services.retriever import retriever
    assert len(retriever.knowledge_base) > 0
    res = retriever.retrieve("How much customs will I pay?")
    assert len(res) > 0
    assert "score" in res[0]
    assert "semantic_score" in res[0]
