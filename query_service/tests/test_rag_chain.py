import sys
from pathlib import Path
import pytest
from unittest.mock import Mock, patch

# Add parent directory to system path
#sys.path.append(str(Path(__file__).parent.parent))
from query_service.rag_chain.rag_chain import HotmartRAGSystem

@pytest.fixture
def mock_vector_store():
    """Fixture for mocking Chroma vector store"""
    with patch('rag_chain.Chroma') as mock_chroma:
        mock_chroma.return_value.as_retriever.return_value = Mock()
        yield mock_chroma

@pytest.fixture
def mock_embeddings():
    """Fixture for mocking HuggingFace embeddings"""
    with patch('rag_chain.HuggingFaceEmbeddings') as mock_embeddings:
        yield mock_embeddings

@pytest.fixture
def mock_llm():
    """Fixture for mocking Ollama LLM"""
    with patch('rag_chain.OllamaLLM') as mock_llm:
        yield mock_llm

@pytest.fixture
def rag_system(mock_vector_store, mock_embeddings, mock_llm):
    """Fixture for RAG system with mocked dependencies"""
    return HotmartRAGSystem()

def test_rag_system_initialization(rag_system):
    """Test proper initialization of RAG system"""
    assert rag_system.prompt_template is not None
    assert "contexto" in rag_system.prompt_template.lower()
    assert "pergunta" in rag_system.prompt_template.lower()
    print("\n✓ Initialization test passed: prompt template properly set")

def test_generate_response_success(rag_system):
    """Test successful response generation"""
    test_response = "Resposta de teste"
    
    with patch('rag_chain.RetrievalQA') as mock_qa:
        mock_qa.from_chain_type.return_value.invoke.return_value = {
            "result": test_response
        }
        
        result = rag_system.generate_response("Como funciona a Hotmart?")
        
        assert result["answer"] == test_response
        mock_qa.from_chain_type.assert_called_once()
        print("\n✓ Response generation test passed: correct answer received")

# def test_generate_response_error(rag_system):
#     """Test error handling in response generation"""
#     error_message = "Erro de teste"
    
#     with patch('rag_chain.RetrievalQA') as mock_qa:
#         mock_qa.from_chain_type.side_effect = Exception(error_message)
        
#         result = rag_system.generate_response("Como funciona a Hotmart?")
        
#         assert "error" in result
#         assert error_message in result["error"]
#         print("\n✓ Error handling test passed: error properly caught and returned")

# def test_generate_response_empty_result(rag_system):
#     """Test handling of empty results"""
#     with patch('rag_chain.RetrievalQA') as mock_qa:
#         mock_qa.from_chain_type.return_value.invoke.return_value = {
#             "result": ""
#         }
        
#         result = rag_system.generate_response("Como funciona a Hotmart?")
        
#         assert "error" in result
#         assert "empty response" in result["error"].lower()
#         print("\n✓ Empty result test passed: properly handled empty response")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
