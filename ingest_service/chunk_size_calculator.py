from math import floor

BASE_CHUNK_SIZE = 1250
BASE_OVERLAP_SIZE = 250

def calculate_dynamic_chunk_params(text: str) -> tuple[int, int]:
    """
    Calculate optimal chunk_size and overlap based on text characteristics
    Returns: (chunk_size, overlap)
    """
    text_length = len(text)
    if text_length < 2000:
        return (text_length, floor(text_length * 0.1))
    
    elif text_length < 50000:
        chunk_size = BASE_CHUNK_SIZE
        overlap = BASE_OVERLAP_SIZE
    
    else:
        raise ValueError("Text is too long to be processed")
    
    return (chunk_size, max(overlap, 100))