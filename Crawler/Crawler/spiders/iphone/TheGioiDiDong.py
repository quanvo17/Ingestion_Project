import scrapy
from scrapy_splash import SplashRequest
from scrapy import *
import requests
from bs4 import BeautifulSoup
# from Crawler.matching import *


class TheGioiDiDong(scrapy.Spider):
    name = 'iphone_TheGioiDiDong'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://www.thegioididong.com/dtdd-apple-iphone"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("viewmore")[0].click();'))
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
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)
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
            Ram = ''
            CPU = ''
            kich_thuoc_man_hinh = ''
            ROM = ''
            do_phan_giai_man_hinh = ''
            Pin = ''
            Camera_sau = ''
            Camera_truoc = ''
            bluetooth = ''
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            link = 'https://www.thegioididong.com/' + str(item.css('a').attrib['href'])
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('ul', class_='parameter')
            try:
                man_hinh = informations.find('li', class_='g6459_79_77')
                kich_thuoc_man_hinh = man_hinh.split(',')[1]
            except:
                print()
            try:
                Ram = informations.find('li', class_='g50').find('div').text
            except:
                print()
            try:
                ROM = informations.find('li', class_='g49').find('div').text
            except:
                print()
            try:
                Camera_sau = informations.find('li', class_='g27').find('div').text
            except:
                print()
            try:
                Camera_truoc = informations.find('li', class_='g29').find('div').text
            except:
                print()
            try:
                Pin = informations.find('li', class_='g84_26846').find('div').text
            except:
                print()
            try:
                CPU = informations.find('li', class_='g6059').find('div').text
            except:
                print()

            # yield convert( {
            #     'Tên sản phẩm': str(item.css('h3::text').get()).replace('\n', ''),
            #     'Giá sản phẩm': str(item.css('div.price strong::text').get()).replace('₫', ' VNĐ'),
            #     'Kích thước màn hình': kich_thuoc_man_hinh,
            #     'Ram': Ram,
            #     'Bộ nhớ trong': ROM,
            #     'CPU': CPU,
            #     'Camera sau': Camera_sau,
            #     'Camera trước': Camera_truoc,
            #     'Pin': Pin,
            #     'Độ phân giải màn hình': do_phan_giai_man_hinh,
            #     'Bluetooth': bluetooth,
            #     'Link': link,
            #     'Loại sản phẩm': 'IPHONE',
            #     'Tên cửa hàng': 'THE GIOI DI DONG'
            # })