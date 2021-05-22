import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class CellPhone(scrapy.Spider):
    name = 'iphone_CellPhone'
    start_urls = ["https://cellphones.com.vn/mobile/apple.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("pagination")[1].getElementsByTagName("a")[0].click();'))
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
        items = response.css('li.cate-pro-short')
        for item in items:
            price = str(item.css('span.price::text').get())
            link = item.css('div.lt-product-group-info')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtin = soup.find('div', class_='content')
            try:
                bluetooth = thongtin.find_all('tr')[29].find_all('td')[1].text
            except:
                print()

            yield convert({
                "Tên sản phẩm": str(item.css('div.lt-product-group-info')[0].css('h3::text').get()).replace('\t', ''),
                "Link": link,
                "Giá sản phẩm": price.replace('\xa0₫', ' VNĐ'),
                "Kích thước màn hình": thongtin.find_all('tr')[0].find_all('td')[1].text,
                "Độ phân giải màn hình": thongtin.find_all('tr')[1].find_all('td')[1].text,
                "Camera sau": thongtin.find_all('tr')[2].find_all('td')[1].text,
                "Camera trước": thongtin.find_all('tr')[3].find_all('td')[1].text,
                "CPU": thongtin.find_all('tr')[4].find_all('td')[1].text,
                "Ram": thongtin.find_all('tr')[5].find_all('td')[1].text,
                "Bộ nhớ trong": thongtin.find_all('tr')[6].find_all('td')[1].text,
                "Pin": thongtin.find_all('tr')[7].find_all('td')[1].text,
                "Bluetooth": bluetooth,
                'Loại sản phẩm': 'IPHONE',
                'Cửa hàng': 'CELL_PHONE'
            })
        if str(response.css('ul.pagination')[1].css('a::text').get()) == 'Tiếp ':
            yield SplashRequest(
                response.url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )