import matplotlib
matplotlib.use('Agg')  # Definir o backend para "Agg" (sem interface gráfica)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import funcionalidades.stocks_data as sd
import asyncio


# Função para gerar o gráfico de fechamento do ano (retorna o objeto Figure)
def fechamento_ano(ticker):
    dados_acao = sd.obter_historico_ano(ticker)
    dados_acao.index = pd.to_datetime(dados_acao.index)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dados_acao.index, dados_acao['Close'], label='Preço de Fechamento')
    
    ax.set_title(f'Histórico de Preços no último ano - {ticker.upper()}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço de Fechamento (R$)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("R${x:,.2f}"))
    ax.legend()
    ax.grid(True)
    
    return fig  

# Função para gerar o gráfico de preços no mês (retorna o objeto Figure)
def precos(ticker):
    dados_acao = sd.obter_historico_mes(ticker)
    dados_acao.index = pd.to_datetime(dados_acao.index)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dados_acao.index, dados_acao['Close'], label='Preço de Fechamento')
    
    ax.set_title(f'Histórico de Preços no último mês - {ticker.upper()}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço de Fechamento (R$)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("R${x:,.2f}"))
    ax.legend()
    ax.grid(True)
    
    return fig  

# Função assíncrona para gerar o gráfico de fechamento do ano
async def gerar_fechamento_ano(ticker):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fechamento_ano, ticker)

# Função assíncrona para gerar o gráfico de preços no mês
async def gerar_precos(ticker):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, precos, ticker)


