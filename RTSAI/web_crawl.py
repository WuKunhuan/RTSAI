import shutil, os, subprocess
from RTSAI.config import DATA_PATH

debug = 1

def construct_crawl_knowledge_graphs(crawl_files, knowledge_graph_name): 
    '''
    Construct the specified knowledge graph with crawl_files provided. 
    '''

    # knowledge_graph_path = os.path.join(DATA_PATH, "Knowledge_graphs", knowledge_graph_name)
    from RTSAI.knowledge_graph import create_knowledge_graph
    create_knowledge_graph(knowledge_graph_name)

    '''
    Retrieve information from each crawl .html files (in the future, more file types will be supported; 
    including web resources like images). They will be stored locally inside data/scrapy_spiders/<knowledge_graph_name> folder
    '''

def crawl_URL(URL, spider_name):
    '''
    Automatically create a scrapy spider with name spider_name to crawl the URL. 
    Return an array containing the path to the response HTML content files
    '''
    spider_directory = os.path.join(DATA_PATH, "scrapy_spiders", spider_name)
    spider_file_name = os.path.join(spider_directory, "scraper.py")
    try: shutil.rmtree(spider_directory)
    except: pass
    
    os.makedirs(spider_directory)
    spider_file = open(spider_file_name, 'w')  # spider_directory
    spider_file.write(f'''
import scrapy, os
                      
web_crawl_ID_counter = 0
def web_crawl_ID(): 
    global web_crawl_ID_counter; web_crawl_ID_counter += 1
    return web_crawl_ID_counter

class {spider_name}_Spider(scrapy.Spider):
    name = '{spider_name}'
    start_urls = ['{URL}']

    def parse(self, response):
        if response.status == 200: 
            with open(os.path.join("{spider_directory}", f"response_{{web_crawl_ID()}}.html"), 'w', encoding='utf-8') as response_file:
                response_file.write(response.text)
        else: 
            with open(os.path.join("{spider_directory}", "html_status_code.txt"), 'r+') as html_status_file: 
                html_status_file.write(str(response.status))
            self.log(f"Request to {{response.url}} failed with status code {{response.status}}")

        # TO BE COMPLETED
        # Further define the web crawl structure to regularize the crawl results
        # Automatically forward to the next URL with some criteria
        # next = SOME URL
        # url = response.urljoin(next)
        # yield scrapy.Request(url=url, callback=self.parse)

''')
    spider_file.close()
    process = subprocess.Popen(['scrapy', 'runspider', spider_file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    '''
    Create the knowledge graphs when the web crawl is successful
    '''
    response_files = []
    if (debug == 1): print (f"Resulting web crawl files: {os.listdir(spider_directory)}")
    for filename in os.listdir(spider_directory):
        if filename.startswith("response_") and filename.endswith(".html"):
            response_files.append(os.path.join(spider_directory, filename))
    if (response_files): 
        construct_crawl_knowledge_graphs(response_files, spider_name)
        return (response_files)
    else: # web crawl failed
        if (os.path.exists(os.path.join(spider_directory, "html_status_code.txt"))): 
            with open(os.path.join(spider_directory, "html_status_code.txt")) as status_file: 
                status_code = int(status_file.readline())
                return (f"HTML status code: {status_code}")
        else: return (f"The site can't be reached. ")

