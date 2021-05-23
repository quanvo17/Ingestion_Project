import scrapy
from scrapy_splash import SplashRequest
from scrapy import *
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class DiDongThongMinh(scrapy.Spider):
    name = 'ipad_DiDongThongMinh'
    start_urls = ["https://didongthongminh.vn/?s=ipad&post_type=product"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
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

        items = response.xpath('//*[@id="main"]/ul').css('li.col-6')
        for item in items:
            thongtin = dict()
            thongtin['name'] = str(item.css('span.dst_primtitle::text').get()).replace('\n', '').replace('\t', '').replace('\r', '')
            thongtin['price'] = str(item.css('span.woocommerce-Price-amount::text').get()).replace('\n', '').replace('\t', '').replace('\r', '') + ' VND'
            link = item.css('a')[0].attrib['href']
            thongtin['link'] = link
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('table', class_='shop_attributes').find_all('tr')
            for information in informations:
                label = str(information.find('th').text).replace('\n', '').replace('\t', '').replace('\r', '')
                value = str(information.find('td').text).replace('\n', '').replace('\t', '').replace('\r', '')
                thongtin[label] = value

            yield  convert(thongtin)