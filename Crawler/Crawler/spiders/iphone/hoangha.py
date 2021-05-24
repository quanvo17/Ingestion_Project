import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import  *

class hoangha(scrapy.Spider):
    name = 'iphone_hoangha'
    start_urls = ["https://hoanghamobile.com/dien-thoai-di-dong/iphone"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('try{document.getElementsByClassName("more-product")[0].getElementsByTagName("a")[0].click()}catch(e){};'))
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
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}
        items = response.xpath('/html/body/section[4]/div/div[1]/div').css('div.item')
        for item in items:
            thongtin = dict()
            thongtin['name'] = str(item.css('div.info a::text').get())
            thongtin['price'] = str(item.css('span.price strong::text').get()).replace('₫', 'VND')
            link = thongtin['link'] = "https://hoanghamobile.com" + str(item.css('div.info a').attrib['href'])
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('div', class_='specs-special').find_all('li')
            for information in informations:
                label = str(information.find('strong').text).replace(':', '')
                value = str(information.find('span').text)
                thongtin[label] = value
            yield convert(thongtin)
