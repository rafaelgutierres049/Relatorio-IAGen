Sistema de Geração de Relatórios utilizando IA Generativa

Descrição
Sistema que envia dados de ações buscadas no site da infomoney, assim como resultados de cálculos matemáticos utilizando esses dados para a API da OpenAI, que realiza previsões e comparações de acordo com notícias e dados históricos das ações listadas na B3.

Funcionalidades
- Geração de relatório de uma empresa específica:
    Realiza as seguintes funções relacionadas a uma empresa que o usuário escolher: Análise de Impacto das Notícias, Resumo Diário, Análise Semanal,Recomendações, Previsões de Mercado, Análise Comparativa e gráficos.

- Comparação de duas empresas:
    Realiza a comparação dos dados de Preço Atual, P/L, Dividend Yield, Variação ao longo do mês, Variação ao longo da semana e Variação ao longo do ano de duas empresas. O sistema mostra para o usuário por meio de cores qual empresa se sobressai.

- Greração de relatório diário:
    O relatório segue uma estrutura predefinida, com seções específicas para análise e recomendações, e é personalizado com os dados fornecidos. As principais etapas e partes incluem:

    Impacto das Notícias no Mercado: Avalia como as notícias fornecidas afetam as ações, considerando mudanças de preços e impacto econômico.

    Recomendações Personalizadas por Perfil de Investimento: Fornece recomendações para investidores com diferentes horizontes de tempo (curto, médio e longo prazo), levando em conta a volatilidade das ações e o impacto das notícias. As sugestões incluem estratégias claras de compra, venda ou manutenção.

    Previsões de Mercado: Faz previsões detalhadas para as ações analisadas, com base nas notícias e nas tendências do mercado.

    Análise Comparativa: Compara as ações fornecidas com concorrentes do setor, destacando vantagens competitivas com base nas notícias e métricas financeiras.

Tecnologias Utilizadas
Python, HTML, CSS, JavaScript, Flask

Como Rodar o Projeto
- Clone este repositório:
    https://github.com/rafaelgutierres049/Relatorio-IAGen

- Instale as dependências:
    pip install -r requirements.txt

- Obtenha uma chave de API do OpenAI
    https://openai.com/api/
    Substitua em senha.py a sua chave de API

- Execute o sistema:
    python app.py

Como Usar
- Após executar o sistema, acesse o endereço local fornecido pelo servidor para acessar a interface do sistema.
- Selecione a funcionalidade que deseja utilizar
- No caso de ser uma relacionada a geração de PDFs, aguarde 1 minuto para que o sistema gere o relatório
- No caso de ser a comparação de empresa, deverá entrar com o Ticker de duas ações que deseja fazer a comparação
