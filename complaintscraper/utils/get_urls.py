import requests
from bs4 import BeautifulSoup
from lxml import etree

base_url = "https://www.reclameaqui.com.br/" #base_url = "https://www.reclameaqui.com.br/santander/"
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64'}

def iosearch():
  
  global header, base_url
  
  iosearch_url = "https://www.reclameaqui.com.br/empresa/santander/lista-reclamacoes/?pagina=1"
  html_content = requests.get(iosearch_url, headers = header, timeout=5 ).text
  soup = BeautifulSoup(html_content, "html.parser")
  
  dom = etree.HTML(str(soup))
  number_of_pages = int(dom.xpath('//*[@id="__next"]/div[1]/div[1]/div[3]/main/section[2]/div[2]/div[2]/div[11]/ul/li[8]')[0].text)
  
  for page in range(6, number_of_pages + 1):
    print(page)
    iosearch_url = f"https://www.reclameaqui.com.br/empresa/santander/lista-reclamacoes/?pagina={page}"
    
    html_content = requests.get(iosearch_url, headers = header).text
    soup = BeautifulSoup(html_content, "html.parser")

    with open('data/urls.txt', 'a', encoding='latin-1') as file:
      for href in range(len(soup.findAll("div",{"class":"bJdtis"}))):
        url = base_url + soup.findAll("div",{"class":"bJdtis"})[href].find_all('a')[0].get('href') + '\n'
        file.write(url)
  
  print("Created Json File!")

if __name__ == "__main__":
  
  res = iosearch()
 