import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class iphone_24hStore(scrapy.Spider):
    name = 'iphone_24hstore'
    start_urls = ["https://24hstore.vn/dien-thoai-iphone-apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementById("load_more_button").click();}'))
                assert(splash:wait(1))
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

        items = response.xpath('//*[@id="box_product"]').css('div.product')
        for item in items:
            thongtin = dict()
            link = item.css('div.frame_inner')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('table', class_='charactestic_table').find_all('tr')
            for information in informations:
                label = str(information.find_all('td')[0].text).replace('\n', '').replace('\t', '').replace('\r', '').replace(":", '')
                value = str(information.find_all('td')[1].text).replace('\n', '').replace('\t', '').replace('\r', '').replace(":", '')
                thongtin[label] = value
            thongtin['name'] = item.css('div.name h3::text').get()
            thongtin['price'] =item.css('span.price::text').get()
            yield convert(thongtin)