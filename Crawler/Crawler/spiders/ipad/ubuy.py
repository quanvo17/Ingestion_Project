import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
import pandas as pd
from Crawler.matching import *


class uBuy(scrapy.Spider):
    name = 'ipad_ubuy'
    start_urls = ["https://www.jbhifi.com.au/collections/computers-tablets/apple-ipads"]

    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('try{document.getElementsByClassName("ais-Pagination-link")[0].click();}catch(e){}'))
                assert(splash:wait(5))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """
    script1 = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(2))
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
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script1}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.xpath('//*[@id="collection-search-results"]/div/div').css('div.ais-hits--item')
        print(items)
        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )
