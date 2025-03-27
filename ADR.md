# ADR: Arquitetura do sistema RAG para desafio técnico da Hotmart 

## 1. Contexto
O desafio técnico exigia a construção de dois microsserviços principais:
1. **Serviço de Ingestão**: Processa e armazena documentos em um banco de dados vetorial
2. **Serviço de Consulta**: Recupera informações relevantes e gera respostas usando LLM

Serviços auxiliares implementados:
- Ollama (servidor local para LLM)
- Chroma (banco de dados vetorial open-source)

## 2. Decisões Técnicas

### 2.1 Modelo de LLM: Mistral (7B)
**Alternativas consideradas:**
- TinyLlama
- DeepSeek (quantizado)
- Phi-2

**Decisão final:** Mistral 7B

**Motivação:**
- Melhor equilíbrio entre performance e eficiência para português
- Modelo open-source que roda localmente via Ollama
- Boa qualidade de respostas mesmo com hardware limitado

### 2.2 Modelo de Embedding: multilingual-e5-small
**Alternativas consideradas:**
- all-MiniLM-L6-v2
- paraphrase-multilingual-MiniLM-L12-v2

**Decisão final:** intfloat/multilingual-e5-small

**Motivação:**
- Otimizado para múltiplos idiomas (incluindo português)
- Tamanho compacto (ideal para execução local)
- Boa performance em similaridade semântica

### 2.3 Configuração de Chunking
**Parâmetros selecionados:**
- Tamanho do chunk: 1250 caracteres
- Overlap: 250 caracteres

**Motivação:**
- Alinhado com o tamanho médio de parágrafos do blog da Hotmart
- Overlap evita perda de contexto entre chunks
- Resultados empíricos mostraram melhor recall com esta configuração

### 2.4 Framework: LangChain
**Alternativas consideradas:**
- Implementação manual
- LlamaIndex

**Decisão final:** LangChain

**Motivação:**
- Abstrai a complexidade do pipeline RAG
- Integração simplificada com Chroma e Ollama
- Facilita modificações futuras

### 2.5 Endpoint de Ingestão Automática
**Funcionalidade:**
`ingest_full_blog_content` - ingere automaticamente todo o conteúdo do blog Hotmart

**Motivação:**
- Funcionalidade extra
- Elimina a necessidade de ingestão manual
- Enriquece a base de conhecimento do sistema RAG

## 3. Consequências

### Pontos Positivos
- ✅ Mistral + E5-small garantem respostas rápidas e precisas em português
- ✅ Docker Compose permite execução local sem dependências externas
- ✅ LangChain facilita futuras evoluções do sistema

### Riscos e Limitações
- ⚠️ Mistral 7B pode demandar mais RAM em máquinas modestas
- ⚠️ Chunk fixo pode não ser ideal para todos os tipos de conteúdo
- ⚠️ E5-small tem limitações com textos muito longos/complexos

## 4. Próximos Passos (Opcionais)
- Testar modelos menores (ex: Phi-2 quantizado) para ambientes limitados
- Adicionar metadados dinamiamente nos dados processados pelo serviço de ingestão
- Implementar combinação de busca lexical com busca semântica no serviços de query
