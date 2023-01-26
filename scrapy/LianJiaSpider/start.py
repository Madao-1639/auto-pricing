from scrapy import cmdline
import os
dirpath=os.path.dirname(os.path.abspath(__file__))
os.chdir(dirpath)
cmdline.execute('scrapy crawl LJspider'.split())
