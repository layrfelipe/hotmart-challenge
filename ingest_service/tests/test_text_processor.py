import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock

sys.path.append(str(Path(__file__).parent.parent))
from text_processor import process_and_store_text, TextProcessorException

@pytest.fixture
def sample_text():
    """Fixture providing a sample text for testing"""
    return "This is a sample text for testing purposes." * 50

def test_process_and_store_text_success(sample_text):
    """Test successful text processing and storage"""
    with patch('text_processor.Chroma.from_texts') as mock_chroma, \
         patch('text_processor.HuggingFaceEmbeddings') as mock_embeddings, \
         patch('text_processor.calculate_dynamic_chunk_params') as mock_calc:
        
        # Setup mocks
        mock_embeddings.return_value = Mock()
        mock_calc.return_value = (100, 20)  # chunk_size, chunk_overlap
        
        # Execute
        result = process_and_store_text(sample_text)
        
        # Assert
        assert isinstance(result, int)
        assert result > 0
        mock_chroma.assert_called_once()
        mock_embeddings.assert_called_once_with(model_name="intfloat/multilingual-e5-small")
        mock_calc.assert_called_once_with(sample_text)
        print("\n✓ Success test passed: text processed and stored correctly")

def test_process_empty_text():
    """Test handling of empty text input"""
    with pytest.raises(TextProcessorException) as exc_info:
        process_and_store_text("")
    
    assert "Invalid input" in str(exc_info.value)
    print("\n✓ Empty text test passed: correctly handled empty input")

def test_process_invalid_input():
    """Test handling of invalid input types"""
    with pytest.raises(TextProcessorException) as exc_info:
        process_and_store_text(None)
    
    assert "Invalid input" in str(exc_info.value)
    print("\n✓ Invalid input test passed: correctly handled None input")

def test_chunk_calculation_error():
    """Test handling of chunk calculation errors"""
    with patch('text_processor.calculate_dynamic_chunk_params') as mock_calc:
        mock_calc.side_effect = Exception("Chunk calculation failed")
        
        with pytest.raises(TextProcessorException) as exc_info:
            process_and_store_text("Sample text")
        
        assert "Error calculating chunk parameters" in str(exc_info.value)
        print("\n✓ Chunk calculation error test passed: correctly handled calculation error")

def test_embedding_initialization_error():
    """Test handling of embedding model initialization errors"""
    with patch('text_processor.calculate_dynamic_chunk_params') as mock_calc, \
         patch('text_processor.HuggingFaceEmbeddings') as mock_embeddings:
        
        mock_calc.return_value = (100, 20)
        mock_embeddings.side_effect = Exception("Embedding initialization failed")
        
        with pytest.raises(TextProcessorException) as exc_info:
            process_and_store_text("Sample text")
        
        assert "Error initializing embeddings model" in str(exc_info.value)
        print("\n✓ Embedding error test passed: correctly handled initialization error")

def test_storage_error():
    """Test handling of vector database storage errors"""
    with patch('text_processor.calculate_dynamic_chunk_params') as mock_calc, \
         patch('text_processor.HuggingFaceEmbeddings') as mock_embeddings, \
         patch('text_processor.Chroma.from_texts') as mock_chroma:
        
        mock_calc.return_value = (100, 20)
        mock_embeddings.return_value = Mock()
        mock_chroma.side_effect = Exception("Storage failed")
        
        with pytest.raises(TextProcessorException) as exc_info:
            process_and_store_text("Sample text")
        
        assert "Error storing chunks" in str(exc_info.value)
        print("\n✓ Storage error test passed: correctly handled storage error")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 