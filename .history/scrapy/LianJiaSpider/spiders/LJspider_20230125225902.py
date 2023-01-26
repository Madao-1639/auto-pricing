import scrapy


class LjspiderSpider(scrapy.Spider):
    name = 'LJspider'
    allowed_domains = ['xa.lianjia.com']
    start_urls = ['https://xa.lianjia.com/ershoufang/pg1co32/']
    BASE_url = 'https://xa.lianjia.com/'
    maxPage = 100

    def parse(self, response):
        inner_urls = response.xpath(\
            '//ul[@class="sellListContent"]//div[@class="info clear"]/div[@class="title"]/a/@href').getall()
        for url in inner_urls:
            yield scrapy.Request(url = url, callback = self.infoparse)
        
        self.page = int(response.url[36:-5])
        if self.page < self.maxPage:
            next_page = self.page + 1
            next_url = response.url[:36] + str(next_page) + response.url[-5:]
            yield scrapy.Request(url = next_url, callback = self.parse)

    #def infoparse(self, response):

