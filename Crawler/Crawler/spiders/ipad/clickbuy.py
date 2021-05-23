import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class ClickBuy(scrapy.Spider):
    name = 'ipad_ClickBuy'
    start_urls = ["https://clickbuy.com.vn/danh-muc/apple-ipad/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementById("sb-infinite-scroll-load-more-1").getElementsByTagName("a")[0].click();'))
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

        items = response.xpath('//*[@id="main"]/ul').css('li.col-6')
        for item in items:
            thongtin = dict()
            thongtin['name'] = item.css('h2.woocommerce-loop-product__title::text').get()
            thongtin['price'] = str(item.css('span.woocommerce-Price-amount::text').get()).replace('\xa0', ' VNĐ')
            link = item.css('a.woocommerce-LoopProduct-link')[0].attrib['href']
            thongtin['link'] = link
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('table', class_='woocommerce-product-attributes shop_attributes').find_all('tr')
            for information in informations:
                title = str(information.find('th', class_='woocommerce-product-attributes-item__label').text).replace('\n', '').replace('\t', '')
                value = str(information.find('td', class_='woocommerce-product-attributes-item__value').text).replace('\n', '').replace('\t', '')
                thongtin[title] = value

            yield convert(thongtin)
