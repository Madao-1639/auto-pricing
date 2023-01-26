import scrapy


class LjspiderSpider(scrapy.Spider):
    name = 'LJspider'
    allowed_domains = ['xa.lianjia.com']
    start_urls = ['http://xa.lianjia.com/']

    def parse(self, response):
        pass
