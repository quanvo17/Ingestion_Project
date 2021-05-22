import scrapy
from Crawler.matching import *


class Cellphones(scrapy.Spider):
    name = 'macbook_CellPhoneS'
    allowed_domains = ['cellphones.com.vn']
    start_urls = ['https://cellphones.com.vn/laptop/mac.html',
                  'https://cellphones.com.vn/laptop/mac.html?p=2']
    handle_httpstatus_list = [301]


    def parse(self, response):
        # Request tới từng sản phẩm có trong danh sách các Macbook dựa vào href
        for product in response.css(".list-laptop > ul > li"):
            if(len(product.css(".lt-product-group-cau-hinh > table > tr > td"))):
                cpu = product.css(".lt-product-group-cau-hinh > table > tr > td ")[1].css("::text").extract_first()
                vga = product.css(".lt-product-group-cau-hinh > table > tr > td ")[3].css("::text").extract_first()
                dr = product.css(".lt-product-group-cau-hinh > table > tr > td ")[5].css("::text").extract_first()
            else:
                cpu = ""
                vga = ""
                dr = ""
            item_url = product.css(".lt-product-group-info > a ::attr(href)").extract_first()
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_macbook, cb_kwargs={'cpu': cpu, 'vga': vga, 'dr': dr, "url":item_url})

    def parse_macbook(self, response, cpu,vga, dr, url):
        yield convert({
            'name': response.css(
                'div.topview > h1 ::text').extract_first(),
            'price_sale': response.css(
                'p.special-price > span::text').extract_first(),
            'price': response.css(
                'p.old-price > span::text').extract_first(),
            'rate': response.css(
                'p.averageRatings::text').extract_first(),
            'cpu': cpu,
            'gpu': vga,
            'storage': dr,
            'url' : url,
            'website': self.allowed_domains[0]
        })
