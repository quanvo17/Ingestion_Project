import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class OneWayMobile(scrapy.Spider):
    name = 'iphone_OneWayMobile'
    start_urls = ["https://onewaymobile.vn/iphone-pc29.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next-page")[0].getElementsByTagName("i")[0].click();'))
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
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}
        items = response.xpath('//*[@id="home-product-list"]/div').css('div.image-check')
        for item in items:
            link = item.css('div.title-product')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            Ram = ''
            CPU = ''
            kich_thuoc_man_hinh = ''
            ROM = ''
            do_phan_giai_man_hinh = ''
            Pin = ''
            Camera_sau = ''
            Camera_truoc = ''
            bluetooth = ''
            try:
                informations = soup.find_all('table', class_='shop_attributes')[1].find_all('tr')
                for information in informations:
                    if information.find('th').text == 'RAM':
                        Ram = information.find('p').text
                    elif information.find('th').text == 'CPU' or information.find('th').text == 'Chip x??? l?? (CPU)':
                        CPU = information.find('p').text
                    elif information.find('th').text == 'K??ch th?????c m??n h??nh':
                        kich_thuoc_man_hinh = information.find('p').text
                    elif information.find('th').text == 'B??? nh??? trong':
                        ROM = information.find('p').text
                    elif information.find('th').text == 'Bluetooth':
                        bluetooth = information.find('p').text
                    elif information.find('th').text == '????? ph??n gi???i m??n h??nh':
                        do_phan_giai_man_hinh = information.find('p').text
                    elif information.find('th').text == 'Pin' or information.find('th').text == 'Dung l?????ng pin (mAh)':
                        Pin = information.find('p').text
                    elif information.find('th').text == 'M??y ???nh ch??nh':
                        Camera_sau = information.find('p').text
                    elif information.find('th').text == 'M??y ???nh ph???':
                        Camera_truoc = information.find('p').text
            except:
                print("error: " + str(link))

            yield convert({
                "T??n s???n ph???m": item.css('div.title-product')[0].css('a::text').get(),
                "Gi?? s???n ph???m": str(item.css('span.final-price::text').get()).replace('??', ' VN??'),
                "K??ch th?????c m??n h??nh ": kich_thuoc_man_hinh,
                "????? ph??n gi???i m??n h??nh": do_phan_giai_man_hinh,
                "CPU": CPU,
                "RAM": Ram,
                "B??? nh??? trong": ROM,
                "Pin": Pin,
                "Bluetooth": bluetooth,
                "Camera sau": Camera_sau,
                "Camera tr?????c": Camera_truoc,
                "Link": link,
                'Th??? lo???i s???n ph???m': 'IPHONE',
                'C???a h??ng': 'ONE WAY MOBILE'
            })

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )