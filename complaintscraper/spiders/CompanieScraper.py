'''
This spider file contains the spider logic and scraping code to get companies registered on www.reclameaqui.com.br
scrapy crawl CompanieScraper --set FEED_EXPORT_ENCODING=utf-8 -o complaintscraper/data/companies.json
'''

import scrapy
from scrapy.spiders import CrawlSpider

from complaintscraper.items.CompanieItem import CompanieItem

import json
import ast

class CompanieScraper(CrawlSpider):

  name = "CompanieScraper"
  custom_settings = {
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS': 10,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
    'DOWNLOAD_DELAY': 1
  }
 
  def start_requests(self):
    categories = self.get_categories()
    for category in categories:
      categoryId = category['id']
      categoryName = category['name']
      url = f'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/banco/10/100?category={categoryId}'
      yield scrapy.Request(url, callback = self.parse_companie,  cb_kwargs=dict(categoryName=categoryName) )
  
  def parse_companie(self, response, categoryName):
    
    companieItem = CompanieItem()

    data = json.loads(response.text)
    companies = data['complainResult']['complains']['companies']
    
    for companie in companies:
      
      companieItem['id']   = companie['id']
      companieItem['companyName'] = companie['name']
      companieItem['companyShortname'] = companie['companyShortname']
      companieItem['categoryName'] = categoryName
      
      yield companieItem

  def get_categories(self):
    categories = []
    with open('complaintscraper/data/categories.json') as file:
      categories = ast.literal_eval(file.read())
    return categories

    
