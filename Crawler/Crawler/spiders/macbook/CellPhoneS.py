import scrapy
from scrapy import item
from Crawler.matching import *

class MacbookCellphonesSpider(scrapy.Spider):
    name = 'macbook_cellphoneS'
    allowed_domains = ['cellphones.com.vn']
    start_urls = ['https://cellphones.com.vn/laptop/mac.html',
                  'https://cellphones.com.vn/laptop/mac.html?p=2']
    handle_httpstatus_list = [301]

    def parse(self, response):
        for product in response.css(".list-laptop > ul > li"):
            item_url = product.css(
                ".lt-product-group-info > a ::attr(href)").extract_first()
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_macbook, cb_kwargs={'url': item_url})

    def parse_macbook(self, response,url):
        item = dict()

        item['name'] = response.css(
            'div.topview > h1 ::text').extract_first()
        item['price_sale'] = response.css(
            'p.special-price > span::text').extract_first()
        item['price'] = response.css(
            'p.old-price > span::text').extract_first()
        lst_params = response.css('#tskt > tr')
        for params in lst_params:
            if len(params.css('td')) > 1:
                params_name = params.css('td::text').extract_first()
                if 'CPU' in params_name or 'cpu' in params_name:
                    params_name = 'cpu'              
                elif 'RAM' in params_name or 'ram' in params_name:
                    params_name = 'ram'  
                elif 'Ổ cứng' in params_name:
                    params_name = 'rom'                

                params_value = params.css('td::text').extract()[1]
                item[params_name] = params_value

        item['url'] = url
        item['website'] = self.allowed_domains[0]

        yield convert(item)
