import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class NguyenKim(scrapy.Spider):
    name = 'iphone_NguyenKim'
    start_urls = ["https://www.nguyenkim.com/dien-thoai-di-dong-apple-iphone/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("nki-arow-rounded-next")[0].click();'))
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
        items = response.xpath('//*[@id="pagination_contents"]').css('div.item')
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
            link = item.css('div.product-title')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            try:
                informations = soup.find_all('table', class_='productSpecification_table')[1].find_all('tr')
                for information in informations:
                    if information.find('td', class_='title').text == 'Chipset:':
                        CPU = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == 'RAM:':
                        Ram = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == 'B??? nh??? trong:':
                        ROM = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == 'K??ch th?????c m??n h??nh:':
                        kich_thuoc_man_hinh = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == '????? ph??n gi???i m??n h??nh:':
                        do_phan_giai_man_hinh = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == 'Camera sau:':
                        Camera_sau = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == 'Camera tr?????c:':
                        Camera_truoc = information.find('td', class_='value').text
                    elif information.find('td', class_='title').text == 'Bluetooth:':
                        bluetooth = information.find('td', class_='value').text
            except:
                print("error " + str(link))
            yield convert({
                "T??n s???n ph???m": item.css('div.product-title a::text').get(),
                "Gi?? s???n ph???m": str(item.css('p.final-price::text').get()).replace('??', ' VN??'),
                "CPU": CPU,
                "Ram": Ram,
                "B??? nh??? trong": ROM,
                "K??ch th?????c m??n h??nh": kich_thuoc_man_hinh,
                "????? ph??n gi???i m??n h??nh": do_phan_giai_man_hinh,
                "Camera sau": Camera_sau,
                "Camera tr?????c": Camera_truoc,
                "Pin": Pin,
                "Bluetooth": bluetooth,
                "Link": link,
                'Th??? lo???i s???n ph???m': 'IPHONE',
                'C???a h??ng': 'NGUYEN KIM'
            })

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )