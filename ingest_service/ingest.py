from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    os.makedirs("./chroma_db", exist_ok=True)

@app.post("/ingest")
async def ingest_document(url: str = "https://hotmart.com/pt-br/blog/como-funciona-hotmart"):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        return {"status": "error", "message": str(e)}