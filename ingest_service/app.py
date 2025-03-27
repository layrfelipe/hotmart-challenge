from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

from scraper import scrape_content
from chunk_size_calculator import calculate_dynamic_chunk_params
from constants import CHROMA_DB_PERSIST_DIRECTORY

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        description="The text content to be ingested and processed",
        example="This is a sample text that needs to be processed and stored in the vector database."
    )

class IngestResponse(BaseModel):
    status: str = Field(..., description="Status of the ingestion process")
    chunks: int = Field(..., description="Number of chunks created from the text")

class ErrorResponse(BaseModel):
    status: str = Field(..., description="Error status")
    message: str = Field(..., description="Error message details")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")

app = FastAPI(
    title="Hotmart RAG Ingest Service",
    description="""
    API for ingesting content into the Hotmart RAG system.
    This service processes text content and stores it in a vector database for later retrieval.
    """,
    version="0.1.0",
    contact={
        "name": "Layr Felipe",
        "email": "layrfpf@gmail.com",
    },
)

@app.on_event("startup")
async def startup_event():
    """Initialize necessary directories on startup"""
    os.makedirs(CHROMA_DB_PERSIST_DIRECTORY, exist_ok=True)

@app.get(
        '/health',
        response_model=HealthResponse,
        tags=["Health"],
        summary="Check if API is running",
        description="Returns the status of the ingest service"
)
async def health():
    return HealthResponse(status="ok")

@app.post(
    "/ingest_text",
    response_model=Union[IngestResponse, ErrorResponse],
    tags=["Ingestion"],
    summary="Ingest text content",
    description="Process and store text content in the vector database"
)
async def ingest_text(request: TextRequest):
    """
    Ingest and process text content:
    - Splits text into appropriate chunks
    - Generates embeddings
    - Stores in vector database
    
    Returns:
        - Success response with number of chunks created
        - Error response if processing fails
    """
    try:
        chunk_size, chunk_overlap = calculate_dynamic_chunk_params(request.text)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

        chunks = text_splitter.split_text(request.text)
        embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
        Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PERSIST_DIRECTORY,
        )

        return IngestResponse(status="success", chunks=len(chunks))
    except Exception as e:
        return ErrorResponse(status="error", message=str(e))

@app.get(
    "/ingest_full_blog_content",
    response_model=Union[IngestResponse, ErrorResponse],
    tags=["Ingestion"],
    summary="Ingest Hotmart blog content",
    description="Scrape, process and store Hotmart blog content in the vector database"
)
async def ingest_full_blog_content():
    """
    Scrape and ingest Hotmart blog content:
    - Scrapes content from predefined blog URL
    - Processes and splits content into chunks
    - Stores in vector database
    
    Returns:
        - Success response with number of chunks created
        - Error response if processing fails
    """
    try:
        full_text = scrape_content()
        chunk_size, chunk_overlap = calculate_dynamic_chunk_params(full_text)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
        chunks = text_splitter.split_text(full_text)
        embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
        Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PERSIST_DIRECTORY
        )
        return IngestResponse(status="success", chunks=len(chunks))
    except Exception as e:
        return ErrorResponse(status="error", message=str(e))