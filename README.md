# Relatório IAGen

> Plataforma web para análise e geração de relatórios financeiros de ações da B3, com inteligência artificial generativa.

[![CI](https://github.com/rafaelgutierres049/Relatorio-IAGen/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/rafaelgutierres049/Relatorio-IAGen/actions/workflows/ci.yml)

---

## Funcionalidades

### Gerar Relatório de Ação
Informe o ticker de uma ação (ex: `PETR4`) e o sistema gera um relatório completo com:
- Introdução e contexto de mercado
- Análise do impacto de notícias recentes
- Resumo diário e análise semanal
- Recomendações de compra/venda/manutenção
- Previsões de mercado
- Análise comparativa com o setor
- Gráficos interativos: candlestick anual com volume e preços mensais

### Comparar Duas Ações
Compare o desempenho de dois ativos lado a lado:
- Preço atual
- P/L (Preço/Lucro)
- Dividend Yield
- Variação na semana, no mês e no ano

### Descobrir Melhores Ações
Analisa todas as ações listadas na B3 cruzando com as notícias do mercado para identificar as melhores oportunidades por prazo (curto, médio e longo).

---

## Tecnologias

| Categoria | Tecnologia |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| IA Generativa | [OpenAI API](https://platform.openai.com/) (GPT-4) |
| Dados históricos (OHLC) | [yfinance](https://github.com/ranaroussi/yfinance) 1.2.0 |
| Dados fundamentais | [brapi.dev](https://brapi.dev/) (P/L, Dividend Yield, info) |
| Gráficos | [Plotly](https://plotly.com/python/) |
| Web scraping | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) |
| Cache de requisições | [requests-cache](https://requests-cache.readthedocs.io/) |
| Templates | [Jinja2](https://jinja.palletsprojects.com/) |
| Containerização | Docker + Docker Compose |
| CI | GitHub Actions (lint + docker build) |

---

## Estrutura do Projeto

```
Relatorio-IAGen/
├── app/
│   ├── chat_integration/
│   │   └── chat_integration.py   # Integração com a OpenAI API
│   ├── core/
│   │   ├── config.py             # Configurações via variáveis de ambiente
│   │   ├── logger.py             # Logger centralizado
│   │   └── schemas.py            # Schemas Pydantic
│   └── funcionalidades/
│       ├── graficos.py           # Geração de gráficos Plotly (HTML)
│       ├── news_data.py          # Scraping de notícias financeiras
│       └── stocks_data.py        # Dados de ações (yfinance + brapi.dev)
├── frontend/
│   ├── static/
│   │   ├── styles.css
│   │   └── script.js
│   └── templates/                # Templates Jinja2
├── .env.example
├── .github/workflows/ci.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── run.py
```

---

## Como Rodar

### Pré-requisitos
- Docker e Docker Compose **ou** Python 3.12+
- Chave de API da [OpenAI](https://platform.openai.com/api-keys)

### 1. Clone o repositório

```bash
git clone https://github.com/rafaelgutierres049/Relatorio-IAGen.git
cd Relatorio-IAGen
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
OPENAI_API_KEY=sk-...          # Sua chave da OpenAI
OPENAI_MODEL=gpt-4             # Modelo a utilizar
OPENAI_TEMPERATURE=0.5

APP_DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000
```

### 3a. Rodar com Docker (recomendado)

```bash
docker compose up --build
```

Acesse: [http://localhost:8000](http://localhost:8000)

### 3b. Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Página inicial |
| `GET/POST` | `/relatorio` | Formulário e submissão de ticker |
| `GET` | `/relatorio/gera?ticker=XXXX` | Geração do relatório |
| `GET/POST` | `/compara` | Formulário de comparação |
| `GET` | `/compara/acoes?ticker1=X&ticker2=Y` | Resultado da comparação |
| `GET` | `/encontrar` | Página de descoberta de ações |
| `GET` | `/encontrar/acoes` | Análise das melhores ações da B3 |

---

## CI/CD

O pipeline de CI roda automaticamente em todo push e pull request para `master`:

1. **Lint** — `ruff check app/` com Python 3.12
2. **Docker Build** — valida que a imagem constrói com sucesso

---

## Autor

Criado por **Rafael Ponte Gutierres**
