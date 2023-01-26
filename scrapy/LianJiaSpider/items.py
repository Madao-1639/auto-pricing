import scrapy

class LianjiaspiderItem(scrapy.Item):
    _id = scrapy.Field()
    totalPrice = scrapy.Field()
    unitPrice = scrapy.Field()
    region = scrapy.Field()
    garden = scrapy.Field()
    layout = scrapy.Field()
    floor = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    building = scrapy.Field()
    direction = scrapy.Field()
    structure = scrapy.Field()
    renovation = scrapy.Field()
    stairway = scrapy.Field()
    heating = scrapy.Field()
    elevator = scrapy.Field()
    usage = scrapy.Field()
    year = scrapy.Field()

