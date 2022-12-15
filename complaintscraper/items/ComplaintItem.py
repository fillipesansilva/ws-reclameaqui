# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ComplaintItem(Item):
    
    id               = Field()
    title            = Field()
    description      = Field()
    tags             = Field() #(Problemas Gerais, Mau atendimento do prestador de serviço, ...)
    url              = Field()
    userCity         = Field()
    userState        = Field()
    creation_date    = Field()
    status           = Field()
    solved           = Field() #Não respondida/respondida/resolvido
    deal_again       = Field() #Sim / Não
    score            = Field() #Nota do atendimento
    interactions     = Field() #contain customer and company replicas.
    categoryName     = Field() 