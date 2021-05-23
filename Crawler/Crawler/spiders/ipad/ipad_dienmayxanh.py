import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class DienMayXanh(scrapy.Spider):
    name = 'ipad_dienmayxanh'
    start_urls = ["https://www.dienmayxanh.com/may-tinh-bang-apple-ipad"]
    script = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
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
        items = response.css('li.item')
        for item in items:
            thongtin = dict()
            thongtin['name'] = str(item.css('h3::text').get()).replace('\n', '').replace('\t', '')
            thongtin['price'] = str(item.css('strong.price::text').get()).replace('\n', '').replace('\t', '')
            link  = "https://www.dienmayxanh.com"+str(item.css('a')[0].attrib['href'])
            thongtin['link'] = link
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find(class_='parameter').find_all('li')
            for information in informations:
                label = str(information.text).split(':')[0].replace('\n', '').replace('\t', '')
                value = str(information.text).split(':')[1].replace('\n', '').replace('\t', '')
                thongtin[label] = value

            yield convert(thongtin)