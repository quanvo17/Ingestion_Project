import scrapy
from scrapy.http import request
import requests
from Crawler.matching import *

class Macbook24h(scrapy.Spider):
    name = 'hanoicom'
    allowed_domains = ['www.hanoicomputer.vn']
    start_urls = ['https://www.hanoicomputer.vn/laptop-apple']
    handle_httpstatus_list = [301]
    page = 1
    lst_url = []
    def parse(self, response):
        for page_url in response.css('.cate-list-prod> div> .p-info> h3 > a::attr(href)').extract():
            if (page_url not in self.lst_url):
                self.lst_url.append(page_url)
                yield scrapy.Request(response.urljoin(page_url), callback=self.parse_macbook, cb_kwargs={'url': page_url})
        
        self.page +=1
        p_count = len(response.css('.paging')[0].css('a::attr(href)'))
        if self.page <= p_count: 
            next_page = self.start_urls[0] + '/' + str(self.page) + '/'
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_macbook(self, response, url):
        item = dict()

        item['name'] =  response.css('.product_detail-title > h1 ::text').extract_first()
        item['price_sale'] = response.css('#product-info-price >.giakm::text').extract_first().strip()[:-1]
        r_price = response.css('#product-info-price >.giany::text').extract_first()
        if r_price:
            item['price'] = r_price.strip()[:-1]
        lst_params =  response.css('#popup-tskt > .content-popup > div > table > tbody > tr')
        pid = 1
        for params in lst_params:
            if len(params.css('td > p::text')) > 1:
                params_name = params.css('td > p::text')[0].extract()
                params_value = params.css('td> p::text')[1].extract()

                if('vi xử lý' in params_name):
                    params_name = 'cpu'
                elif ('Bộ nhớ trong' in params_name):
                    params_name = 'ram'
                elif 'Ổ cứng' in params_name:
                    params_name = 'rom'
            else:
                params_name = "err_" + str(pid)
                params_value = 'error_value'
            item[params_name] = params_value

        item['url'] = "https://www.hanoicomputer.vn/" +url
        item['website'] = self.allowed_domains[0]
        item['tssss'] = len(self.lst_url)

        yield convert(item)
