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

    def infoparse(self, response):
        id = response.url[34:-5]
        content = response.xpath('//div[@class="content"]')

        price_box = content.xpath('.//div[@class="price "]')
        totalPrice = price_box.xpath('./span[@class="total"]/text()').get()
        unitPrice = price_box.xpath('.//span[@class="unitPriceValue"]/text()').get()

        house_info = content.xpath('./div[@class="houseInfo"]')
        layout = house_info.xpath('./div[@class="room"]/div[@class="mainInfo"]/text()').get()
        floor = house_info.xpath('./div[@class="room"]/div[@class="subInfo"]/text()').get()
        direction = house_info.xpath('./div[@class="type"]/div[@class="mainInfo"]/text()').get()
        type = house_info.xpath('./div[@class="type"]/div[@class="subInfo"]/text()').get()
        area = house_info.xpath('./div[@class="area"]/div[@class="mainInfo"]/text()').get()
        building = house_info.xpath('./div[@class="area"]/div[@class="subInfo"]/text()').get()

        pass

