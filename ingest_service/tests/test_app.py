import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

sys.path.append(str(Path(__file__).parent.parent))
from app import app

client = TestClient(app)

@pytest.fixture
def sample_text():
    """Fixture providing a sample text for testing"""
    return "This is a sample text for testing purposes." * 50

def test_ingest_text_success(sample_text):
    """Test successful text ingestion"""
    with patch('app.Chroma.from_texts') as mock_chroma, \
         patch('app.HuggingFaceEmbeddings') as mock_embeddings:
        
        # Setup mocks
        mock_embeddings.return_value = Mock()
        
        # Execute
        response = client.post(
            "/ingest_text",
            json={"text": sample_text}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "success"
        assert isinstance(response_data["chunks"], int)
        assert response_data["chunks"] > 0
        
        # Verify mocks
        mock_chroma.assert_called_once()
        mock_embeddings.assert_called_once_with(model_name="intfloat/multilingual-e5-small")
        print("\n✓ Text ingestion success test passed: content processed correctly")

def test_ingest_text_empty():
    """Test handling of empty text input"""
    response = client.post(
        "/ingest_text",
        json={"text": ""}
    )
    print("response", response)
    assert response.status_code == 200  # Due to error handling in route
    response_data = response.json()
    assert response_data["status"] == "error"
    assert "empty" in response_data["message"].lower()
    print("\n✓ Empty text test passed: correctly handled empty input")

def test_ingest_text_too_long(sample_text):
    """Test handling of text that exceeds length limit"""
    very_long_text = sample_text * 1000
    
    response = client.post(
        "/ingest_text",
        json={"text": very_long_text}
    )
    
    assert response.status_code == 200  # Due to error handling in route
    response_data = response.json()
    assert response_data["status"] == "error"
    assert "too long" in response_data["message"].lower()
    print("\n✓ Long text test passed: correctly handled oversized input")

def test_ingest_text_invalid_request():
    """Test handling of invalid request format"""
    response = client.post(
        "/ingest_text",
        json={"wrong_field": "some text"}
    )
    
    assert response.status_code == 422  # FastAPI validation error
    print("\n✓ Invalid request test passed: correctly handled malformed input")

def test_startup_event():
    """Test database directory creation on startup"""
    with patch('os.makedirs') as mock_makedirs:
        from app import startup_event
        import asyncio
        
        # Execute startup event
        asyncio.run(startup_event())
        
        # Verify directory creation
        mock_makedirs.assert_called_once_with("./chroma_db", exist_ok=True)
        print("\n✓ Startup event test passed: database directory creation verified")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 