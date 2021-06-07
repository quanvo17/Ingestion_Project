import scrapy
from Crawler.matching import *

class MacOne(scrapy.Spider):
    name = 'macone'
    allowed_domains = ['macone.vn']
    start_urls = ['https://macone.vn/macbook-cu-moi/']
    handle_httpstatus_list = [301]

    def parse(self, response):
        for page_url in response.css('.product_inner> div > div > .item-product > .image-box > a::attr(href)').extract():
            if('macbook' in page_url):
                yield scrapy.Request(response.urljoin(page_url), callback=self.parse_macbook, cb_kwargs={'url': page_url})

        next_page = response.css('.nextpostslink::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_macbook(self, response, url):
        item = dict()
        iname = response.css('.product-title ::text').extract_first()
        if not iname:
            iname = response.css('.produce-info >h1 ::text').extract()
        item['name'] = iname
        price = response.css('.produce-info > .price-box > div > strong::text').extract_first()
        if price:
            item['price_sale'] = price.strip()[:-1]
        
        lst_params = response.css('.table-responsive > table > tbody > tr')

        for params in lst_params:
            if len(params.css('td')) > 1:
                params_name = params.css('td > strong ::text').extract_first().strip()
                params_value = params.css('td::text').extract_first()
                if 'CPU' in params_name or 'cpu' in params_name:
                    params_name= 'cpu'
                elif 'RAM' in params_name or 'ram' in params_name:
                    params_name = 'ram'
                elif 'Ổ cứng' in params_name:
                    params_name = 'rom'
                item[params_name] = params_value

        item['url'] = url
        item['website'] = self.allowed_domains[0]

        yield convert(item)
