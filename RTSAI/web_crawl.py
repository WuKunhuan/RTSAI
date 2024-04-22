import shutil, os, subprocess
from RTSAI.config import DATA_PATH

def crawl_URL(URL, spider_name):
    '''
    Automatically create a scrapy spider with name spider_name to crawl the URL
    Return an array containing the number of items scraped, HTTP status codes,
    and the response HTML content
    '''
    spider_directory = os.path.join(DATA_PATH, "scrapy_spiders", spider_name)
    spider_file_name = os.path.join(spider_directory, "scraper.py")
    try: shutil.rmtree(spider_directory)
    except: pass
    
    os.makedirs(spider_directory)
    spider_file = open(spider_file_name, 'w')  # spider_directory
    spider_file.write(f'''
import scrapy, os

class {spider_name}_Spider(scrapy.Spider):
    name = '{spider_name}'
    start_urls = ['{URL}']

    def parse(self, response):
        # html_content = response.body.decode('utf-8')
        print (os.path.join("{spider_directory}", "response.html"))
        with open(os.path.join("{spider_directory}", "response.html"), 'w', encoding='utf-8') as response_file: 
            response_file.write(response.text)
            response_file.close()
        # yield html_content
''')
    spider_file.close()
    process = subprocess.Popen(['scrapy', 'runspider', spider_file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)



