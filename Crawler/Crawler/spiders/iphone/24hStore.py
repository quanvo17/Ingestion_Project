import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class iphone_24hstore(scrapy.Spider):
    name = 'iphone_24hstore'
    start_urls = ["https://24hstore.vn/dien-thoai-iphone-apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementById("load_more_button").click();}'))
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

        items = response.xpath('//*[@id="box_product"]').css('div.product')
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
            link = item.css('div.frame_inner')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            try:
                # print(link)
                # print(len(soup.find_all('table', class_='charactestic_table_detail')))
                informations = soup.find_all('table', class_='charactestic_table_detail')[0].find_all('tr')
                for information in informations:
                    if information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                     '') == 'Mànhìnhrộng:':
                        kich_thuoc_man_hinh = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                                          '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'Độphângiải:':
                        do_phan_giai_man_hinh = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                                            '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'Ram:':
                        Ram = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                          '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'Bộnhớtrong:':
                        ROM = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                          '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'CPU:':
                        CPU = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                          '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'CameraSau:':
                        Camera_sau = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                                 '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'Cameratrước:':
                        Camera_truoc = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                                   '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'Dunglượngpin:':
                        Pin = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                          '').replace(
                            '\n', '')
                    elif information.find_all('td')[0].text.replace(' ', '').replace('\r', '').replace('\n',
                                                                                                       '') == 'Bluetooth:':
                        bluetooth = information.find_all('td')[1].text.replace(' ', '').replace('\r',
                                                                                                '').replace(
                            '\n', '')

                yield {
                    'Tên sản phẩm': item.css('div.name h3::text').get(),
                    'Giá sản phẩm': str(item.css('span.price::text').get()).replace('đ', ' VNĐ'),
                    'Kích thước màn hình': kich_thuoc_man_hinh,
                    'Độ phân giải màn hình': do_phan_giai_man_hinh,
                    'Ram': Ram,
                    'Bộ nhớ trong': ROM,
                    'CPU': CPU,
                    'Camera sau': Camera_sau,
                    'Camera trước': Camera_truoc,
                    'Pin': Pin,
                    'Bluetooth': bluetooth,
                    'Link': link
                }
            except:
                continue