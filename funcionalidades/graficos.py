import matplotlib.pyplot as plt
import pandas as pd
import funcionalidades.stocks_data as sd

def fechamento_ano(ticker):
    dados_acao = sd.obter_historico_ano(ticker)
    dados_acao.index = pd.to_datetime(dados_acao.index)
    
    # Criando a figura e os eixos do gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dados_acao.index, dados_acao['Close'], label='Preço de Fechamento')
    ax.set_title(f'Histórico de Preços no último ano - {ticker.upper()}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço de Fechamento (R$)')
    ax.legend()
    ax.grid(True)
    
    return fig

def precos(ticker):
    dados_acao = sd.obter_historico_mes(ticker)
    dados_acao.index = pd.to_datetime(dados_acao.index)
    
    # Criando a figura e os eixos do gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dados_acao.index, dados_acao['Open'], label='Abertura', alpha=0.7)
    ax.plot(dados_acao.index, dados_acao['High'], label='Máxima', alpha=0.7)
    ax.plot(dados_acao.index, dados_acao['Low'], label='Mínima', alpha=0.7)
    ax.plot(dados_acao.index, dados_acao['Close'], label='Fechamento', alpha=0.9, linewidth=2)
    
    # Configurando título e rótulos
    ax.set_title(f'Histórico de Preços no último mês - {ticker.upper()}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço (R$)')
    ax.legend(loc='best')
    ax.grid(True)
    
    # Retornando o objeto Figure
    return fig
