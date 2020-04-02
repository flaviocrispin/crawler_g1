import scrapy
import string
import random
import time

from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.http import Request

from selenium import webdriver

class GloboSpider(CrawlSpider):
    name = "GloboSpider"
    start_urls = []
    extractClass = ""
    qtdPages = 2

    rules = (

    )

    def __init__(self,extractClass=None,numpages=2):
        CrawlSpider.__init__(self)
        self.driver = webdriver.Firefox()
        self.extractClass = extractClass
        self.qtdPages = numpages

        if extractClass:
            build_url = 'http://g1.globo.com/%s/noticia/plantao.html' % (extractClass)
            self.start_urls = [build_url]                 

    def __del__(self):
        CrawlSpider.__del__(self)

    def parse(self, response):  	

        for page in xrange(1,int(self.qtdPages)):
    	    self.driver.get(response.url + '#' + str(page))
    	    time.sleep(3)
    	    print ('[DEBUG] Parsing Page ' + response.url + '#' + str(page))

        links_noticias = self.driver.find_elements_by_xpath("//div/h3/a")

        for link in links_noticias:
            yield scrapy.Request(link.get_attribute("href"), self.parseNews)

    def parseNews(self, response):        
        content = ""

        newsTexts = response.xpath("//div[@id='materia-letra']//div/p/text()").extract()

        for text in newsTexts:
            content += text

        contentBeauty = BeautifulSoup(content).get_text().strip()
        fileName = ''.join(random.sample(string.letters, 15))

        with open(self.extractClass + '/' + fileName, 'wb') as f:
            f.write(contentBeauty.encode('utf8'))