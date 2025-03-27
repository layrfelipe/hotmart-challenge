#!/bin/bash

# Define base URLs
BASE_URL_INGEST_SERVICE="http://localhost:8000"
BASE_URL_QUERY_SERVICE="http://localhost:8001"

echo "=== Hotmart RAG API Test ==="

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

# 3. Sample Queries
echo "3. Testing sample queries:"

questions=(
    "A Hotmart é uma empresa de quê?"
    "Quais são as taxas da plataforma Hotmart?"
    "Qualquer pessoa do Brasil pode vender produtos na Hotmart?"
)

for question in "${questions[@]}"; do
    echo "Q: $question"
    response=$(curl -s -X POST "$BASE_URL_QUERY_SERVICE/query" \
        -H "Content-Type: application/json" \
        -d "{\"question\": \"$question\"}")
    
    if [ $? -eq 0 ]; then
        echo "A: $response"
    else
        echo "Error processing question: $response"
    fi
    echo "---"
done

# Optional: Uncomment to test text ingestion
# echo -n "4. Testing text ingestion..."
# text="A Hotmart é uma empresa global de tecnologia e educação..."
# response=$(curl -s -X POST "$BASE_URL_INGEST_SERVICE/ingest_text" \
#     -H "Content-Type: application/json" \
#     -d "{\"text\": \"$text\"}")
# if [ $? -eq 0 ]; then
#     echo " [OK]"
#     echo "$response"
# else
#     echo " [FAILED]"
#     echo "Error: $response"
# fi

echo "=== Test completed ===" 