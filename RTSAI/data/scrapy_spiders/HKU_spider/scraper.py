
import scrapy, os

class HKU_spider_Spider(scrapy.Spider):
    name = 'HKU_spider'
    start_urls = ['https://www.hku.hk/']

    def parse(self, response):
        # html_content = response.body.decode('utf-8')
        print (os.path.join("/Users/abc/Desktop/RTSAI/RTSAI/data/scrapy_spiders/HKU_spider", "response.html"))
        with open(os.path.join("/Users/abc/Desktop/RTSAI/RTSAI/data/scrapy_spiders/HKU_spider", "response.html"), 'w', encoding='utf-8') as response_file: 
            response_file.write(response.text)
            response_file.close()
        # yield html_content
