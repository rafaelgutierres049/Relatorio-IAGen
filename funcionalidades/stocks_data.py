import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def obter_preco_atual(ticker: str):
    ticker_yf = yf.Ticker(f"{ticker.upper()}.SA")
    preco_atual = ticker_yf.history(period="1d")['Close'].iloc[-1]
    return preco_atual

def obter_historico_semana(ticker: str):
    hoje = datetime.today()
    
    semana_passada = hoje - timedelta(weeks=1)  

    data_inicio = semana_passada.strftime('%Y-%m-%d')
    data_fim = hoje.strftime('%Y-%m-%d')

    ticker_yf = yf.Ticker(f"{ticker}.SA")
    dados = ticker_yf.history(start=data_inicio, end=data_fim)

    return dados

def obter_historico_mes(ticker: str):
    hoje = datetime.today()
    
    mes_passado = hoje - timedelta(days=30)  

    data_inicio = mes_passado.strftime('%Y-%m-%d')
    data_fim = hoje.strftime('%Y-%m-%d')

    ticker_yf = yf.Ticker(f"{ticker}.SA")
    dados = ticker_yf.history(start=data_inicio, end=data_fim)

    return dados

def obter_historico_semestre(ticker: str):
    hoje = datetime.today()
    
    semestre_passado = hoje - timedelta(days=182)  

    data_inicio = semestre_passado.strftime('%Y-%m-%d')
    data_fim = hoje.strftime('%Y-%m-%d')

    ticker_yf = yf.Ticker(f"{ticker}.SA")
    dados = ticker_yf.history(start=data_inicio, end=data_fim)

    return dados

def obter_historico_ano(ticker: str):
    hoje = datetime.today()
    
    um_ano_atras = hoje - timedelta(days=365)  

    data_inicio = um_ano_atras.strftime('%Y-%m-%d')
    data_fim = hoje.strftime('%Y-%m-%d')

    ticker_yf = yf.Ticker(f"{ticker}.SA")
    dados = ticker_yf.history(start=data_inicio, end=data_fim)

    return dados

def obter_info(ticker: str):
    ticker_yf = yf.Ticker(f"{ticker}.SA")
    info_ticker = ticker_yf.info
    return info_ticker

def obter_dividendos(ticker: str):
    ticker_yf = yf.Ticker(f"{ticker}.SA")
    dividendo = ticker_yf.dividends
    return dividendo

def comparar(ticker1: str, ticker2: str):
    # Obter os dados dos tickers
    ticker_yf1 = yf.Ticker(f"{ticker1}.SA")
    ticker_yf2 = yf.Ticker(f"{ticker2}.SA")

    # Definir as datas
    hoje = datetime.today()
    mes_passado = hoje - timedelta(days=30)
    semana_passada = hoje - timedelta(weeks=1)
    ano_passado = hoje - timedelta(days=365)

    data_inicio_semana = semana_passada.strftime('%Y-%m-%d')
    data_inicio_mes = mes_passado.strftime('%Y-%m-%d')
    data_inicio_ano = ano_passado.strftime('%Y-%m-%d')

    data_fim = hoje.strftime('%Y-%m-%d')

    # Preço atual
    preco_atual_ticker_yf1 = ticker_yf1.history(period="1d")['Close'].iloc[-1]
    preco_atual_ticker_yf2 = ticker_yf2.history(period="1d")['Close'].iloc[-1]

    # Histórico de preços ao longo do mês, semana e ano
    dados_mes_1 = ticker_yf1.history(start=data_inicio_mes, end=data_fim)[['Close']].rename(columns={'Close': ticker1.upper()})
    dados_mes_2 = ticker_yf2.history(start=data_inicio_mes, end=data_fim)[['Close']].rename(columns={'Close': ticker2.upper()})
    
    dados_semana_1 = ticker_yf1.history(start=data_inicio_semana, end=data_fim)[['Close']].rename(columns={'Close': ticker1.upper()})
    dados_semana_2 = ticker_yf2.history(start=data_inicio_semana, end=data_fim)[['Close']].rename(columns={'Close': ticker2.upper()})
    
    dados_ano_1 = ticker_yf1.history(start=data_inicio_ano, end=data_fim)[['Close']].rename(columns={'Close': ticker1.upper()})
    dados_ano_2 = ticker_yf2.history(start=data_inicio_ano, end=data_fim)[['Close']].rename(columns={'Close': ticker2.upper()})

    # Calcular a variação percentual para o mês, semana e ano
    variacao_mes_1 = ((dados_mes_1.iloc[-1] - dados_mes_1.iloc[0]) / dados_mes_1.iloc[0]) * 100
    variacao_mes_2 = ((dados_mes_2.iloc[-1] - dados_mes_2.iloc[0]) / dados_mes_2.iloc[0]) * 100
    
    variacao_semana_1 = ((dados_semana_1.iloc[-1] - dados_semana_1.iloc[0]) / dados_semana_1.iloc[0]) * 100
    variacao_semana_2 = ((dados_semana_2.iloc[-1] - dados_semana_2.iloc[0]) / dados_semana_2.iloc[0]) * 100
    
    variacao_ano_1 = ((dados_ano_1.iloc[-1] - dados_ano_1.iloc[0]) / dados_ano_1.iloc[0]) * 100
    variacao_ano_2 = ((dados_ano_2.iloc[-1] - dados_ano_2.iloc[0]) / dados_ano_2.iloc[0]) * 100

    # Verificar e obter dados financeiros adicionais
    p_l_1 = ticker_yf1.info.get('trailingPE', 'N/A')
    p_l_2 = ticker_yf2.info.get('trailingPE', 'N/A')

    dividend_yield_1 = ticker_yf1.info.get('dividendYield', 'N/A')
    dividend_yield_2 = ticker_yf2.info.get('dividendYield', 'N/A')

    # Resumo comparativo
    resumo_comparativo = {
        'Preço Atual': {ticker1: preco_atual_ticker_yf1, ticker2: preco_atual_ticker_yf2},
        'P/L': {ticker1: p_l_1, ticker2: p_l_2},
        'Dividend Yield': {ticker1: dividend_yield_1, ticker2: dividend_yield_2},
        'Variação ao longo do mês (%)': {ticker1: variacao_mes_1.iloc[0], ticker2: variacao_mes_2.iloc[0]},
        'Variação ao longo da semana (%)': {ticker1: variacao_semana_1.iloc[0], ticker2: variacao_semana_2.iloc[0]},
        'Variação ao longo do ano (%)': {ticker1: variacao_ano_1.iloc[0], ticker2: variacao_ano_2.iloc[0]},
    }

    return resumo_comparativo
    
def todas_acoes():
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

    url = "https://www.infomoney.com.br/cotacoes/empresas-b3/"

    #URL_ULTIMAS
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    td = soup.find_all('td', class_="strong")

    resultado = []

    for linha in td:
            ticker = linha.find('a')  
            if ticker: 
                text = ticker.get_text(strip=True)
                resultado.append(text)

    return resultado





