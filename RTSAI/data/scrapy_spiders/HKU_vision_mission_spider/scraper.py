
import scrapy, os

class HKU_vision_mission_spider_Spider(scrapy.Spider):
    name = 'HKU_vision_mission_spider'
    start_urls = ['https://wukunhuan.github.io/Web_Crawl_Tests/hku_vision_mission.html']

    def parse(self, response):
        # html_content = response.body.decode('utf-8')
        print (os.path.join("/Users/abc/Desktop/RTSAI/RTSAI/data/scrapy_spiders/HKU_vision_mission_spider", "response.html"))
        with open(os.path.join("/Users/abc/Desktop/RTSAI/RTSAI/data/scrapy_spiders/HKU_vision_mission_spider", "response.html"), 'w', encoding='utf-8') as response_file: 
            response_file.write(response.text)
            response_file.close()
        # yield html_content
