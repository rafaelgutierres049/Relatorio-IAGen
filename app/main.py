from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime

import app.funcionalidades.stocks_data as sd
import app.chat_integration.chat_integration as ci
import app.funcionalidades.news_data as nd
from app.core.logger import get_logger

logger = get_logger("main")

BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

api = FastAPI(title="Relatorio IAGen")

api.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")
templates = Jinja2Templates(directory=FRONTEND_DIR / "templates")


@api.get("/")
async def home(request: Request):
    logger.info("Página inicial acessada")
    return templates.TemplateResponse("index.html", {"request": request})


@api.get("/relatorio")
async def relatorio_form(request: Request):
    return templates.TemplateResponse("relatorio.html", {"request": request})


@api.post("/relatorio")
async def relatorio_submit(ticker: str = Form(...)):
    logger.info(f"Ticker recebido para relatório: {ticker}")
    return RedirectResponse(url=f"/relatorio/gera?ticker={ticker}", status_code=303)


@api.get("/relatorio/gera")
async def relatorio_gera(request: Request, ticker: str):
    logger.info(f"Iniciando geração de relatório para: {ticker}")
    noticias = await nd.obter_noticias()
    logger.info(f"{len(noticias)} notícias obtidas")
    info_acao = sd.obter_info(ticker)
    logger.info(f"Dados da ação {ticker} obtidos")
    (
        relatorio,
        grafico_fechamento_ano_html,
        grafico_preco_html,
    ) = await ci.gerar_relatorio(ticker, noticias, info_acao)
    logger.info(f"Relatório gerado com sucesso para: {ticker}")
    return templates.TemplateResponse(
        "relatorio_gera.html",
        {
            "request": request,
            "ticker": ticker,
            "relatorio": relatorio.model_dump(),
            "grafico_fechamento_ano_html": grafico_fechamento_ano_html,
            "grafico_preco_html": grafico_preco_html,
        },
    )


@api.get("/compara")
async def comparar_form(request: Request):
    return templates.TemplateResponse("compara.html", {"request": request})


@api.post("/compara")
async def comparar_submit(ticker1: str = Form(...), ticker2: str = Form(...)):
    logger.info(f"Comparação solicitada: {ticker1} vs {ticker2}")
    return RedirectResponse(
        url=f"/compara/acoes?ticker1={ticker1}&ticker2={ticker2}", status_code=303
    )


@api.get("/compara/acoes")
async def comparar_acoes(request: Request, ticker1: str, ticker2: str):
    ticker1 = ticker1.upper()
    ticker2 = ticker2.upper()
    logger.info(f"Comparando ações: {ticker1} vs {ticker2}")
    comparacao = sd.comparar(ticker1, ticker2)
    data_hoje = datetime.today().strftime("%d/%m/%Y")
    logger.info(f"Comparação concluída: {ticker1} vs {ticker2}")
    return templates.TemplateResponse(
        "comparar_acoes.html",
        {
            "request": request,
            "ticker1": ticker1,
            "ticker2": ticker2,
            "comparacao": comparacao,
            "data_hoje": data_hoje,
        },
    )


@api.get("/encontrar")
async def encontrar(request: Request):
    logger.info("Página de descoberta de ações acessada")
    return templates.TemplateResponse("encontrar.html", {"request": request})


@api.get("/encontrar/acoes")
async def encontrar_acoes(request: Request):
    logger.info("Iniciando busca pelas melhores ações")
    acoes = sd.todas_acoes()
    logger.info(f"{len(acoes)} ações obtidas da B3")
    noticias = await nd.obter_noticias()
    logger.info(f"{len(noticias)} notícias obtidas")

    if acoes and noticias:
        encontrado = ci.verificar_melhor(acoes, noticias)
        logger.info("Análise das melhores ações concluída")
        return templates.TemplateResponse(
            "encontrar_acoes.html",
            {"request": request, "encontrado": encontrado.model_dump()},
        )

    logger.warning("Dados insuficientes para análise de ações")
    return templates.TemplateResponse("encontrar_acoes.html", {"request": request})
