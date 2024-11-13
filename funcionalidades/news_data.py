from bs4 import BeautifulSoup
import aiohttp
import asyncio

# Criação de uma função para fazer a pesquisa conforme os parametros da url, da tag a ser utilizada na pesquisa com o BeautifulSoup, da classe HTML e sessão
async def fetch_news_from_url(url, tag, css_class, session):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), 'html.parser')
            elements = soup.find_all(tag, class_=css_class)
            return [el.get_text(strip=True) for el in elements]
    except Exception as e:
        print(f"Erro ao buscar {url}: {e}")
        return []

# Função a ser utilizada para fazer a busca das notícias de acordo com o site da infomoney
async def obter_noticias():
    urls_info = [
        ('https://www.infomoney.com.br/ultimas-noticias/', 'span', "hl-title hl-title-2"),
        ('https://www.infomoney.com.br/tudo-sobre/agro/', 'h2', "font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal"),
        ('https://www.infomoney.com.br/tudo-sobre/energia/', 'h2', "font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal"),
        ('https://www.infomoney.com.br/business/global/', 'h2', "font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal"),
        ('https://www.infomoney.com.br/tudo-sobre/inovacao/', 'h2', "font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal"),
        ('https://www.infomoney.com.br/mercados/', 'h3', "article-card__headline"),
        ('https://www.infomoney.com.br/advisor/investimentos/', 'h2', "font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal"),
        ('https://www.infomoney.com.br/politica/', 'h3', "article-card__headline"),
        ('https://www.infomoney.com.br/economia/', 'h3', "article-card__headline"),
        ('https://www.infomoney.com.br/business/', 'h2', "font-im-sans text-wl-neutral-950 text-base md:text-lg font-semibold tracking-wide md:tracking-normal"),
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_news_from_url(url, tag, css_class, session) for url, tag, css_class in urls_info]
        noticias = await asyncio.gather(*tasks)
    
    return [item for sublist in noticias for item in sublist]

