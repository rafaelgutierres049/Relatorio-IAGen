import requests
from bs4 import BeautifulSoup


def obter_noticias():
    resultado = []

    url_ultimas = 'https://www.infomoney.com.br/ultimas-noticias/'    
    url_agro = 'https://www.infomoney.com.br/tudo-sobre/agro/'
    url_energia = 'https://www.infomoney.com.br/tudo-sobre/energia/'
    url_global = 'https://www.infomoney.com.br/business/global/'
    url_inovacao = 'https://www.infomoney.com.br/tudo-sobre/inovacao/'
    url_mercados = 'https://www.infomoney.com.br/mercados/'
    url_investimentos = 'https://www.infomoney.com.br/advisor/investimentos/'
    url_politica = 'https://www.infomoney.com.br/politica/'
    url_economia = 'https://www.infomoney.com.br/economia/'
    url_business = 'https://www.infomoney.com.br/business/'

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    
    #URL_ULTIMAS
    response = requests.get(url_ultimas, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    spans = soup.find_all('span', class_="hl-title hl-title-2")


    for span in spans:
        link = span.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)

    #URL_AGRO
    response_agro = requests.get(url_agro, headers=headers)
    soup_agro = BeautifulSoup(response_agro.content, 'html.parser')

    h2_agro = soup_agro.find_all('h2', class_="font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal")


    for h2 in h2_agro:
        link = h2.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)
    
    #URL_ENERGIA
    response_energia = requests.get(url_energia, headers=headers)
    soup_energia = BeautifulSoup(response_energia.content, 'html.parser')

    h2_agro = soup_energia.find_all('h2', class_="font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal")


    for h2 in h2_agro:
        link = h2.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)
    
    #URL_GLOBAL
    response_global = requests.get(url_global, headers=headers)
    soup_global = BeautifulSoup(response_global.content, 'html.parser')

    h2_agro = soup_global.find_all('h2', class_="font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal")


    for h2 in h2_agro:
        link = h2.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)
        
    #URL_INOVAÇÃO
    response_ino = requests.get(url_inovacao, headers=headers)
    soup_ino = BeautifulSoup(response_ino.content, 'html.parser')

    h2_agro = soup_global.find_all('h2', class_="font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal")


    for h2 in h2_agro:
        link = h2.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)
    
    #URL_MERCADOS
    response_mercados = requests.get(url_mercados, headers=headers)
    soup_mercados = BeautifulSoup(response_mercados.content, 'html.parser')

    h3_mercado = soup_mercados.find_all('h3', class_="article-card__headline")


    for h3 in h3_mercado:
        text = h3.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
        resultado.append(text)
    
    #URL_INVESTIMENTOS
    response_invest = requests.get(url_investimentos, headers=headers)
    soup_invest = BeautifulSoup(response_invest.content, 'html.parser')

    h2_agro = soup_invest.find_all('h2', class_="font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal")


    for h2 in h2_agro:
        link = h2.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)
    
    #URL_POLITICA
    response_politica = requests.get(url_politica, headers=headers)
    soup_politica = BeautifulSoup(response_politica.content, 'html.parser')

    h3_mercado = soup_politica.find_all('h3', class_="article-card__headline")


    for h3 in h3_mercado:
        text = h3.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
        resultado.append(text)
   

    #URL_ECONOMIA
    response_economia = requests.get(url_economia, headers=headers)
    soup_economia = BeautifulSoup(response_economia.content, 'html.parser')

    h3_mercado = soup_economia.find_all('h3', class_="article-card__headline")

    for h3 in h3_mercado:
        text = h3.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
        resultado.append(text)

    #URL_BUSINESS
    response_business = requests.get(url_business, headers=headers)
    soup_business = BeautifulSoup(response_business.content, 'html.parser')

    h2_agro = soup_business.find_all('h2', class_="font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal")


    for h2 in h2_agro:
        link = h2.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)  # Extrai o texto da tag <a> e remove espaços extras
            resultado.append(text)

    return resultado

