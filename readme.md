# Protótipo Hotmart RAG

Sistema de Retrieval-Augmented Generation (RAG) para conhecimento sobre a Hotmart. Este sistema permite a ingestão de conteúdo e consultas utilizando RAG para fornecer respostas precisas sobre a Hotmart. Vale destacar que todas as tecnologias utiliadas no projeto são open source.

## Tecnologias Utilizadas
- **Versão Python**: 3.10
- **RAG Framework**: LangChain
- **LLM**: Mistral (7B)
- **Execução do LLM**: Ollama
- **Vector DB**: ChromaDB
- **Backend**: FastAPI
- **Embeddings**: Multilingual-E5-Small (HuggingFace)
- **Orquestração**: Docker Compose

---

## Arquitetura do Sistema

O sistema é composto por dois serviços principais:

### 1. Ingest Service (Porta 8000)
- Responsável pela ingestão de conteúdo
- Processamento e chunking de texto
- Geração de embeddings
- Armazenamento no ChromaDB

### 2. Query Service (Porta 8001)
- Processamento de consultas
- Recuperação de contexto relevante
- Geração de respostas utilizando RAG

Para mais detalhes sobre as decisões arquiteturais, modelos escolhidos e configurações técnicas, consulte o [ADR (Architecture Decision Record)](ADR.md).

---

## Pré-requisitos
- Docker e Docker Compose instalados
- Mínimo de 8GB de RAM disponível
- Git instalado

## Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/layrfelipe/hotmart-challenge.git
cd hotmart-challenge
```

2. Inicie os containers:
```bash
docker-compose up --build -d
```

3. Verifique se todos os serviços estão rodando:
```bash
docker-compose ps
```

---

## Endpoints Disponíveis

### Ingest Service (http://localhost:8000)

#### 1. Ingestão de Texto
- **Endpoint**: POST `/ingest_text`
- **Payload**:
```json
{
    "text": "Texto a ser processado"
}
```

#### 2. Ingestão de Blog (extra)
- **Endpoint**: POST `/ingest_full_blog_content`
- **Descrição**: Realiza scraping e ingestão automática do conteúdo completo do blog da Hotmart

### Query Service (http://localhost:8001)

#### 1. Consulta ao Conhecimento
- **Endpoint**: POST `/query`
- **Payload**:
```json
{
    "question": "Sua pergunta sobre a Hotmart"
}
```

---

## Documentação da API

A documentação completa da API está disponível através do Swagger UI:
- Ingest Service: http://localhost:8000/docs
- Query Service: http://localhost:8001/docs

---

## Desenvolvimento e Testes

### Instalação de Dependências
```bash
# Instale as dependências de desenvolvimento

## Acesse cada serviço (ingest_service e query_service) separadamente para criar seus virtual environments e realizar os testes
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Executando Testes
```bash
# Ingest Service (partindo da raíz do projeto)
cd /ingest_service
pytest

# Query Service partindo da raíz do projeto)
cd /query_service
pytest
```

---

## Estrutura do Projeto

### Limitações e Considerações

- O sistema está configurado para processar textos de até 50.000 caracteres
- O modelo Mistral é razoavelmente leve e pode ter limitações em respostas complexas
- Por uma questão de adequação ao contexto proposto, as respostas são sempre geradas em português
- O sistema utiliza embeddings multilíngues para melhor processamento do português, tive certa dificuldade em achar modelos leves e eficientes treinados em PT-BR

## Contato

Layr Felipe - [layrfpf@gmail.com](mailto:layrfpf@gmail.com)

Link do Projeto: [https://github.com/layrfelipe/hotmart-challenge](https://github.com/layrfelipe/hotmart-challenge)
