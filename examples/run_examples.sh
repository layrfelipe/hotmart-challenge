#!/bin/bash

# Define base URLs
BASE_URL_INGEST_SERVICE="http://localhost:8000"
BASE_URL_QUERY_SERVICE="http://localhost:8001"

echo "=== Hotmart RAG API Test ==="
echo

# 1. Health Check Ingest Service
echo -n "1. Testing Ingest Service health..."
if response=$(curl -s "$BASE_URL_INGEST_SERVICE/health"); then
    echo " [OK]"
    echo "$response"
else
    echo " [FAILED]"
    echo "Error: $response"
    exit 1
fi

# 2. Health Check Query Service
echo -n "2. Testing Query Service health..."
if response=$(curl -s "$BASE_URL_QUERY_SERVICE/health"); then
    echo " [OK]"
    echo "$response"
else
    echo " [FAILED]"
    echo "Error: $response"
    exit 1
fi

# 3. Ingest Text
echo -n "3. Ingesting text..."
text="A Hotmart é uma empresa global de tecnologia e educação, líder no mercado de produtos digitais, com sede em Amsterdã, nos Países Baixos (Holanda), e escritórios no Brasil, Espanha, Colômbia, México, Estados Unidos, Reino Unido e México. Contamos com soluções completas para Produtores, Afiliados e alunos. São mais de 580 mil produtos cadastrados, 35 milhões de usuários e vendas realizadas em mais de 188 países. E tudo começou quando João Pedro Resende e Mateus Bicalho se uniram para criar uma solução para quem quisesse vender produtos digitais. Na época, JP tinha criado um ebook sobre estratégia de marketing digital para gamers e encontrou diversos desafios para disponibilizar esse conteúdo online. Com isso, os sócios começaram a trabalhar nesta solução no tempo livre, fizeram um MVP e colocaram no ar, até que conseguiram realizar as primeiras vendas pela plataforma. Então passaram a se dedicar integralmente ao negócio. Em 2011, a Hotmart foi fundada!"

if response=$(curl -s -X POST "$BASE_URL_INGEST_SERVICE/ingest_text" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"$text\"}"); then
    echo " [OK]"
    echo "$response"
else
    echo " [FAILED]"
    echo "Error: $response"
    exit 1
fi

# 4. Sample Queries
echo -e "\n4. Testing sample queries:"

questions=(
    "A Hotmart é uma empresa de quê?"
    "Quais são as taxas da plataforma Hotmart?"
    "Qualquer pessoa do Brasil pode vender produtos na Hotmart?"
)

for question in "${questions[@]}"; do
    echo -e "\nQ: $question"
    echo -n "Processing..."
    if response=$(curl -s -X POST "$BASE_URL_QUERY_SERVICE/query" \
        -H "Content-Type: application/json" \
        -d "{\"question\": \"$question\"}"); then
        echo -e "\rA: $response"
    else
        echo -e "\rError processing question: $response"
    fi
done

# 5. Full Blog Ingestion
# echo -n "5. Ingesting full blog content..."
# if response=$(curl -s "$BASE_URL_INGEST_SERVICE/ingest_full_blog_content"); then
#     echo " [OK]"
#     echo "$response"
# else
#     echo " [FAILED]"
#     echo "Error: $response"
#     exit 1
# fi

echo -e "\n=== Test completed ===" 