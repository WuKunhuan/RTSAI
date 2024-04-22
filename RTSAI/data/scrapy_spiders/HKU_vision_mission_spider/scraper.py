
import scrapy, os
                      
web_crawl_ID_counter = 0
def web_crawl_ID(): 
    global web_crawl_ID_counter; web_crawl_ID_counter += 1
    return web_crawl_ID_counter

class HKU_vision_mission_spider_Spider(scrapy.Spider):
    name = 'HKU_vision_mission_spider'
    start_urls = ['https://wukunhuan.github.io/Web_Crawl_Tests/hku_vision_mission.html']

    def parse(self, response):
        # html_content = response.body.decode('utf-8')
        with open(os.path.join("/Users/abc/Desktop/RTSAI/RTSAI/data/scrapy_spiders/HKU_vision_mission_spider", f"response_{web_crawl_ID_counter}.html"), 'w', encoding='utf-8') as response_file: 
            response_file.write(response.text)
            response_file.close()
        # yield html_content

        # TO BE COMPLETED
        # Further define the web crawl structure to regularize the crawl results

        # next = SOME URL
        # url = response.urljoin(next)
        # yield scrapy.Request(url=url, callback = self.parse)

