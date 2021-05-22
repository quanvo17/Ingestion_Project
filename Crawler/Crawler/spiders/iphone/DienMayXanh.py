import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class DienMayXanh(scrapy.Spider):
    name = 'iphone_DienMayXanh'
    start_urls = ["https://www.dienmayxanh.com/dien-thoai-apple-iphone"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("loadmore")[0].click();'))
                assert(splash:wait(5))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.prdWrFixHe')
        print(len(items))
        for item in items:
            thongtins = item.css('div.prdTooltip')[0]
            yield convert({
                "Tên sản phẩm": item.css('div.prdName span::text').get(),
                "Giá sản phẩm": str(item.css('strong.prPrice::text').get()).replace('₫', ' VNĐ'),
                "Màn hình": str(thongtins.css('span::text')[0].get()).split(', ')[0].replace('"', ' inch'),
                "Chip": str(thongtins.css('span::text')[0].get()).split(', ')[1],
                'RAM': str(thongtins.css('span::text')[1].get()).split(', ')[0].replace('RAM ', ''),
                'Bộ nhớ trong': str(thongtins.css('span::text')[1].get()).split(', ')[1].replace('ROM ', ''),
                'Camera sau': str(thongtins.css('span::text')[2].get()).replace('Camera sau: ', ''),
                'Camera trước': str(thongtins.css('span::text')[3].get()).replace('Camera trước:  ', ''),
                'Pin': str(thongtins.css('span::text')[4].get()).split(', ')[0].replace('Pin ', ''),
                'Sạc': str(thongtins.css('span::text')[4].get()).split(', ')[1].replace('Sạc ', ''),
                'Loại sản phẩm': 'IPHONE',
                'Cửa hàng': 'DIEN MAY XANH'
            })