import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class viettel_store(scrapy.Spider):
    name = 'viettel-store'
    start_urls = ["https://viettelstore.vn/tablet-apple-ipad"]
    script = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(1))
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

        items = response.css('div.col-xs-12 > div.wrap-pro-list').css('div.item')

        for item in items:
            thongtin = dict()
            thongtin['name'] = item.css('h2.name::text').get()
            thongtin['price'] = item.css('span.price::text').get()
            link = "https://viettelstore.vn" + str(item.css('a')[0].attrib['href'])
            thongtin['link'] = link
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('div', class_='digital').find_all('tr')
            for information in informations:
                lable = str(information.find_all('td')[0].text).replace(':', '')
                value = str(information.find_all('td')[1].text)
                thongtin[lable] = value
            yield convert(thongtin)
