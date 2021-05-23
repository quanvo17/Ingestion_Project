import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class DienThoaiMoi(scrapy.Spider):
    name = 'ipad_dienthoaimoi'
    start_urls = ["https://dienthoaimoi.vn/dien-thoai-apple-iphone-pcm135.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next-page")[0].click();'))
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
        items = response.css('div.product_grid')[0].css('div.item')
        for item in items:
            thongtin = dict()
            thongtin['name'] = str(item.css('a.name::text').get()).replace('\t', '').replace('\n', '').replace('\r', '')
            thongtin['price'] = str(item.css('div.price_current::text').get()).replace('₫', ' VND')
            link = item.css('a.name')[0].attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtin['link'] = link
            informations = soup.find('table', class_='compare_table').find_all('tr')
            for information in informations:
                try:
                    label = str(information.find('td', class_='title_charactestic').text).replace('\t', '').replace('\n', '').replace('\r', '')
                    value = str(information.find('td', class_='content_charactestic').text).replace('\t', '').replace('\n', '').replace('\r', '')
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
