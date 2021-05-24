import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
import pandas as pd
from Crawler.matching import *


class uBuy(scrapy.Spider):
    name = 'ipad_ubuy'
    start_urls = ["https://imagineonline.store/t/category/watch"]

    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next_page page-item")[0].click();'))
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
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.xpath('//*[@id="content"]/div/div[4]/div[1]/div/div/div/div[1]').css('div.overflow-hidden')
        for item in items:
            thongtin = dict()
            thongtin['name'] = str(item.css('h5::text').get())
            thongtin['price'] = str(item.css('div.flex-grow-1 span::text').get())

            yield convert(thongtin)

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )
