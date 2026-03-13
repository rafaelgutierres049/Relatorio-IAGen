import json
import requests
import app.core.config as config
import app.funcionalidades.graficos as graficos
from app.core.logger import get_logger
from app.core.schemas import RelatorioAcao, RelatorioBuscaAcoes

logger = get_logger("chat_integration")

headers = {"Authorization": f"Bearer {config.OPENAI_API_KEY}"}
url = "https://api.openai.com/v1/chat/completions"


async def gerar_relatorio(ticker, noticias, dados_acao):
    logger.info(f"Gerando relatório para a ação: {ticker}")

    prompt = (
        f"Gere um relatório financeiro detalhado para a ação {ticker}.\n\n"
        f"Notícias recentes:\n{noticias}\n\n"
        f"Dados da ação:\n{dados_acao}\n\n"
        "IMPORTANTE: Responda APENAS com um JSON válido onde TODOS os valores são strings de texto corrido em português. "
        "Não use objetos aninhados, arrays, chaves extras nem formatação JSON dentro dos valores. "
        "Cada campo deve conter um parágrafo de texto simples, como se fosse uma redação.\n\n"
        "Formato exato esperado (substitua os exemplos pelo conteúdo real):\n"
        "{\n"
        f'  "introducao": "Texto corrido com a visão geral de {ticker} e seu contexto no mercado.",\n'
        f'  "analise_impacto_noticias": "Texto corrido descrevendo como cada notícia relevante pode impactar {ticker}.",\n'
        f'  "resumo_diario": "Texto corrido sobre o desempenho recente de {ticker} com as variações mais importantes.",\n'
        f'  "analise_semanal": "Texto corrido sobre as tendências semanais de {ticker} com base nos dados históricos.",\n'
        f'  "recomendacoes": "Texto corrido com a recomendação clara de compra, venda ou manutenção de {ticker} e sua justificativa.",\n'
        f'  "previsoes_mercado": "Texto corrido com as previsões de movimentos futuros de {ticker}.",\n'
        f'  "analise_comparativa": "Texto corrido comparando {ticker} com o setor e o mercado em geral."\n'
        "}"
    )

    data = {
        "model": config.OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é um analista financeiro experiente. Responda sempre com JSON válido onde todos os valores são strings de texto corrido em português. Nunca use objetos, arrays ou JSON aninhado dentro dos valores.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": config.OPENAI_TEMPERATURE,
        "response_format": {"type": "json_object"},
    }

    logger.info(f"Enviando requisição à API OpenAI (model={config.OPENAI_MODEL})")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        raw = response.json()["choices"][0]["message"]["content"]
        logger.info(f"Relatório recebido com sucesso para: {ticker}")
        try:
            relatorio = RelatorioAcao(**json.loads(raw))
        except Exception as e:
            logger.error(f"Erro ao parsear JSON do relatório: {e}")
            relatorio = RelatorioAcao(
                introducao=raw,
                analise_impacto_noticias="",
                resumo_diario="",
                analise_semanal="",
                recomendacoes="",
                previsoes_mercado="",
                analise_comparativa="",
            )
    else:
        logger.error(
            f"Erro na requisição OpenAI: {response.status_code} - {response.text}"
        )
        relatorio = RelatorioAcao(
            introducao=f"Erro ao gerar relatório: {response.status_code}",
            analise_impacto_noticias="",
            resumo_diario="",
            analise_semanal="",
            recomendacoes="",
            previsoes_mercado="",
            analise_comparativa="",
        )

    logger.info(f"Gerando gráficos para: {ticker}")
    grafico_fechamento_ano_html = await graficos.gerar_fechamento_ano(ticker)
    grafico_preco_html = await graficos.gerar_precos(ticker)
    logger.info(f"Gráficos gerados com sucesso para: {ticker}")

    return relatorio, grafico_fechamento_ano_html, grafico_preco_html


def verificar_melhor(acoes, noticias):
    logger.info(f"Analisando melhores ações entre {len(acoes)} candidatas")

    prompt = (
        "Identifique as melhores oportunidades de investimento com base nas ações e notícias fornecidas.\n\n"
        f"Ações em análise: {acoes}\n\n"
        f"Principais notícias: {noticias}\n\n"
        "IMPORTANTE: Responda APENAS com um JSON válido onde TODOS os valores são strings de texto corrido em português. "
        "Não use objetos aninhados, arrays, chaves extras nem formatação JSON dentro dos valores. "
        "Cada campo deve conter um parágrafo de texto simples, como se fosse uma redação.\n\n"
        "Formato exato esperado (substitua os exemplos pelo conteúdo real):\n"
        "{\n"
        '  "impacto_noticias": "Texto corrido descrevendo o impacto de cada notícia relevante nas ações analisadas.",\n'
        '  "recomendacoes_curto_prazo": "Texto corrido com as ações recomendadas para curto prazo, mencionando os tickers e justificativas diretamente no parágrafo.",\n'
        '  "recomendacoes_medio_prazo": "Texto corrido com as ações recomendadas para médio prazo, com justificativas.",\n'
        '  "recomendacoes_longo_prazo": "Texto corrido com as ações recomendadas para longo prazo, com fundamentos.",\n'
        '  "previsoes_mercado": "Texto corrido com previsões de mercado para as principais ações analisadas.",\n'
        '  "analise_comparativa": "Texto corrido comparando as melhores ações com concorrentes do setor."\n'
        "}"
    )

    data = {
        "model": config.OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é um analista financeiro experiente. Responda sempre com JSON válido onde todos os valores são strings de texto corrido em português. Nunca use objetos, arrays ou JSON aninhado dentro dos valores.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": config.OPENAI_TEMPERATURE,
        "response_format": {"type": "json_object"},
    }

    logger.info(f"Enviando requisição à API OpenAI (model={config.OPENAI_MODEL})")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        raw = response.json()["choices"][0]["message"]["content"]
        logger.info("Análise das melhores ações recebida com sucesso")
        try:
            relatorio = RelatorioBuscaAcoes(**json.loads(raw))
        except Exception as e:
            logger.error(f"Erro ao parsear JSON da análise: {e}")
            relatorio = RelatorioBuscaAcoes(
                impacto_noticias=raw,
                recomendacoes_curto_prazo="",
                recomendacoes_medio_prazo="",
                recomendacoes_longo_prazo="",
                previsoes_mercado="",
                analise_comparativa="",
            )
    else:
        logger.error(
            f"Erro na requisição OpenAI: {response.status_code} - {response.text}"
        )
        relatorio = RelatorioBuscaAcoes(
            impacto_noticias=f"Erro ao gerar relatório: {response.status_code}",
            recomendacoes_curto_prazo="",
            recomendacoes_medio_prazo="",
            recomendacoes_longo_prazo="",
            previsoes_mercado="",
            analise_comparativa="",
        )

    return relatorio
