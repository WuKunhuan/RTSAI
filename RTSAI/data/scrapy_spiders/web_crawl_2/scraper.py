
import scrapy, os
                      
web_crawl_ID_counter = 0
def web_crawl_ID(): 
    global web_crawl_ID_counter; web_crawl_ID_counter += 1
    return web_crawl_ID_counter

class web_crawl_2_Spider(scrapy.Spider):
    name = 'web_crawl_2'
    start_urls = ['https://wukunhuan.github.io/Web_Crawl_Tests/hku_vision_mission.html']

    def parse(self, response):
        if response.status == 200: 
            with open(os.path.join("/Users/abc/Desktop/[HOLD]/RTSAI/RTSAI/data/scrapy_spiders/web_crawl_2", f"response_{web_crawl_ID()}.html"), 'w', encoding='utf-8') as response_file:
                response_file.write(response.text)
        else: 
            with open(os.path.join("/Users/abc/Desktop/[HOLD]/RTSAI/RTSAI/data/scrapy_spiders/web_crawl_2", "html_status_code.txt"), 'r+') as html_status_file: 
                html_status_file.write(str(response.status))
            self.log(f"Request to {response.url} failed with status code {response.status}")

        # TO BE COMPLETED
        # Further define the web crawl structure to regularize the crawl results
        # Automatically forward to the next URL with some criteria
        # next = SOME URL
        # url = response.urljoin(next)
        # yield scrapy.Request(url=url, callback=self.parse)

