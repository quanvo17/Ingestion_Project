import scrapy
from Crawler.matching import *


class TrueSmart(scrapy.Spider):
    name = 'macbook_TrueSmart'
    allowed_domains = ['truesmart.com.vn']
    start_urls = ['https://www.truesmart.com.vn/macbook.html']
    handle_httpstatus_list = [301]
    lst_page = ['/macbook.html']
    lst_url = []
    def parse(self, response):
        for page_url in response.css('.pul > li > .t > a::attr(href)').extract():
            if page_url not in self.lst_url:
                self.lst_url.append(page_url)
                yield scrapy.Request(response.urljoin(page_url), callback=self.parse_macbook, cb_kwargs={'url': page_url})

        next_pages = response.css('.lpg >a::attr(href)').extract()
        for next_page in next_pages:
            if next_page and next_pages not in self.lst_page:
                self.lst_page.append(next_page)
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_macbook(self, response, url):
        item = dict()
        iname = response.css('.upt > .l > h1::text').extract_first()
        if not iname:
            iname = response.css('.upt > .l > h1::text').extract_first()
        item['name'] = iname
        price = response.css('.d0 > .l>b::text ').extract_first()
        if price:
            item['price_sale'] = price.strip()[:-1]

        lst_params = response.css('.cp1 > table >tbody >tr')

        for params in lst_params:
            if len(params.css('td')) > 1:
                try:
                    params_name = params.css('td > span ::text').extract_first().strip()
                    params_value = params.css('td::text').extract_first()
                    item[params_name] = params_value
                except:
                    pass

        item['url'] = url
        item['website'] = self.allowed_domains[0]

        yield convert(item)
