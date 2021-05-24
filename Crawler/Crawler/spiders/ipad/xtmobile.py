import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class ipad_xtmobile(scrapy.Spider):
    name = 'ipad_xtmobile'
    start_urls = ["https://www.xtmobile.vn/ipad"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
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

        items = response.xpath('//*[@id="List_Product"]').css('div.product-base-grid')
        for item in items:
            thongtin = dict()
            thongtin['name'] = item.css('div.pinfo a::text').get()
            thongtin['price'] = str(item.css('div.price::text').get()).replace('đ', '')
            link = thongtin['link'] = "https://www.xtmobile.vn" + str(item.css('div.pinfo a').attrib['href'])
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('ul', class_='parametdesc').find_all('li')
            for information in informations:
                label = str(information.find('span').text).replace(':','')
                value = information.find('strong').text
                thongtin[label] = value
            yield convert(thongtin)
