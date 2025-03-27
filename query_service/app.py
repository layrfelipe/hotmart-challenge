from fastapi import FastAPI, HTTPException

from rag_chain import QueryRequest, QueryResponse, RAGException, HotmartRAGSystem

app = FastAPI(
    title="Hotmart RAG Query Service",
    description="""
    API for querying the Hotmart RAG system.
    This service processes questions and generates responses using the stored knowledge base.
    """,
    version="0.1.0",
    contact={
        "name": "Layr Felipe",
        "email": "layrfpf@gmail.com",
    },
)

@app.post(
    "/query",
    response_model=QueryResponse,
    tags=["Query"],
    summary="Query the knowledge base",
    description="Process a question and generate a response using the RAG system"
)
async def query_knowledge(request: QueryRequest):
    """
    Process a question and generate a response:
    - Validates the input question
    - Retrieves relevant context from the vector store
    - Generates a response using the LLM
    
    Returns:
        - QueryResponse with the generated answer
        - HTTPException if processing fails
    """
    try:
        rag_system = HotmartRAGSystem()
        result = rag_system.generate_response(request.question)
        
        return QueryResponse(answer=result["answer"])
        
    except RAGException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )