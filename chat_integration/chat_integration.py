from chat_integration.senha import OPENAI_API_KEY
import requests
import funcionalidades.graficos as graficos 
import io
import base64
import matplotlib.pyplot as plt

headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

url = "https://api.openai.com/v1/chat/completions"

def gerar_relatorio(ticker, noticias, dados_acao):
    prompt = (
    f"Gostaria que você gerasse um relatório financeiro detalhado para a ação {ticker}. Abaixo estão as principais notícias do mundo neste momento e os dados mais recentes da ação.\n\n"
    f"Notícias:\n{noticias}\n\n"
    f"Dados da Ação:\n{dados_acao}\n\n"
    "Por favor, organize o relatório da seguinte forma:\n"
    f" **Análise de Impacto das Notícias** Verifique os cabeçalhos das notícias e avalie se há alguma possibilidade de impacto significativo na ação {ticker} com base nas informações fornecidas. Considere como cada notícia pode afetar a ação, seja de forma positiva ou negativa.\n"
    f" **Resumo Diário** Crie um resumo que inclua o desempenho recente da ação, destacando quaisquer variações importantes e o impacto potencial das notícias mais recentes.\n"
    f" **Análise Semanal** Inclua uma breve análise de tendências semanais para a ação {ticker}, com base nos dados históricos e nas notícias recentes. Identifique padrões ou mudanças significativas.\n"
    f" **Recomendações** Forneça recomendações sobre compra, venda ou manutenção da ação {ticker} com base na análise das notícias e dados. Explique a lógica por trás das recomendações.\n"
    f" **Previsões de Mercado** Utilize dados históricos e as notícias recentes para prever possíveis movimentos futuros da ação {ticker}. Sugira ações estratégicas com base nessas previsões.\n"
    f" **Análise Comparativa** Se possível, compare a ação {ticker} com outras ações similares ou com o mercado em geral, usando as métricas financeiras disponíveis e as notícias recentes para fornecer um contexto mais amplo.\n\n"
    "Formato do Relatório:\n"
    f"Introdução com uma visão geral da ação {ticker}.\n"
    "Análise detalhada das notícias e seu impacto.\n"
    "Recomendações de compra/venda/manutenção.\n"
    f"Por favor, elabore o relatório com base nesses pontos, foque na parte de análise de impacto das notícias, previsões de mercado, recomendações, e forneça uma visão clara e objetiva sobre a ação {ticker}."
)

    # Criando o corpo da requisição
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Você é um analista financeiro experiente."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    # Fazendo a requisição para a API da OpenAI
    response = requests.post(url, headers=headers, json=data)

    # Exibindo a resposta
    if response.status_code == 200:
        resultado = response.json()
        resposta = resultado['choices'][0]['message']['content']
    else:
        print("Erro na requisição:")
        print(response.status_code, response.text)
        resposta = f"Erro ao gerar relatório: {response.status_code} - {response.text}"

    # Gerando o gráfico de fechamento anual
    fig = graficos.fechamento_ano(ticker)
    fig2 = graficos.precos(ticker)
    
    # Convertendo o gráfico para Base64
    
    img = io.BytesIO()
    img2 = io.BytesIO()

    fig.savefig(img, format='png')
    img.seek(0)
    grafico_fechamento_ano_base64 = base64.b64encode(img.getvalue()).decode()

    fig2.savefig(img2, format='png')
    img2.seek(0)
    grafico_preco_base64 = base64.b64encode(img2.getvalue()).decode()

    # Fechando o gráfico para liberar memória
    plt.close(fig)
    plt.close(fig2)


    return resposta, grafico_fechamento_ano_base64, grafico_preco_base64


def verificar_melhor(acoes, noticias):
    prompt = (
    "Preciso que você elabore um relatório detalhado, identificando as melhores ações para investimento com base no perfil do investidor, seja de curto, médio ou longo prazo. Abaixo estão as ações em análise e as principais notícias globais atuais:"
    f"Ações em Análise: {acoes}"
    f"Principais Notícias: {noticias}"
    "Por favor, organize o relatório da seguinte forma"
    " **Impacto das Notícias no Mercado** Analise as manchetes das notícias fornecidas e identifique possíveis impactos significativos no mercado em geral e nas ações listadas. Considere o contexto econômico e geopolítico para prever como esses eventos podem influenciar os preços das ações a curto, médio e longo prazo."
    " **Recomendações Personalizadas por Perfil de Investimento**"
    "Curto Prazo: Identifique as ações mais voláteis ou aquelas que podem se beneficiar de movimentos rápidos devido a notícias recentes. Forneça recomendações de compra, venda ou manutenção para esse perfil."
    "Médio Prazo: Selecione as ações que apresentam um bom equilíbrio entre risco e retorno, considerando o impacto potencial das notícias e as tendências do mercado. Sugira estratégias de investimento adequadas para investidores de médio prazo."
    "Longo Prazo: Indique as ações com fundamentos sólidos e que, apesar de possíveis flutuações no curto prazo, têm boas perspectivas de crescimento sustentado no longo prazo. Faça recomendações de investimento para esse perfil."
    " **Previsões de Mercado** Baseando-se em dados históricos, nas notícias recentes e nas tendências atuais, faça previsões sobre os possíveis movimentos futuros das ações selecionadas para cada perfil de investimento. Proponha ações estratégicas que o investidor pode tomar em resposta a essas previsões."
    " **Análise Comparativa** Compare a ação que se destaca em cada perfil (curto, médio, longo prazo) em relação às outras, usando métricas financeiras e as notícias recentes. Forneça uma visão geral de por que essa ação é a melhor escolha em seu respectivo perfil e como ela se posiciona frente ao cenário atual do mercado."
    )
    # Criando o corpo da requisição
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Você é um analista financeiro experiente."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    # Fazendo a requisição para a API da OpenAI
    response = requests.post(url, headers=headers, json=data)

    # Exibindo a resposta
    if response.status_code == 200:
        resultado = response.json()
        resposta = resultado['choices'][0]['message']['content']
    else:
        print("Erro na requisição:")
        print(response.status_code, response.text)
        resposta = f"Erro ao gerar relatório: {response.status_code} - {response.text}"

    return resposta