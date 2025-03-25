from fastapi import FastAPI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

embeddings = HuggingFaceEmbeddings(model_name="multilingual-e5-small")
vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

llm = OllamaLLM(base_url="http://ollama:11434", model="mistral")

prompt_template = """Aja como um antigo funcionário da Hotmart que conhece a fundo a empresa.
Se não souber a resposta, diga que não sabe. Não invente.
Use o seguinte contexto para responder a pergunta.

Contexto: {context}
Pergunta: {question}

Resposta:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

@app.post("/ask")
async def ask_question(query: Query):
    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result = qa_chain.invoke({"query": query.question})
        return {"question": query.question, "answer": result["result"]}
    except Exception as e:
        return {"error": str(e)}