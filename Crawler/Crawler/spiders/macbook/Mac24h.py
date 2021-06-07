import scrapy
from Crawler.matching import *

class Macbook24h(scrapy.Spider):
    name = 'mac24h'
    allowed_domains = ['mac24h.vn']
    start_urls = ['https://mac24h.vn/mac/']
    handle_httpstatus_list = [301]

    def parse(self, response):
        for page_url in response.css('div.ty-grid-list__image > a ::attr(href)').extract():
            if('macbook' in page_url):
                yield scrapy.Request(response.urljoin(page_url), callback=self.parse_macbook, cb_kwargs={'url': page_url})

        next_page = response.css('.ty-pagination__next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_macbook(self,response, url):
        item = dict()
        item['name'] = response.css('.ty-product-block-title::text').extract_first()
        item['price_sale'] = response.css('.ty-product-prices > div > span > span.ty-price ::text').extract_first()
        r_price = response.css('.ty-product-prices > div > span >span >span ::text').extract_first()
        if r_price:
            item['price'] = r_price
        item['shipping'] = response.css('span.shipping-fee ::text').extract_first()

        lst_params =response.css('.ty-product-block__description > div > ul > li::text ').extract()
        pi = 1
        
        for params in lst_params:
            if 'cpu' in params.lower() or 'processor' in params.lower() or 'intel' in params.lower():
                item['cpu'] = params
            elif 'gpu' in params.lower() or "graphics" in params.lower() or 'vga' in params.lower():
                item['gpu'] = params
            elif 'storage' in params.lower() or 'sdd' in params.lower() or 'hdd' in params.lower():
                item['rom'] = params
            elif 'ram' in params.lower() or 'ddr' in params.lower() or 'memory' in params.lower():
                item['ram'] = params
            elif 'inch' in params.lower() or 'display' in params.lower() or 'retina' in params.lower():
                item['display'] = params
            else:
                item['params_' + str(pi)] = params
                pi += 1

        item['url'] = url
        item['website'] = self.allowed_domains[0]

        yield convert(item)
