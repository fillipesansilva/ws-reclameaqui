'''
This spider file contains the spider logic and scraping code to get (almost) all categories registered on www.reclameaqui.com.br
To run: scrapy crawl CategoryScraper --set FEED_EXPORT_ENCODING=utf-8 -o complaintscraper/data/categories.json
'''

import scrapy
from scrapy.spiders import CrawlSpider

from complaintscraper.items.CategoryItem import CategoryItem

import json

class CategoryScraper(CrawlSpider):
  
  name = "CategoryScraper"
  custom_settings = {
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS': 10,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
    'DOWNLOAD_DELAY': 1
  }

  start_urls = [
    "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/Bancos/10/0",
    "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/Informática/10/0"
    "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/Eletrodoméstico/10/0"
  ]
  
  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(url, callback = self.get_categories)

    
  def get_categories(self, response):
    data = json.loads(response.text)
    categories = data['complainResult']['complains']['categories']
    
    for category in categories:
      
      categoryItem = CategoryItem()
      
      categoryItem['id']   = category['id']
      categoryItem['name'] = category['name']

      yield  categoryItem
    