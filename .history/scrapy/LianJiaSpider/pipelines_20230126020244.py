from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import CloseSpider

class LianjiaspiderPipeline:
    def __init__(self):
        self.fp = open('data.csv', 'w', encoding="utf-8")
        self.exporter = CsvItemExporter(self.fp)

    def process_item(self, item, spider):
        for key,val in item.items():
            if val == '暂无数据':
                item[key] = None
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        if spider.maxPage == -1:
            raise CloseSpider('\n' + '*' * 20 + f'\nIP Get Banned!\tError page: {spider.page}\n' + '*' * 20 + '\n')
        print('success!')
        pass
