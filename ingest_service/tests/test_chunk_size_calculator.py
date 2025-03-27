import pytest
import sys
from pathlib import Path

#sys.path.append(str(Path(__file__).parent.parent))

from chunk_size_calculator import calculate_dynamic_chunk_params, BASE_CHUNK_SIZE, BASE_OVERLAP_SIZE

def test_small_text_chunking():
    text = "Small text example" * 10  # ~150 chars
    chunk_size, overlap = calculate_dynamic_chunk_params(text)
    
    assert chunk_size == len(text)
    assert overlap == len(text) * 0.1
    print(f"\n✓ Small text test passed: chunk_size={chunk_size}, overlap={overlap}")

def test_medium_text_chunking():
    text = "Medium length text" * 100  # ~1600 chars
    chunk_size, overlap = calculate_dynamic_chunk_params(text)
    
    assert chunk_size == len(text)
    assert overlap == len(text) * 0.1
    print(f"\n✓ Medium text test passed: chunk_size={chunk_size}, overlap={overlap}")

def test_regular_text_chunking():
    text = "Regular text" * 1000  # ~11000 chars
    chunk_size, overlap = calculate_dynamic_chunk_params(text)
    
    assert chunk_size == BASE_CHUNK_SIZE
    assert overlap == BASE_OVERLAP_SIZE
    print(f"\n✓ Regular text test passed: chunk_size={chunk_size}, overlap={overlap}")

def test_very_long_text():
    text = "Very long text" * 10000  # >100000 chars
    with pytest.raises(ValueError) as exc_info:
        calculate_dynamic_chunk_params(text)
    assert str(exc_info.value) == "Text is too long to be processed"
    print("\n✓ Very long text test passed: correctly raised exception")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 