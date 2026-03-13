from pydantic import BaseModel


class RelatorioAcao(BaseModel):
    introducao: str
    analise_impacto_noticias: str
    resumo_diario: str
    analise_semanal: str
    recomendacoes: str
    previsoes_mercado: str
    analise_comparativa: str


class RelatorioBuscaAcoes(BaseModel):
    impacto_noticias: str
    recomendacoes_curto_prazo: str
    recomendacoes_medio_prazo: str
    recomendacoes_longo_prazo: str
    previsoes_mercado: str
    analise_comparativa: str
