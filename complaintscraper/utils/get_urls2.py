# Import the required modules
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import json
import urllib.request
import urllib 

import unicodedata
import re


base_url = "https://www.reclameaqui.com.br/santander/"
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
          'AppleWebKit/537.11 (KHTML, like Gecko) '
          'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

def get_complaint(content):
  
  #dataCleaning = DataCleaning()
  #complaintItem = ComplaintItem()
  
  print(content)
  '''
  complaintItem['id']               = content.find('span', attrs={'data-testid': 'complaint-id'}).text.split()[1]
  complaintItem['title']            = content.find('h1', attrs={'data-testid': 'complaint-title'}).text
  complaintItem['solved']           = self.get_data(data, "props.pageProps.complaint.solved")
  complaintItem['description']      = content.find('p', attrs={'data-testid': 'complaint-description'}).text
  complaintItem['url']              = response.url

  content_container                 = response.xpath('//*[contains(@data-testid, "complaint-content-container")]//text()').extract()
  complaintItem['tags']             = content_container[content_container.index("ID:") + 2 : content_container.index("Status da reclamação:")]
  complaintItem['status']           = content.find('div', attrs={'data-testid': 'complaint-status'}).text
   
  complaintItem['userCity']         = self.get_data(data, "props.pageProps.complaint.userCity")
  complaintItem['userState']        = self.get_data(data, "props.pageProps.complaint.userState")
  complaintItem['creation_date']    = self.get_data(data, "props.pageProps.complaint.created")
    
  #Interactions contain customer and company replicas.
  complaintItem['interactions']   = self.get_interactions(data)
  complaintItem['deal_again']       = self.get_data(data, "props.pageProps.complaint.dealAgain")
  complaintItem['score']            = self.get_data(data, "props.pageProps.complaint.score")
  
  '''
  return ""
  

def get_html(url):
  html_content = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_content, "html.parser")
  return soup

def iosearch():
  
  global header, base_url
  
  count = 0
  #iosearch_url = [f"https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/{count}?company=98",

  while True :
    iosearch_url = f"https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/{count}?company=98&status=ANSWERED&evaluated=bool:false"
    
    request = urllib.request.Request(url=iosearch_url, headers=header) 
    page = urllib.request.urlopen(request).read()
    js_iosearch = json.loads(page)
    
    if not len(js_iosearch) : break
    count+=10
    if count == 100 : break
    
    for complaint in range(10):
      title = js_iosearch['complainResult']['complains']['data'][complaint]['title']
      id    = js_iosearch['complainResult']['complains']['data'][complaint]['id']

      title = unicodedata.normalize("NFD", title)
      title = re.sub("[\u0300-\u036f]", "", title)  
      title = re.sub(r'[^a-zA-Z0-9]+', ' ', title)
      title = title.replace(" ","-")

      link = base_url + title + "_"+ id
      print(link)
    #break
    #content = get_html(link)
    #complaint = get_complaint(content)
    #print(complaint)
  


if __name__ == "__main__":
  
  res = iosearch()
 
  with open('data/complaints.json', 'w', encoding='latin-1') as f:
    json.dump(res, f, indent=8, ensure_ascii=False)
    #print("Created Json File")