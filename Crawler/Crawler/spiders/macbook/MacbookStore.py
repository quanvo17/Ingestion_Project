import scrapy
from Crawler.matching import *

class MacbookStore(scrapy.Spider):
    name = 'MacbookStore'
    allowed_domains = ['macstores.vn']
    start_urls = ['https://macstores.vn/macbook-pro/']
    handle_httpstatus_list = [301]
    list_url = []

    def check_valid_product(self,url):
        if url in self.list_url:
            return False
        else:
            self.list_url.append(url)
            return True

    def parse(self, response):
        for page_url in response.css('.wpb_wrapper > div > div > p > a ::attr(href)').extract():
            if('macbook' in page_url):
                yield scrapy.Request(response.urljoin(page_url), callback=self.parse_page)

    def parse_page(self, response):
        for item_url in response.css('ul .product > div > div > a::attr(href)').extract():
            if(self.check_valid_product(item_url) == True):
                yield scrapy.Request(response.urljoin(item_url), callback=self.parse_macbook, cb_kwargs={'url': item_url})

    def parse_macbook(self, response, url):
        item = dict()
        item['product_name'] = response.css('div.product-title > h1::text').extract_first()

        item['price_sale'] = response.css('p.price > span ::text').extract_first()

        lst_params = response.css('.product-description')[0].css('li ::text').extract()
        pi = 1
        for params in lst_params:
            if 'cpu' in params.lower():
                item['cpu'] = params
            elif 'gpu' in params.lower() or "graphics" in params.lower() or 'vga' in params.lower():
                item['gpu'] = params            
            elif 'storage' in params.lower() or 'sdd' in params.lower() or 'hdd' in params.lower():
                item['rom'] = params
            elif 'ram' in params.lower() or 'ddr' in params.lower():
                item['ram'] = params
            elif 'inch' in params.lower() or 'display' in params.lower() or 'retina' in params.lower():
                item['display'] = params
            else:
                item['params_' + str(pi)] = params
                pi +=1

        item['url'] = url
        item['website'] = self.allowed_domains[0]
        
        yield convert(item)

