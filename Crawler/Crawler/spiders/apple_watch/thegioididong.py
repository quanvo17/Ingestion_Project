import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class TheGioiDiDong_watch(scrapy.Spider):
    name = 'watch_thegioididong'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://www.thegioididong.com/dong-ho-thong-minh-apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("viewmore")[0].click();}catch(e){}'))
                assert(splash:wait(2))
                assert(splash:runjs('try{document.getElementsByClassName("viewmore")[0].click();}catch(e){}'))
                assert(splash:wait(2))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        items = response.css('li.item')
        for item in items:
            thongtin = dict()
            link = 'https://www.thegioididong.com' + item.css('a').attrib['href']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('div', class_='parameter').find_all('li')
            thongtin['name'] = str(item.css('h3::text').get()).replace('\n', '')
            thongtin['price'] = str(item.css('strong.price::text').get()).replace('₫', ' VND')
            thongtin['link'] = link
            for information in informations:
                label = str(information.find('p', class_='lileft').text).replace(':','').replace('\n', '').replace('\t', '').replace('\r', '')
                value = str(information.find('div', class_='liright').text).replace('\n', '').replace('\t', '').replace('\r', '')
                thongtin[label] = value
            yield convert(thongtin)


