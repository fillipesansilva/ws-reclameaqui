# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class CompanieItem(Item):
    
  id = Field()
  companyName = Field()
  categoryName = Field()
  companyShortname = Field()
  
