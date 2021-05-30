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
        items = response.xpath('//*[@id="categoryPage"]/div[3]/ul').css('li.item')
        for item in items:
            thongtin = dict()
            thongtin['name'] = str(item.css('h3::text').get()).replace('\n', '').replace('\t', '').replace('\r', '')
            thongtin['prict'] = item.css('strong.price::text').get()
            thongtin['screen'] = str(item.css('div.utility').css('p::text')[0].get()).split(',')[0]
            thongtin['CPU']  = str(item.css('div.utility').css('p::text')[0].get()).split(',')[1]

            thongtin['RAM'] = str(item.css('div.utility').css('p::text')[1].get()).split(',')[0]
            thongtin['ROM'] = str(item.css('div.utility').css('p::text')[1].get()).split(',')[1]

            thongtin['camera sau'] = str(item.css('div.utility').css('p::text')[2].get())
            thongtin['camera sau'] = str(item.css('div.utility').css('p::text')[3].get())
            thongtin['pin'] = str(item.css('div.utility').css('p::text')[4].get())


            yield convert(thongtin)
