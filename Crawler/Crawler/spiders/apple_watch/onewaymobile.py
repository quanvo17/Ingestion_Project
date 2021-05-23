import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *

class onewaymobile_watch(scrapy.Spider):
    name = 'watch_onewaymobile'
    start_urls = ["https://onewaymobile.vn/apple-watch-pc61.html"]
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
            loai_man_hinh = ''
            chip = ''
            tinh_nang_khac = ''
            pin = ''
            bluetooth = ''
            ho_tro_sim = ''
            try:
                informations = soup.find_all('table', class_='shop_attributes')[1].find_all('tr')
                for information in informations:
                    if information.find('th').text == 'Loại màn hình' or information.find('th').text == 'Kiểu màn hình':
                        loai_man_hinh = information.find('p').text
                    elif information.find('th').text == 'Chipset' or information.find('th').text == 'Chip xử lý (CPU)':
                        chip = information.find('p').text
                    elif information.find('th').text == 'Tính năng khác':
                        tinh_nang_khac = information.find('p').text
                    elif information.find('th').text == 'Dung lượng pin (mAh)' or information.find('th').text == 'Pin':
                        pin = information.find('p').text
                    elif information.find('th').text == 'Bluetooth':
                        bluetooth = information.find('p').text
                    elif information.find('th').text == 'Hỗ trợ nhiều sim':
                        ho_tro_sim = information.find('p').text
            except:
                print("error: " + str(link))

            yield convert({
                "Tên sản phẩm": item.css('div.title-product')[0].css('a::text').get(),
                "Giá sản phẩm": str(item.css('span.final-price::text').get()).replace('đ', ' VNĐ'),
                "Loại màn hình": loai_man_hinh,
                "Chip": chip,
                "Tính năng khác": tinh_nang_khac,
                "Pin": pin,
                "Bluetooth": bluetooth,
                "Hỗ trợ sim": ho_tro_sim,
                "Link": link,
                'Thể loại sản phẩm': 'APPLE WATCH',
                'Cửa hàng': 'ONE WAY MOBILE'
            })

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )
