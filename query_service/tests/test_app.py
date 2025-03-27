import sys
from pathlib import Path
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add parent directory to system path
#sys.path.append(str(Path(__file__).parent.parent))
from app import app
from query_service.rag_chain.rag_chain import RAGException

client = TestClient(app)

def test_query_knowledge_success():
    """Test successful query response"""
    test_question = "Como funciona a Hotmart?"
    expected_answer = "A Hotmart é uma plataforma de produtos digitais."
    
    with patch('app.HotmartRAGSystem') as mock_rag:
        mock_rag.return_value.generate_response.return_value = {
            "answer": expected_answer
        }
        
        response = client.post(
            "/query",
            json={"question": test_question}
        )
        
        assert response.status_code == 200
        assert response.json() == {
            "answer": expected_answer
        }
        print("\n✓ Query success test passed: correct response received")

def test_query_knowledge_rag_error():
    """Test handling of RAG system errors"""
    with patch('app.HotmartRAGSystem') as mock_rag:
        mock_rag.return_value.generate_response.side_effect = RAGException("Failed to generate response")
        
        response = client.post(
            "/query",
            json={"question": "Pergunta teste"}
        )
        
        assert response.status_code == 400
        assert "Failed to generate response" in response.json()["detail"]
        print("\n✓ RAG error test passed: error properly handled")

def test_query_knowledge_invalid_request():
    """Test handling of invalid request format"""
    response = client.post(
        "/query",
        json={}  # Missing required 'question' field
    )
    
    assert response.status_code == 422
    print("\n✓ Invalid request test passed: validation error caught")

def test_query_knowledge_empty_question():
    """Test handling of empty question"""
    response = client.post(
        "/query",
        json={"question": ""}
    )
    
    assert response.status_code == 422
    print("\n✓ Empty question test passed: validation error caught")

def test_query_knowledge_long_question():
    """Test handling of very long questions"""
    response = client.post(
        "/query",
        json={"question": "?" * 501}  # Exceeds max_length
    )
    
    assert response.status_code == 422
    print("\n✓ Long question test passed: validation error caught")

def test_query_knowledge_system_error():
    """Test handling of unexpected system errors"""
    with patch('app.HotmartRAGSystem') as mock_rag:
        mock_rag.return_value.generate_response.side_effect = Exception("Unexpected error")
        
        response = client.post(
            "/query",
            json={"question": "Pergunta teste"}
        )
        
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]
        print("\n✓ System error test passed: unexpected error properly handled")

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
