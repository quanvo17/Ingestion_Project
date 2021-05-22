import scrapy
from scrapy_splash import SplashRequest
from scrapy import *
import requests
from bs4 import BeautifulSoup
# from Crawler.matching import *


class didongthongminh_iphone(scrapy.Spider):
    name = 'iphone_DiDongThongMinh'
    start_urls = ["https://didongthongminh.vn/iphone"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("lmp_button")[0].click()'))
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

        items = response.xpath('//*[@id="main"]/ul').css('li.col-6')

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
            link = item.css('a.woocommerce-LoopProduct-link').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('table', class_='shop_attributes').find_all('tr')
            for information in informations:
                try:
                    if information.find('th').text == 'Màn hình':
                        kich_thuoc_man_hinh = information.find('a').text
                    elif information.find('th').text == 'CPU':
                        CPU = information.find('a').text
                    elif information.find('th').text == 'RAM':
                        Ram = information.find('a').text
                    elif information.find('th').text == 'Bộ nhớ trong':
                        ROM = information.find('a').text
                    elif information.find('th').text == 'Camera sau':
                        Camera_sau = information.find('a').text
                    elif information.find('th').text == 'Camera trước':
                        Camera_truoc = information.find('a').text
                    elif information.find('th').text == 'Pin':
                        Pin = information.find('a').text
                    elif information.find('th').text == 'Bluetooth':
                        bluetooth = information.find('a').text
                except:
                    continue
            yield {
                "name": item.css('span.dst_primtitle::text').get(),
                "Giá sản phẩm": item.css('span.woocommerce-Price-amount::text').get() + ' VNĐ',
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