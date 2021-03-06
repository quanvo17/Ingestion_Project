import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class TrueSmart(scrapy.Spider):
    name = 'iphone_TrueSmart'
    start_urls = [
        "https://www.truesmart.com.vn/dien-thoai/iphone/",
        "https://www.truesmart.com.vn/iphone/page-2.html",
        "https://www.truesmart.com.vn/iphone/page-3.html",
        "https://www.truesmart.com.vn/iphone/page-4.html",
        "https://www.truesmart.com.vn/iphone/page-5.html"
    ]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("nki-arow-rounded-next")[0].click();'))
                assert(splash:wait(2))
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
        items = response.css('ul.pul')[0].css('li.c')
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
            link = 'https://www.truesmart.com.vn' + str(item.css('strong.t')[0].css('a').attrib['href'])
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            informations = soup.find('div', class_='cp1').find_all('tr')
            for information in informations:
                if str(information.find_all('td')[0].text).replace('\n', '').replace('\t', '') == 'B??? nh??? trong' or str(
                        information.find_all('td')[0].text).replace('\n', '').replace('\t', '') == 'B??? nh??? trong:':
                    ROM = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                       '') == 'K??ch th?????c m??n h??nh' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                          '') == 'K??ch th?????c m??n h??nh:':
                    kich_thuoc_man_hinh = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                       '') == '????? ph??n gi???i m??n h??nh' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace(
                            '\n', '') == '????? ph??n gi???i m??n h??nh:':
                    do_phan_giai_man_hinh = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Dung l?????ng pin' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                          '') == 'Dung l????ng pin:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Pin:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Pin':
                    Pin = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera sau:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera sau':
                    Camera_sau = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera tr?????c:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera tr?????c':
                    Camera_truoc = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'CPU:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'CPU':
                    CPU = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'RAM:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'RAM':
                    Ram = information.find_all('td')[1].text

            yield convert({
                'T??n s???n ph???m': item.css('strong.t')[0].css('a::text').get(),
                'Gi?? s???n ph???m': str(item.css('b.b::text').get()).replace('???', 'VN??'),
                'B??? nh??? trong': ROM,
                '????? ph??n gi???i m??m h??nh': do_phan_giai_man_hinh,
                'K??ch th?????c mnaf h??nh': kich_thuoc_man_hinh,
                'Camera sau': Camera_sau,
                'Camera tr?????c': Camera_truoc,
                "CPU": CPU,
                "RAM": Ram,
                "Pin": Pin,
                'Link': link
            })