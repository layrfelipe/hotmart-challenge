from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from chunk_size_calculator import calculate_dynamic_chunk_params
from constants import CHROMA_DB_PERSIST_DIRECTORY

class TextProcessorException(Exception):
    """Custom exception for text processing errors"""
    pass

def process_and_store_text(text: str) -> int:
    """
    Process the text into chunks and store in a vector database.
    
    Args:
        text (str): The text to process.
    
    Returns:
        int: Number of chunks created.
        
    Raises:
        TextProcessorException: If there's an error during text processing or storage
    """
    try:
        if not text or not isinstance(text, str):
            raise TextProcessorException("Invalid input: text must be a non-empty string")

        # Calculate chunk parameters
        try:
            chunk_size, chunk_overlap = calculate_dynamic_chunk_params(text)
        except Exception as e:
            raise TextProcessorException(f"Error calculating chunk parameters: {str(e)}")

        # Split text into chunks
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
        except Exception as e:
            raise TextProcessorException(f"Error splitting text into chunks: {str(e)}")

        if not chunks:
            raise TextProcessorException("No chunks were created from the input text")

        # Generate embeddings
        try:
            embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
        except Exception as e:
            raise TextProcessorException(f"Error initializing embeddings model: {str(e)}")

        # Store in vector database
        try:
            Chroma.from_texts(
                texts=chunks,
                embedding=embeddings,
                persist_directory=CHROMA_DB_PERSIST_DIRECTORY
            )
        except Exception as e:
            raise TextProcessorException(f"Error storing chunks in vector database: {str(e)}")

        return len(chunks)

    except TextProcessorException:
        raise
    except Exception as e:
        raise TextProcessorException(f"Unexpected error during text processing: {str(e)}")
