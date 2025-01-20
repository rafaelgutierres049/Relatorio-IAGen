# Sistema de Geração de Relatórios utilizando IA Generativa
Este sistema foi desenvolvido para fornecer análises detalhadas e comparações de ações listadas na B3, com base em dados históricos e notícias do mercado. Utilizando IA Generativa, o sistema gera relatórios personalizados para investidores e compara o desempenho de diferentes ações, fornecendo recomendações e previsões de mercado.

## Funcionalidades
1. Geração de relatório de empresa específica
- Geração de Relatório de uma Empresa Específica
- Análise de Impacto das Notícias
- Resumo Diário
- Análise Semanal
- Recomendações
- Previsões de Mercado
- Análise Comparativa
- Gráficos detalhados
2. Comparação de Duas Empresas
- Comparação dos seguintes dados:
- Preço Atual
- P/L (Preço/Lucro)
- Dividend Yield
- Variação ao longo do mês
- Variação ao longo da semana
- Variação ao longo do ano
- A comparação é apresentada com cores para destacar qual empresa se sobressai em cada métrica.
3. Geração de Relatório Diário
O relatório gerado é estruturado em seções específicas, com análise detalhada e recomendações personalizadas:

- Impacto das Notícias no Mercado: Como as notícias afetam o preço das ações.
Recomendações Personalizadas: Estratégias de investimento para diferentes perfis (curto, médio e longo prazo).
- Previsões de Mercado: Previsões sobre o desempenho das ações com base nas notícias e tendências do mercado.
- Análise Comparativa: Comparação de ações dentro do mesmo setor com destaque para as vantagens competitivas.
  
## Tecnologias Utilizadas
- Python
- HTML, CSS, JavaScript
- Flask (para o servidor web)
- OpenAI API (para análises e previsões geradas por IA)
- yfinance (para obter dados históricos de ações)
- BeautifulSoup (para web scraping das notícias financeiras)
- reportlab (para gerar os PDFs dos relatórios)

## Como Rodar o Projeto
1. Clone este repositório:
bash
Copiar
Editar
git clone https://github.com/rafaelgutierres049/Relatorio-IAGen
2. Instale as dependências:
bash
Copiar
Editar
pip install -r requirements.txt
3. Obtenha uma chave de API do OpenAI:
Acesse: https://openai.com/api
Crie sua conta e gere sua chave de API.
4. Substitua a chave de API no arquivo senha.py:
No arquivo senha.py, substitua o valor da chave pela chave que você obteve do OpenAI:

python
Copiar
Editar
api_key = 'sua_chave_api_aqui'
5. Execute o sistema:
bash
Copiar
Editar
python app.py
O sistema irá rodar em um servidor local e fornecer o endereço para você acessar a interface no seu navegador.

## Como Usar
Após executar o sistema, abra o navegador e acesse o endereço local fornecido pelo servidor (geralmente http://127.0.0.1:5000).
Escolha a funcionalidade que deseja utilizar:
Geração de Relatórios de uma Empresa: Selecione a empresa e aguarde a geração do relatório.
Comparação de Empresas: Insira o ticker de duas ações para gerar a comparação entre elas.
Se estiver gerando um relatório de PDF, aguarde cerca de 1 minuto para que o sistema finalize o processo e forneça o arquivo para download.


Criado por: Rafael Ponte Gutierres
