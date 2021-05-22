import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class XTSmart(scrapy.Spider):
    name = 'iphone_XTSmart'
    start_urls = ["https://www.xtsmart.vn/apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementsByClassName("pagination-more")[0].getElementsByTagName("i")[0].click()}'))
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

        items = response.xpath('//*[@id="List_Product"]').css('div.product-base-grid')
        for item in items:
            Ram = ''
            CPU = ''
            kich_thuoc_man_hinh = ''
            ROM = ''
            do_phan_giai_man_hinh = ''
            Pin = ''
            Camera_sau = ''
            Camera_truoc = ''
            bluetooth = ''
            link = item.css('h3 a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('ul', class_='paraexpand').find_all('li')
            for information in informations:
                try:
                    if information.find('span').text == 'Chipset (hãng SX CPU)':
                        CPU = information.find('strong').text
                    elif information.find('span').text == 'RAM':
                        Ram = information.find('strong').text
                    elif information.find('span').text == 'Bộ nhớ trong':
                        ROM = information.find('strong').text
                    elif information.find('span').text == 'Bluetooth':
                        bluetooth = information.find('strong').text
                    elif information.find('span').text == 'Màn hình rộng':
                        kich_thuoc_man_hinh = information.find('strong').text
                    elif information.find('span').text == 'Độ phân giải':
                        do_phan_giai_man_hinh = information.find('strong').text
                    elif information.find('span').text == 'Dung lượng pin':
                        Pin = information.find('strong').text

                except:
                    continue
            yield {
                "Tên sản phẩm": item.css('h3 a::text').get(),
                "Giá sản phẩm": item.css('div.price::text').get().replace('đ', 'VNĐ'),
                'CPU': CPU,
                'RAM': Ram,
                "Bộ nhớ trong": ROM,
                "Kích thước màn hình": kich_thuoc_man_hinh,
                "Độ phân giải màn hình": do_phan_giai_man_hinh,
                'Pin': Pin,
                "Bluetooth": bluetooth,
                "Camera sau": Camera_sau,
                'Camera trước': Camera_truoc,
                "Link": link
            }