import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

url = "https://www.infomoney.com.br/cotacoes/empresas-b3/"

#URL_ULTIMAS
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

td = soup.find_all('td', class_="strong")

resultado = []

for a in td:
        link = a.find('a')  
        if link:  # Verifica se a tag <a> foi encontrada
            text = link.get_text(strip=True)
            resultado.append(text)

for a in resultado:
      print(f"\n{a}")

print(len(resultado))