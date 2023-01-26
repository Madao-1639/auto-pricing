import scrapy


class LjspiderSpider(scrapy.Spider):
    name = 'LJspider'
    allowed_domains = ['xa.lianjia.com']
    start_urls = ['https://xa.lianjia.com/ershoufang/pg1co32/']
    BASE_url = 'https://xa.lianjia.com/'

    def parse(self, response):
        inner_urls=response.xpath(\
            '//ul[@class="sellListContent"]//div[@class="info clear"]/div[@class="title"]/a/@href').get
        pass

