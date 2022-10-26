import requests
from bs4 import BeautifulSoup

headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

r = requests.get("https://www.reclameaqui.com.br/santander/acordo-nao-feito-pelo-banco_wEuRs5rN_7-psbaA/")
soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
print(soup)