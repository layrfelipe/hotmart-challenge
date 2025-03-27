# Define base URLs
$BASE_URL_INGEST_SERVICE = "http://localhost:8000"
$BASE_URL_QUERY_SERVICE = "http://localhost:8001"

Write-Host "=== Hotmart RAG API Test ===" "`n"

# 1. Health Check Ingest Service
try {
    Write-Host "1. Testing Ingest Service health..." -NoNewline
    $health = Invoke-RestMethod -Uri "$BASE_URL_INGEST_SERVICE/health" -Method Get
    Write-Host " [OK]" -ForegroundColor Green
    $health | Format-List | Out-Host
}
catch {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# 2. Health Check Query Service
try {
    Write-Host "2. Testing Query Service health..." -NoNewline
    $health = Invoke-RestMethod -Uri "$BASE_URL_QUERY_SERVICE/health" -Method Get
    Write-Host " [OK]" -ForegroundColor Green
    $health | Format-List | Out-Host
}
catch {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# 3. Ingest Text
try {
    Write-Host "3. Ingesting text..." -NoNewline
    $body = @{
        text = "A Hotmart é uma empresa global de tecnologia e educação, líder no mercado de produtos digitais, com sede em Amsterdã, nos Países Baixos (Holanda), e escritórios no Brasil, Espanha, Colômbia, México, Estados Unidos, Reino Unido e México. Contamos com soluções completas para Produtores, Afiliados e alunos. São mais de 580 mil produtos cadastrados, 35 milhões de usuários e vendas realizadas em mais de 188 países. E tudo começou quando João Pedro Resende e Mateus Bicalho se uniram para criar uma solução para quem quisesse vender produtos digitais. Na época, JP tinha criado um ebook sobre estratégia de marketing digital para gamers e encontrou diversos desafios para disponibilizar esse conteúdo online. Com isso, os sócios começaram a trabalhar nesta solução no tempo livre, fizeram um MVP e colocaram no ar, até que conseguiram realizar as primeiras vendas pela plataforma. Então passaram a se dedicar integralmente ao negócio. Em 2011, a Hotmart foi fundada!"
    }

    $response = Invoke-RestMethod -Uri "$BASE_URL_INGEST_SERVICE/ingest_text" `
        -Method Post `
        -Body ($body | ConvertTo-Json) `
        -ContentType "application/json"
    
    Write-Host " [OK]" -ForegroundColor Green
    $response | Format-List | Out-Host
}
catch {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# 3. Sample Queries
$questions = @(
    "A Hotmart é uma empresa de quê?",
    "Quais são as taxas da plataforma Hotmart?",
    "Qualquer pessoa do Brasil pode vender produtos na Hotmart?"
)

Write-Host "3. Testing sample queries:" -ForegroundColor Cyan

foreach ($question in $questions) {
    try {
        Write-Host "`nQ: $question"
        $body = @{
            question = $question
        }
        Write-Host "Processing..." -NoNewline
        $response = Invoke-RestMethod -Uri "$BASE_URL_QUERY_SERVICE/query" `
            -Method Post `
            -Body ($body | ConvertTo-Json) `
            -ContentType "application/json"
        Write-Host "`r" -NoNewline  # Clear the "Processing..." line
        Write-Host "A: $($response.answer)"
    }
    catch {
        Write-Host "`r" -NoNewline  # Clear the "Processing..." line
        Write-Host "Error processing question: $_"
    }
}

# # 4. Full Blog Ingestion
# try {
#     Write-Host "2. Ingesting full blog content..." -NoNewline
#     $ingestResponse = curl -s -X GET "$BASE_URL/ingest_full_blog_content"
#     Write-Host " [OK]" -ForegroundColor Green
#     $ingestResponse | Format-List | Out-Host
# }
# catch {
#     Write-Host " [FAILED]" -ForegroundColor Red
#     Write-Host "Error: $_" -ForegroundColor Red
# }

Write-Host "`n=== Test completed ===" -ForegroundColor Cyan