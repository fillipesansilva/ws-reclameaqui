'''
This spider file contains the spider logic and scraping code to get all customer complaints. 
scrapy crawl ComplaintScraper --set FEED_EXPORT_ENCODING=utf-8 -o complaintscraper/data/complaints.json
'''

import scrapy
from scrapy.spiders import CrawlSpider

from complaintscraper.items.ComplaintItem import ComplaintItem
from complaintscraper.utils.DataCleaning import DataCleaning

import json
import pydash
import ast
import unicodedata
import re

class ComplaintScraper(CrawlSpider):
  
  name = "ComplaintScraper"  
  custom_settings = {
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS': 10,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
    'DOWNLOAD_DELAY': 1
  }
  
  def start_requests(self):
    companies = self.get_companies()
    for company in companies:
      id = company['id']
      categoryName = company['categoryName']
      companyShortname = company['companyShortname']
      for page in range(0, 1010, 10):
        base = f'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/{page}?company={id}'
        yield scrapy.Request(base, callback = self.parse_complaints, cb_kwargs=dict(companyShortname=companyShortname, categoryName = categoryName)) 
      break

  def get_companies(self):
    companies = []
    with open('complaintscraper/data/companies.json', encoding='utf8') as file:
      companies = ast.literal_eval(file.read())
      
    # Removing duplicate entries (companies)
    rsl = []
    ids = []
    for company in companies:
      if company['id'] in ids: continue
      ids.append(company['id'])
      rsl.append(company) 

    return rsl
      
  def parse_complaints(self, response, companyShortname, categoryName):
    data = json.loads(response.text)
    for complaint in range(10):
      title = data['complainResult']['complains']['data'][complaint]['title']
      id    = data['complainResult']['complains']['data'][complaint]['id']

      title = unicodedata.normalize("NFD", title)
      title = re.sub("[\u0300-\u036f]", "", title)  
      title = re.sub(r'[^a-zA-Z0-9]+', ' ', title)
      title = title.replace(" ","-")

      link = f"https://www.reclameaqui.com.br/{companyShortname}/" + title + "_"+ id
      
      yield scrapy.Request(link, callback=self.parse_model_complaint, dont_filter=True, cb_kwargs=dict(categoryName = categoryName))

  def get_data(self, data, query):
    return pydash.get(data, query, None)

  def get_interactions(self, data):
    rsl = []
    i = 0
    query = "props.pageProps.complaint.interactions." + str(i) + ".message"
    interaction = self.get_data(data, query)
    while interaction:
      rsl.append(interaction)
      i += 1
      query = "props.pageProps.complaint.interactions." + str(i) + ".message"
      interaction = self.get_data(data, query)
    return rsl

  def parse_model_complaint(self, response, categoryName):
    dataCleaning = DataCleaning()
    complaintItem = ComplaintItem()

    data = json.loads(response.xpath('//*[@id="__NEXT_DATA__"]//text()').extract()[0])
    
    complaintItem['categoryName']     = categoryName
    complaintItem['id']               = self.get_data(data, "props.pageProps.complaint.legacyId")
    complaintItem['title']            = self.get_data(data, "props.pageProps.complaint.title")
    complaintItem['solved']           = self.get_data(data, "props.pageProps.complaint.solved")
    complaintItem['description']      = self.get_data(data, "props.pageProps.complaint.description")
    complaintItem['url']              = response.url

    content_container                 = response.xpath('//*[contains(@data-testid, "complaint-content-container")]//text()').extract()
    complaintItem['tags']             = content_container[content_container.index("ID:") + 2 : content_container.index("Status da reclamação:")]
    complaintItem['status']           = response.xpath('//*[contains(@data-testid, "complaint-status")]//text()').extract()
    
    complaintItem['userCity']         = self.get_data(data, "props.pageProps.complaint.userCity")
    complaintItem['userState']        = self.get_data(data, "props.pageProps.complaint.userState")
    complaintItem['creation_date']    = self.get_data(data, "props.pageProps.complaint.created")
    
    #Interactions contain customer and company replicas.
    complaintItem['interactions']   = self.get_interactions(data)
    complaintItem['deal_again']       = self.get_data(data, "props.pageProps.complaint.dealAgain")
    complaintItem['score']            = self.get_data(data, "props.pageProps.complaint.score")
      
    data_processed = dataCleaning(complaintItem)
    yield data_processed
