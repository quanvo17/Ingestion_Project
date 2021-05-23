import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import  *

class NguyenKim(scrapy.Spider):
    name = 'ipad_NguyenKim'
    start_urls = ["https://www.nguyenkim.com/tim-kiem.html?tu-khoa=ipad"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('try{document.getElementsByClassName("page-link indicator next")[0].click()}catch(e){};'))
                assert(splash:wait(5))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """
    script_await = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(2))
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
        items = response.css('div.product-card')
        thongtin = dict()
        for item in items:
            thongtin['name'] = item.css('a.nk-product-link::text').get()
            thongtin['price'] = item.css('p.product-card__price-after-amount::text').get()
            link = item.css('a.nk-product-link').attrib['href']
            thongtin['link'] = link
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('table', class_='productSpecification_table').find_all('tr')
            for information in informations:
                title = information.find('td', class_='title').text
                value = information.find('td', class_='value').text
                thongtin[title] = value

            yield convert(thongtin)

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )