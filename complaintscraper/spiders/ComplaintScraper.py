'''
This spider file contains the spider logic and scraping code. 
In order to determine what needs to go in this file, we have to inspect the website!
'''

import scrapy
from scrapy.spiders import CrawlSpider

from complaintscraper.items.ComplaintItem import ComplaintItem
from complaintscraper.utils.DataCleaning import DataCleaning

import json
import pydash

class ComplaintScraper(CrawlSpider):

  name = "ComplaintScraper"  
  custom_settings = {
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS': 10,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
    'DOWNLOAD_DELAY': 1
  }
  
  start_urls = [
    "https://www.reclameaqui.com.br/empresa/santander/lista-reclamacoes/?pagina=1"
  ]

  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(url, self.parse_page)

  def parse_page(self, response):
    number_of_pages = int(response.xpath('//*[@id="__next"]/div[1]/div/div[3]/main/section[2]/div[2]/div[2]/div[11]/ul/li[8]/text()').extract()[0])
    for page in range(1, number_of_pages + 1, 1):
      url =  "https://www.reclameaqui.com.br/empresa/santander/lista-reclamacoes/?pagina=" + str(page)
      yield scrapy.Request(url, callback=self.parse_complaint, dont_filter=True)

  def parse_complaint(self, response):
    for row in response.xpath('//div[contains(@class,"bJdtis")]'):
      link = row.xpath("./a/@href").get()
      yield scrapy.Request(response.urljoin(link), callback=self.parse_model_complaint, dont_filter=True)

  def get_data(self, data, query):
    return pydash.get(data, query, None)

  def parse_model_complaint(self, response):

    dataCleaning = DataCleaning()
    complaintItem = ComplaintItem()

    data = json.loads(response.xpath('//*[@id="__NEXT_DATA__"]//text()').extract()[0])
    
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
    
    complaintItem['company_answer']   = self.get_data(data, "props.pageProps.complaint.interactions.0.message")
    complaintItem['consumer_replica'] = self.get_data(data, "props.pageProps.complaint.interactions.1.message")
    complaintItem['final_answer']     = self.get_data(data, "props.pageProps.complaint.interactions.2.message")
    complaintItem['deal_again']       = self.get_data(data, "props.pageProps.complaint.dealAgain")
    complaintItem['score']            = self.get_data(data, "props.pageProps.complaint.score")
      
    data_processed = dataCleaning(complaintItem)
    yield data_processed
