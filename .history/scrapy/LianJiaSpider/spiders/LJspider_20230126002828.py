import scrapy
import re


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

        price_box = response.xpath('//div[@class="overview"]/div[@class="content"]//div[@class="price "]')
        totalPrice = price_box.xpath('./span[@class="total"]/text()').get()
        unitPrice = price_box.xpath('.//span[@class="unitPriceValue"]/text()').get()

        house_info = response.xpath('//div[@class="m-content"]//div[@class="introContent"]')
        base_info = house_info.xpath('./div[@class="base"]//li')
        layout = base_info.xpath('./span[text()="房屋户型"]/following-sibling::text()').get()
        floor = base_info.xpath('./span[text()="所在楼层"]/following-sibling::text()').get()
        area = base_info.xpath('./span[text()="建筑面积"]/following-sibling::text()').get()
        type = base_info.xpath('./span[text()="户型结构"]/following-sibling::text()').get()
        building = base_info.xpath('./span[text()="建筑类型"]/following-sibling::text()').get()
        direction = base_info.xpath('./span[text()="房屋朝向"]/following-sibling::text()').get()
        structure = base_info.xpath('./span[text()="建筑结构"]/following-sibling::text()').get()
        decoration = base_info.xpath('./span[text()="装修情况"]/following-sibling::text()').get()
        stairway = base_info.xpath('./span[text()="梯户比例"]/following-sibling::text()').get()
        stairway = base_info.xpath('./span[text()="梯户比例"]/following-sibling::text()').get()
        heating = base_info.xpath('./span[text()="供暖方式"]/following-sibling::text()').get()
        elevator = base_info.xpath('./span[text()="配备电梯"]/following-sibling::text()').get()

        
        area = float(re.search(r'(\.|\d)+',area).group(0))
        pass

