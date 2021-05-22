import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class DienThoaiMoi(scrapy.Spider):
    name = 'iphone_DienThoaiMoi'
    start_urls = ["https://dienthoaimoi.vn/dien-thoai-apple-iphone-pcm135.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next-page")[0].click();'))
                assert(splash:wait(5))
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
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.product_grid')[0].css('div.item')
        for item in items:
            price = item.css('div.price_current::text').get()
            link = item.css('a.name').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtins = soup.find('table', class_='charactestic_table').find_all('tr')
            pin = ''
            for thongtin in thongtins:
                if str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                    '') == 'Công nghệ màn hình':
                    Cong_nghe_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n',
                                                                                                        '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Độ phân giải':
                    Do_phan_giai = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Màn hình rộng':
                    Kich_thuoc_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n',
                                                                                                         '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Camera sau':
                    Camera_sau = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                                  '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Camera trước':
                    Camera_truoc = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Camera trước':
                    Camera_truoc = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Đèn Flash':
                    flash = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Hệ điều hành':
                    he_dieu_hanh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Dung lượng pin':
                    pin = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r', '')
            yield convert({
                "Tên sản phẩm": str(item.css('h2 a::text').get()).replace('\n', '').replace('\t', ''),
                "Giá sản phẩm": price.replace('₫', ' VNĐ'),
                "Công nghệ màn hình": Cong_nghe_man_hinh,
                "Độ phân giải": Do_phan_giai,
                "Kích thước màn hình": Kich_thuoc_man_hinh,
                "Camera sau": Camera_sau,
                "Camera trước": Camera_truoc,
                "Đèn flash": flash,
                "Pin": (pin == '' and None or pin),
                "Hệ điều hành": he_dieu_hanh,
                "Link": link,
                'Loại sản phẩm': 'IPHONE',
                'Cửa hàng': 'DIEN THOAI MOI'
            })

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )