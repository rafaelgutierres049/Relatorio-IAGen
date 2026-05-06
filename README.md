# AI Financial Report Generator

[![CI](https://github.com/rafaelgutierres049/Relatorio-IAGen/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/rafaelgutierres049/Relatorio-IAGen/actions/workflows/ci.yml)

An AI-powered financial report generator for educational and analytical purposes.

The platform combines market data, financial news, interactive visualizations, and LLM-generated summaries to create structured reports about publicly traded companies on the Brazilian stock market.

This project demonstrates how Generative AI can be integrated with financial data pipelines, web scraping, backend APIs, chart generation, and automated report creation.

---

## Disclaimer

This project is for **educational and analytical purposes only**.

It does **not** provide financial advice, investment recommendations, buy/sell signals, or portfolio management guidance. Any generated content should be interpreted as an automated analysis based on public data and should not be used as the sole basis for investment decisions.

---

## Features

### Stock Report Generation

Users can provide a stock ticker, such as `PETR4`, and the system generates a structured report containing:

- Company and market context
- Recent news analysis
- Daily and weekly market summary
- Educational commentary about potential market impacts
- Sector comparison
- Historical price analysis
- Interactive charts with annual candlestick data, volume, and monthly price trends

---

### Stock Comparison

Compare two assets side by side using financial and market indicators such as:

- Current price
- P/E ratio
- Dividend Yield
- Weekly variation
- Monthly variation
- Yearly variation

---

### Market Screener

The system analyzes stocks listed on B3 using public market data and recent financial news to generate an educational overview of assets that may deserve further analysis.

This feature is designed as a **screening and research assistant**, not as an investment recommendation engine.

---

## Why This Project Matters

Financial analysis often requires collecting information from multiple sources, including historical prices, company fundamentals, news articles, and market indicators.

This project explores how Generative AI can support this workflow by:

- Collecting structured and unstructured financial data
- Extracting relevant market news
- Generating summaries from financial context
- Creating interactive visualizations
- Producing automated reports through a backend API
- Organizing financial information into a readable format

The goal is to demonstrate how LLMs can be used as an analytical layer on top of data pipelines, rather than as an isolated chatbot.

---

## Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI + Uvicorn |
| Generative AI | OpenAI API |
| Historical market data | yfinance |
| Fundamental data | brapi.dev |
| Charts | Plotly |
| Web scraping | BeautifulSoup4 |
| Request cache | requests-cache |
| Templates | Jinja2 |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Linting | Ruff |

---

## Engineering Highlights

- FastAPI backend for report generation and financial analysis routes
- Integration with OpenAI API for AI-generated summaries
- Market data retrieval using yfinance and brapi.dev
- Financial news extraction using BeautifulSoup
- Interactive chart generation with Plotly
- Template-based frontend using Jinja2
- Environment-based configuration
- Centralized logging
- Pydantic schemas for data validation
- Dockerized local setup
- GitHub Actions pipeline for linting and Docker build validation
- Request caching to reduce repeated external API calls

---

## Project Structure

```text
Relatorio-IAGen/
├── app/
│   ├── chat_integration/
│   │   └── chat_integration.py   # OpenAI API integration
│   ├── core/
│   │   ├── config.py             # Environment-based settings
│   │   ├── logger.py             # Centralized logger
│   │   └── schemas.py            # Pydantic schemas
│   └── funcionalidades/
│       ├── graficos.py           # Plotly chart generation
│       ├── news_data.py          # Financial news scraping
│       └── stocks_data.py        # Stock data from yfinance and brapi.dev
├── frontend/
│   ├── static/
│   │   ├── styles.css
│   │   └── script.js
│   └── templates/                # Jinja2 templates
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions workflow
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

---

## Getting Started

### Prerequisites

You need either:

- Docker and Docker Compose

or:

- Python 3.12+
- An OpenAI API key

---

## Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then configure the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.5

APP_DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000
```

---

## Running with Docker

Clone the repository:

```bash
git clone https://github.com/rafaelgutierres049/Relatorio-IAGen.git
cd Relatorio-IAGen
```

Create the environment file:

```bash
cp .env.example .env
```

Start the application:

```bash
docker compose up --build
```

Access the application at:

```text
http://localhost:8000
```

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/rafaelgutierres049/Relatorio-IAGen.git
cd Relatorio-IAGen
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Start the application:

```bash
python run.py
```

Access the application at:

```text
http://127.0.0.1:8000
```

---

## API Routes

| Method | Route | Description |
|------|-------|-------------|
| `GET` | `/` | Home page |
| `GET/POST` | `/relatorio` | Stock report form and submission |
| `GET` | `/relatorio/gera?ticker=XXXX` | Generate a stock report |
| `GET/POST` | `/compara` | Stock comparison form |
| `GET` | `/compara/acoes?ticker1=X&ticker2=Y` | Compare two stocks |
| `GET` | `/encontrar` | Market screener page |
| `GET` | `/encontrar/acoes` | Run B3 stock screening analysis |

---

## Example Use Cases

### Generate a Stock Report

Example ticker:

```text
PETR4
```

The system collects market data, retrieves recent news, generates visualizations, and produces an AI-assisted analytical report.

---

### Compare Two Stocks

Example:

```text
PETR4 vs VALE3
```

The system compares both assets using financial indicators and recent price variation.

---

### Analyze Market Candidates

The system reviews available market data and news to create an educational overview of stocks that may require deeper analysis.

This feature is intended to support research workflows, not to recommend trades.

---

## CI/CD

The GitHub Actions workflow runs automatically on pushes and pull requests to the `master` branch.

The pipeline includes:

1. **Linting**  
   Runs `ruff check app/` using Python 3.12.

2. **Docker Build Validation**  
   Validates that the Docker image builds successfully.

---

## Known Limitations

- The system depends on third-party data providers, so availability and accuracy may vary.
- Web scraping can break if the target website changes its HTML structure.
- LLM-generated summaries may contain inaccuracies and should always be reviewed.
- The project does not implement financial risk modeling.
- The project does not provide investment recommendations.
- The project does not include user authentication or persistent user accounts.
- The current implementation is designed for educational and portfolio purposes.

---

## Future Improvements

- Add automated tests for financial data processing
- Add unit tests for API routes
- Add integration tests for report generation
- Add stronger error handling for third-party API failures
- Add support for multiple LLM providers
- Add report export to PDF
- Add authentication for private usage
- Add historical report persistence
- Add better monitoring and observability
- Improve prompt evaluation and output validation
- Add a formal evaluation layer for generated summaries

---

## Author

**Rafael Gutierres**

- GitHub: [rafaelgutierres049](https://github.com/rafaelgutierres049)
- LinkedIn: [Rafael Gutierres](https://www.linkedin.com/in/rafael-gutierres-a314221b5)

---

## Final Note

This project was created to explore the intersection of financial data analysis, backend engineering, web scraping, data visualization, and Generative AI.

The main goal is to demonstrate how LLMs can be integrated into structured analytical workflows using Python, FastAPI, external data sources, and interactive visualizations.
