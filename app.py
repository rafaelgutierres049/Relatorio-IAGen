from flask import Flask, render_template, request, redirect, url_for
import funcionalidades.stocks_data as sd
import funcionalidades.chat_integration as ci
import funcionalidades.scrapping_news as sn
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/relatorio', methods=['GET', 'POST'])
def relatorio():
    if request.method == 'POST':
        ticker = request.form['ticker']
        return redirect(url_for('relatorio_gera', ticker=ticker))
    return render_template('relatorio.html')

@app.route('/relatorio/gera')
def relatorio_gera():
    ticker = request.args.get('ticker')
    if ticker:
        noticias = sn.obter_noticias()
        info_acao = sd.obter_info(ticker)
        relatorio, grafico_fechamento_ano_base64, grafico_preco_base64 = ci.gerar_relatorio(ticker, noticias, info_acao)

        return render_template('relatorio_gera.html', ticker=ticker, relatorio=relatorio, 
                               grafico_fechamento_ano_url=grafico_fechamento_ano_base64, 
                               grafico_preco_url=grafico_preco_base64)
    
    return redirect(url_for('relatorio'))

@app.route('/compara', methods=['GET', 'POST'])
def comparar():
    if request.method == 'POST':
        ticker1 = request.form['ticker1']
        ticker2 = request.form['ticker2']
        return redirect(url_for('comparar_acoes', ticker1=ticker1, ticker2=ticker2))
    return render_template('compara.html')

@app.route('/compara/acoes')
def comparar_acoes():
    ticker1 = request.args.get('ticker1')
    ticker2 = request.args.get('ticker2')
    hoje = datetime.today()
    data_hoje = hoje.strftime('%d/%m/%Y')
    
    if ticker1 and ticker2:
        comparacao = sd.comparar(ticker1, ticker2)
        return render_template('comparar_acoes.html', ticker1=ticker1, ticker2=ticker2, comparacao=comparacao, data_hoje=data_hoje)
    
    return redirect(url_for('comparar'))

@app.route('/encontrar')
def encontrar():
    return render_template('encontrar.html')

@app.route('/encontrar/acoes')
def encontrar_acoes():
    acoes = sd.todas_acoes()
    noticias = sn.obter_noticias()

    if acoes and noticias:
        encontrado = ci.verificar_melhor(acoes, noticias) 
        return render_template('encontrar_acoes.html', encontrado=encontrado)
    return render_template('encontrar_acoes.html')

if __name__ == '__main__':
    app.run(debug=True)