import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import app.funcionalidades.stocks_data as sd
import asyncio
from app.core.logger import get_logger

logger = get_logger("graficos")

_ACCENT = "#63adfd"
_GREEN = "#6fcf97"
_RED = "#eb5757"
_BG = "#0a0a0a"
_SURFACE = "#111111"
_BORDER = "rgba(255,255,255,0.08)"
_MUTED = "#888888"

_LAYOUT_BASE = dict(
    paper_bgcolor=_BG,
    plot_bgcolor=_SURFACE,
    font=dict(color="#f0f0f0", size=12, family="Montserrat, sans-serif"),
    xaxis=dict(
        showgrid=True,
        gridcolor=_BORDER,
        showline=False,
        zeroline=False,
        tickfont=dict(color=_MUTED),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor=_BORDER,
        showline=False,
        zeroline=False,
        tickfont=dict(color=_MUTED),
        tickprefix="R$",
    ),
    margin=dict(l=70, r=20, t=60, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=_BORDER),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#1a1a1a",
        bordercolor=_BORDER,
        font=dict(color="#f0f0f0"),
    ),
)


def _empty_chart(title: str) -> str:
    fig = go.Figure()
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text=title, font=dict(size=15, color="#f0f0f0"), x=0.02),
        annotations=[
            dict(
                text="Dados indisponíveis no momento",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(color=_MUTED, size=14),
            )
        ],
        height=360,
    )
    return fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config={"displayModeBar": False, "responsive": True},
    )


def fechamento_ano(ticker: str) -> str:
    logger.info(f"Gerando gráfico de fechamento anual para: {ticker}")
    dados = sd.obter_historico_ano(ticker)
    if dados.empty:
        logger.warning(f"Dados anuais vazios para {ticker}, retornando gráfico vazio")
        return _empty_chart(f"Histórico Anual — {ticker.upper()}")
    dados.index = pd.to_datetime(dados.index)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.04,
    )

    fig.add_trace(
        go.Candlestick(
            x=dados.index,
            open=dados["Open"],
            high=dados["High"],
            low=dados["Low"],
            close=dados["Close"],
            name="Preço",
            increasing=dict(line=dict(color=_GREEN, width=1), fillcolor=_GREEN),
            decreasing=dict(line=dict(color=_RED, width=1), fillcolor=_RED),
            hovertext=dados.index.strftime("%d/%m/%Y"),
        ),
        row=1,
        col=1,
    )

    colors = [_GREEN if c >= o else _RED for c, o in zip(dados["Close"], dados["Open"])]

    fig.add_trace(
        go.Bar(
            x=dados.index,
            y=dados["Volume"],
            name="Volume",
            marker_color=colors,
            opacity=0.5,
            hovertemplate="%{y:,.0f}<extra>Volume</extra>",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(
            text=f"Histórico Anual — {ticker.upper()}",
            font=dict(size=15, color="#f0f0f0"),
            x=0.02,
        ),
        xaxis_rangeslider_visible=False,
        yaxis2=dict(
            showgrid=True,
            gridcolor=_BORDER,
            showline=False,
            zeroline=False,
            tickfont=dict(color=_MUTED),
            tickformat=".2s",
            title=dict(text="Volume", font=dict(color=_MUTED, size=11)),
        ),
        height=500,
    )

    logger.info(f"Gráfico de fechamento anual gerado para: {ticker}")
    return fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config={"displayModeBar": False, "responsive": True},
    )


def precos(ticker: str) -> str:
    logger.info(f"Gerando gráfico de preços mensais para: {ticker}")
    dados = sd.obter_historico_mes(ticker)
    if dados.empty:
        logger.warning(f"Dados mensais vazios para {ticker}, retornando gráfico vazio")
        return _empty_chart(f"Preço no Último Mês — {ticker.upper()}")
    dados.index = pd.to_datetime(dados.index)

    preco_inicio = dados["Close"].iloc[0]
    preco_fim = dados["Close"].iloc[-1]
    cor_linha = _GREEN if preco_fim >= preco_inicio else _RED
    cor_fill = (
        "rgba(111,207,151,0.08)"
        if preco_fim >= preco_inicio
        else "rgba(235,87,87,0.08)"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dados.index,
            y=dados["Close"],
            mode="lines",
            name="Fechamento",
            line=dict(color=cor_linha, width=2),
            fill="tozeroy",
            fillcolor=cor_fill,
            hovertemplate="<b>R$%{y:.2f}</b><br>%{x|%d/%m/%Y}<extra></extra>",
        )
    )

    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(
            text=f"Preço no Último Mês — {ticker.upper()}",
            font=dict(size=15, color="#f0f0f0"),
            x=0.02,
        ),
        height=360,
        showlegend=False,
    )

    logger.info(f"Gráfico de preços mensais gerado para: {ticker}")
    return fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config={"displayModeBar": False, "responsive": True},
    )


async def gerar_fechamento_ano(ticker: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fechamento_ano, ticker)


async def gerar_precos(ticker: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, precos, ticker)
