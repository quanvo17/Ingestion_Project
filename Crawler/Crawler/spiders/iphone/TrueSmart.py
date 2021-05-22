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
                if str(information.find_all('td')[0].text).replace('\n', '').replace('\t', '') == 'Bộ nhớ trong' or str(
                        information.find_all('td')[0].text).replace('\n', '').replace('\t', '') == 'Bộ nhớ trong:':
                    ROM = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                       '') == 'Kích thước màn hình' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                          '') == 'Kích thước màn hình:':
                    kich_thuoc_man_hinh = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                       '') == 'Độ phân giải màn hình' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace(
                            '\n', '') == 'Độ phân giải màn hình:':
                    do_phan_giai_man_hinh = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Dung lượng pin' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n',
                                                                                          '') == 'Dung lương pin:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Pin:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Pin':
                    Pin = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera sau:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera sau':
                    Camera_sau = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera trước:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'Camera trước':
                    Camera_truoc = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'CPU:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'CPU':
                    CPU = information.find_all('td')[1].text
                elif str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'RAM:' or \
                        str(information.find_all('td')[0].text).replace('\t', '').replace('\n', '') == 'RAM':
                    Ram = information.find_all('td')[1].text

            yield {
                'Tên sản phẩm': item.css('strong.t')[0].css('a::text').get(),
                'Giá sản phẩm': str(item.css('b.b::text').get()).replace('₫', 'VNĐ'),
                'Bộ nhớ trong': ROM,
                'Độ phân giải màm hình': do_phan_giai_man_hinh,
                'Kích thước mnaf hình': kich_thuoc_man_hinh,
                'Camera sau': Camera_sau,
                'Camera trước': Camera_truoc,
                "CPU": CPU,
                "RAM": Ram,
                "Pin": Pin,
                'Link': link
            }