import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class iphone_baotuyetmobile(scrapy.Spider):
    name = 'iphone_baotuyetmobile'
    start_urls = ["https://baotuyetmobile.vn/iphone-2-1-296039.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("pagination d-flex align-items-center justify-content-center")[0].getElementsByTagName("li")[6].getElementsByTagName("a")[0].click();'))
                assert(splash:wait(5))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """
    script_wait = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(1))
                    assert(splash:wait(3))
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
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script_wait}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        items = response.css('ul.v2_bnc_products_page_list li.col-xl-20')
        for item in items:
            thongtin = dict()
            thongtin['name'] = item.css('div.v2_bnc_pr_item_name > h3 >a::text').get()
            thongtin['price'] = str(item.css('p.v2_bnc_pr_item_price::text').get()).replace('đ', 'VND')
            link = thongtin['link'] = item.css('div.v2_bnc_pr_item_name > h3 >a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            try:
                informations = soup.find('div', class_='parameter-detail').find('ul').find_all('li')
            except:
                informations = []
            for information in informations:
                try:
                    label = information.find_all('span')[0].text
                    value = information.find_all('span')[1].text
                    thongtin[label] = value
                except:
                    continue
            yield convert(thongtin)

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )
