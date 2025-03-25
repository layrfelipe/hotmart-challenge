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
        
        content_body = soup.find('div', class_='content__body')
        if not content_body:
            print("Warning: Could not find main content container")
            content_body = ' '.join([p.get_text() for p in soup.find_all('p')])
        
        text_parts = []
        
        for element in content_body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']):
            # Skip nested list items
            if element.name == 'li' and element.find_parent('li'):
                continue
                
            # Skip paragraphs inside list items or other containers
            if element.name == 'p' and element.find_parent(['li', 'div.text', 'span.text']):
                continue
                
            text = element.get_text().strip()
            if not text:  # Skip empty elements
                continue
                
            # Format based on element type
            if element.name.startswith('h'):
                text_parts.append(f"\n\n{text}\n")
            elif element.name == 'li':
                text_parts.append(f"\n{text}")
            else:
                text_parts.append(f"{text}\n")
        
        full_text = ''.join(text_parts)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=250,
            length_function=len
        )
        
        chunks = text_splitter.split_text(full_text)
        embeddings = HuggingFaceEmbeddings(model_name="multilingual-e5-small")
        Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        return {
            "status": "success", 
            "chunks": len(chunks)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}