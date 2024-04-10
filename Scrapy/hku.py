import scrapy


class HkuSpider(scrapy.Spider):
    name = "hku"
    allowed_domains = ["www.hku.hk"]
    start_urls = ["https://www.hku.hk/"]

    def parse(self, response):
        pass
