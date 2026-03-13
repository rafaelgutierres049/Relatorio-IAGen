import yfinance as yf
import pandas as pd
import requests_cache
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from app.core.logger import get_logger

logger = get_logger("stocks_data")

# brapi.dev: API brasileira de bolsa — sem problemas de crumb/rate-limit do Yahoo Finance.
# Usada para fundamentals (info, P/L, Dividend Yield).
# yfinance continua sendo usado para dados históricos OHLC (endpoint diferente, sem 429).
_BRAPI_BASE = "https://brapi.dev/api"

_SESSION = requests_cache.CachedSession(
    cache_name="finance_cache",
    expire_after=1800,
    allowable_methods=["GET", "POST"],
)
_SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    }
)


def _ticker(symbol: str) -> yf.Ticker:
    # Não passar session: yfinance usa curl_cffi internamente e não é compatível
    return yf.Ticker(f"{symbol.upper()}.SA")


def _brapi_get(ticker: str, **params) -> dict:
    """Busca dados fundamentais via brapi.dev. Retorna {} em caso de falha."""
    url = f"{_BRAPI_BASE}/quote/{ticker.upper()}"
    try:
        resp = _SESSION.get(url, params=params, timeout=15)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if results:
            logger.info(f"Dados de {ticker} obtidos via brapi.dev")
            return results[0]
        logger.warning(f"brapi.dev não retornou resultados para {ticker}")
        return {}
    except Exception as e:
        logger.warning(f"Erro ao buscar {ticker} no brapi.dev: {e}")
        return {}


def obter_preco_atual(ticker: str):
    logger.info(f"Obtendo preço atual de: {ticker}")
    dados = _ticker(ticker).history(period="1d")
    preco_atual = dados["Close"].iloc[-1]
    logger.info(f"Preço atual de {ticker}: R${preco_atual:.2f}")
    return preco_atual


def obter_historico_semana(ticker: str):
    logger.info(f"Obtendo histórico semanal de: {ticker}")
    hoje = datetime.today()
    data_inicio = (hoje - timedelta(weeks=1)).strftime("%Y-%m-%d")
    data_fim = hoje.strftime("%Y-%m-%d")
    dados = _ticker(ticker).history(start=data_inicio, end=data_fim)
    logger.info(f"Histórico semanal obtido para {ticker}: {len(dados)} registros")
    return dados


def obter_historico_mes(ticker: str):
    logger.info(f"Obtendo histórico mensal de: {ticker}")
    try:
        hoje = datetime.today()
        data_inicio = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")
        data_fim = hoje.strftime("%Y-%m-%d")
        dados = _ticker(ticker).history(start=data_inicio, end=data_fim)
        logger.info(f"Histórico mensal obtido para {ticker}: {len(dados)} registros")
        return dados
    except Exception as e:
        logger.warning(f"Não foi possível obter histórico mensal de {ticker}: {e}")
        return pd.DataFrame()


def obter_historico_semestre(ticker: str):
    logger.info(f"Obtendo histórico semestral de: {ticker}")
    hoje = datetime.today()
    data_inicio = (hoje - timedelta(days=182)).strftime("%Y-%m-%d")
    data_fim = hoje.strftime("%Y-%m-%d")
    dados = _ticker(ticker).history(start=data_inicio, end=data_fim)
    logger.info(f"Histórico semestral obtido para {ticker}: {len(dados)} registros")
    return dados


def obter_historico_ano(ticker: str):
    logger.info(f"Obtendo histórico anual de: {ticker}")
    try:
        hoje = datetime.today()
        data_inicio = (hoje - timedelta(days=365)).strftime("%Y-%m-%d")
        data_fim = hoje.strftime("%Y-%m-%d")
        dados = _ticker(ticker).history(start=data_inicio, end=data_fim)
        logger.info(f"Histórico anual obtido para {ticker}: {len(dados)} registros")
        return dados
    except Exception as e:
        logger.warning(f"Não foi possível obter histórico anual de {ticker}: {e}")
        return pd.DataFrame()


def obter_info(ticker: str):
    """Retorna dados fundamentais via brapi.dev (evita 429 do Yahoo Finance)."""
    logger.info(f"Obtendo informações da ação: {ticker}")
    return _brapi_get(
        ticker, modules="summaryProfile,financialData,defaultKeyStatistics"
    )


def obter_dividendos(ticker: str):
    logger.info(f"Obtendo dividendos de: {ticker}")
    dividendo = _ticker(ticker).dividends
    logger.info(f"Dividendos obtidos para {ticker}: {len(dividendo)} registros")
    return dividendo


def comparar(ticker1: str, ticker2: str):
    logger.info(f"Iniciando comparação entre {ticker1} e {ticker2}")

    ticker_yf1 = _ticker(ticker1)
    ticker_yf2 = _ticker(ticker2)

    hoje = datetime.today()
    data_fim = hoje.strftime("%Y-%m-%d")
    data_inicio_semana = (hoje - timedelta(weeks=1)).strftime("%Y-%m-%d")
    data_inicio_mes = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")
    data_inicio_ano = (hoje - timedelta(days=365)).strftime("%Y-%m-%d")

    preco_atual_1 = ticker_yf1.history(period="1d")["Close"].iloc[-1]
    preco_atual_2 = ticker_yf2.history(period="1d")["Close"].iloc[-1]
    logger.info(
        f"Preços atuais: {ticker1}=R${preco_atual_1:.2f}, {ticker2}=R${preco_atual_2:.2f}"
    )

    dados_mes_1 = ticker_yf1.history(start=data_inicio_mes, end=data_fim)[
        ["Close"]
    ].rename(columns={"Close": ticker1})
    dados_mes_2 = ticker_yf2.history(start=data_inicio_mes, end=data_fim)[
        ["Close"]
    ].rename(columns={"Close": ticker2})
    dados_semana_1 = ticker_yf1.history(start=data_inicio_semana, end=data_fim)[
        ["Close"]
    ].rename(columns={"Close": ticker1})
    dados_semana_2 = ticker_yf2.history(start=data_inicio_semana, end=data_fim)[
        ["Close"]
    ].rename(columns={"Close": ticker2})
    dados_ano_1 = ticker_yf1.history(start=data_inicio_ano, end=data_fim)[
        ["Close"]
    ].rename(columns={"Close": ticker1})
    dados_ano_2 = ticker_yf2.history(start=data_inicio_ano, end=data_fim)[
        ["Close"]
    ].rename(columns={"Close": ticker2})

    variacao_mes_1 = (
        (dados_mes_1.iloc[-1] - dados_mes_1.iloc[0]) / dados_mes_1.iloc[0]
    ) * 100
    variacao_mes_2 = (
        (dados_mes_2.iloc[-1] - dados_mes_2.iloc[0]) / dados_mes_2.iloc[0]
    ) * 100
    variacao_semana_1 = (
        (dados_semana_1.iloc[-1] - dados_semana_1.iloc[0]) / dados_semana_1.iloc[0]
    ) * 100
    variacao_semana_2 = (
        (dados_semana_2.iloc[-1] - dados_semana_2.iloc[0]) / dados_semana_2.iloc[0]
    ) * 100
    variacao_ano_1 = (
        (dados_ano_1.iloc[-1] - dados_ano_1.iloc[0]) / dados_ano_1.iloc[0]
    ) * 100
    variacao_ano_2 = (
        (dados_ano_2.iloc[-1] - dados_ano_2.iloc[0]) / dados_ano_2.iloc[0]
    ) * 100

    # P/L e Dividend Yield via brapi.dev (sem 429)
    info1 = _brapi_get(ticker1)
    info2 = _brapi_get(ticker2)

    resumo_comparativo = {
        "Preço Atual": {ticker1: preco_atual_1, ticker2: preco_atual_2},
        "P/L": {
            ticker1: info1.get("priceEarnings", "N/A"),
            ticker2: info2.get("priceEarnings", "N/A"),
        },
        "Dividend Yield": {
            ticker1: info1.get("dividendsYield", "N/A"),
            ticker2: info2.get("dividendsYield", "N/A"),
        },
        "Variação ao longo do mês (%)": {
            ticker1: variacao_mes_1.iloc[0],
            ticker2: variacao_mes_2.iloc[0],
        },
        "Variação ao longo da semana (%)": {
            ticker1: variacao_semana_1.iloc[0],
            ticker2: variacao_semana_2.iloc[0],
        },
        "Variação ao longo do ano (%)": {
            ticker1: variacao_ano_1.iloc[0],
            ticker2: variacao_ano_2.iloc[0],
        },
    }

    logger.info(f"Comparação concluída entre {ticker1} e {ticker2}")
    return resumo_comparativo


def todas_acoes():
    logger.info("Buscando todas as ações da B3")
    url = "https://www.infomoney.com.br/cotacoes/empresas-b3/"
    response = requests.get(url, headers={"User-Agent": _SESSION.headers["User-Agent"]})
    soup = BeautifulSoup(response.content, "html.parser")
    td = soup.find_all("td", class_="strong")

    resultado = []
    for linha in td:
        ticker = linha.find("a")
        if ticker:
            resultado.append(ticker.get_text(strip=True))

    logger.info(f"{len(resultado)} ações encontradas na B3")
    return resultado
