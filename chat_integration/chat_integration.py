import matplotlib.pyplot as plt
import requests
import io
import base64
from chat_integration.senha import OPENAI_API_KEY
import funcionalidades.graficos as graficos

headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
url = "https://api.openai.com/v1/chat/completions"

# Função assíncrona para gerar o relatório com gráficos
async def gerar_relatorio(ticker, noticias, dados_acao):
    # Definindo o prompt
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
    # Criando o JSON para enviar para a API
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Você é um analista financeiro experiente."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    # Realizando a requisição à API do OpenAI
    response = requests.post(url, headers=headers, json=data)

    # Verificar se a requisição foi bem sucedida
    if response.status_code == 200:
        resultado = response.json()
        resposta = resultado['choices'][0]['message']['content']
    else:
        print("Erro na requisição:")
        print(response.status_code, response.text)
        resposta = f"Erro ao gerar relatório: {response.status_code} - {response.text}"

    # Gerando gráficos 
    fig = await graficos.gerar_fechamento_ano(ticker)
    fig2 = await graficos.gerar_precos(ticker)

    # Salvando gráficos em base64
    try:
        img = io.BytesIO()  # Garantindo que img seja do tipo BytesIO
        img2 = io.BytesIO()  # Garantindo que img2 seja do tipo BytesIO

        # Salvando o primeiro gráfico
        fig.savefig(img, format='png')  # Salva o gráfico em img, que é um objeto BytesIO
        img.seek(0)  # Retorna ao início do BytesIO
        grafico_fechamento_ano_base64 = base64.b64encode(img.getvalue()).decode()  # Codifica para base64

        # Salvando o segundo gráfico
        fig2.savefig(img2, format='png')  # Salva o gráfico em img2, que também é um BytesIO
        img2.seek(0)  # Retorna ao início do BytesIO
        grafico_preco_base64 = base64.b64encode(img2.getvalue()).decode()  # Codifica para base64

    finally:
        # Fechar as figuras para liberar a memória
        plt.close(fig)
        plt.close(fig2)

    return resposta, grafico_fechamento_ano_base64, grafico_preco_base64


# Função de verificação das melhores ações (não precisa ser assíncrona, pois não faz operações assíncronas)
def verificar_melhor(acoes, noticias):
    # Definindo o prompt
    prompt = (
        "Elabore um relatório detalhado para identificar as melhores oportunidades de investimento com base nas ações e notícias fornecidas. "
        "Este relatório deve incluir análises profundas, justificativas bem fundamentadas e recomendações para cada perfil de investidor. As informações de ações e notícias são as seguintes:\n\n"
        f"Ações em Análise: {acoes}\n"
        f"Principais Notícias: {noticias}\n\n"
        
        "Estrutura do Relatório:\n\n"
        
        "*Impacto das Notícias no Mercado*\n"
        "- Avalie o impacto de cada notícia nas ações fornecidas, considerando possíveis mudanças nos preços e no cenário econômico.\n\n"
        
        "*Recomendações Personalizadas por Perfil de Investimento*\n"
        "- Forneça recomendações detalhadas para cada perfil de investidor com base nas ações e notícias fornecidas:\n"
        "#Curto Prazo# Identifique as ações que apresentam volatilidade ou potencial para ganhos rápidos devido às notícias. Inclua sugestões claras de compra, venda ou manutenção.\n"
        "#Médio Prazo# Destaque ações com bom equilíbrio entre risco e retorno, considerando as notícias e as tendências de mercado. Justifique a escolha dessas ações com base no impacto das notícias.\n"
        "#Longo Prazo# Aponte ações com fundamentos sólidos e boas perspectivas de crescimento sustentável, apesar de possíveis flutuações no curto prazo. Justifique a escolha dessas ações com base em análises financeiras e impacto das notícias.\n\n"
        
        "*Previsões de Mercado*\n"
        "- Faça previsões detalhadas para as ações analisadas, considerando o impacto das notícias e a tendência do mercado.\n\n"
        
        "*Análise Comparativa*\n"
        "- Compare as ações com concorrentes do setor, destacando as vantagens competitivas de cada uma com base nas notícias e métricas financeiras.\n"
    )
    
    # Criando o JSON para enviar para a API
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Você é um analista financeiro experiente. Seu objetivo é criar um relatório detalhado e bem fundamentado que ajude o investidor a tomar decisões informadas."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)

    # Verificaa se a requisição foi bem sucedida
    if response.status_code == 200:
        resultado = response.json()
        resposta = resultado['choices'][0]['message']['content']
    else:
        print("Erro na requisição:")
        print(response.status_code, response.text)
        resposta = f"Erro ao gerar relatório: {response.status_code} - {response.text}"

    return resposta