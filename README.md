
# WS-RECLAMEAQUI

ws-reclameaqui is a python tool developed to mine and clean customer complaints from www.reclameaqui.com.br. 

### Folders

- spiders: This folder contains all of our future Scrapy spider files that extract the data.
- items: This file contains item objects that behave like Python dictionaries and provide an abstraction layer to store scraped data within the Scrapy framework.
- middlewares (advanced): Scrapy middlewares are useful if you want to modify how Scrapy runs and makes requests to the server (e.g., to get around antibot solutions). For simple scraping projects, you don’t need to modify middlewares.
- pipelines: Scrapy pipelines are for extra data processing steps you want to implement after you extract data. You can clean, organize, or even drop data in these pipelines.
- settings: General settings for how Scrapy runs, for example, delays between requests, caching, file download settings, etc.

### How to run 

- pip3 install -r requirements.txt
- (into ws-reclameaqui folder) scrapy crawl ComplaintScraper --set FEED_EXPORT_ENCODING=utf-8 -o data/complaint.json

### Dataset
- Dataset will be create into data/complaint.json.

| Value | Description | 
| :---: | :---: | 
| id | Complaint id | 
| title | Complaint title | 
| description | Complaint description | 
| tags | Complaint tags | 
| url | Complaint url | 
| userCity | User city | 
| userState | User state | 
| creation_date | Date of complaint creation | 
| status | Complaint status (at the moment of scraping) | 
| solved | Complaint solved or not ('Yes' or 'No') | 
| company_answer | Company response | 
| deal_again | Would user do business with the company again? | 
| score | Service evaluation [0,10] | 
| consumer_replica | Consumer replica | 
| final_answer | Final user comment | 