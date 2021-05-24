import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class watch_nguyenkim(scrapy.Spider):
    name = 'watch_nguyenkim'
    start_urls = ["https://www.nguyenkim.com/dong-ho-thong-minh-apple/"]
    script_await = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(5))
                    return {
                        html = splash:html(),
                        url = splash:url(),
                    }
                end
                """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script_await}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}
        items = response.xpath('//*[@id="pagination_contents"]').css('div.item')
        thongtin = dict()
        for item in items:
            thongtin['name'] = item.css('div.product-title a::text').get()
            thongtin['price'] = str(item.css('p.final-price::text').get()).replace('đ', ' VND')
            link = item.css('div.product-title').css('a').attrib['href']
            thongtin['link'] = link
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('table', class_='productSpecification_table').find_all('tr')
            for information in informations:
                title = information.find('td', class_='title').text
                value = information.find('td', class_='value').text
                thongtin[title] = value

            yield convert(thongtin)
