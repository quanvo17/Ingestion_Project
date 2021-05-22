import scrapy
from scrapy_splash import SplashRequest
import requests
from bs4 import BeautifulSoup
from Crawler.matching import *


class ClickBuy(scrapy.Spider):
    name = 'iphone_ClickBuy'
    start_urls = ["https://hcm.clickbuy.com.vn/danh-muc/iphone/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementById("sb-infinite-scroll-load-more-1").getElementsByTagName("a")[0].click();}'))
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
            link = item.css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            try:
                price = str(soup.find('p', class_='price').find('span').text)
                price = price.replace('\xa0₫', ' VNĐ')
            except:
                price = None
            try:
                color = soup.find('tr',
                                  class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_mau-sac').find(
                    'p').text
            except:
                color = None
            try:
                memory = soup.find('tr',
                                   class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_bo-nho-trong').find(
                    'p').text
            except:
                memory = None
            try:
                camera_chinh = soup.find('tr',
                                         class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_camera-chinh').find(
                    'p').text
            except:
                camera_chinh = None
            try:
                camera_phu = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_camera-phu').find(
                    'p').text
            except:
                camera_phu = None
            try:
                CPU = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_cpu').find(
                    'p').text
            except:
                CPU = None
            try:
                dophangiai = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_do-phan-giai-man-hinh').find(
                    'p').text
            except:
                dophangiai = None
            try:
                pin = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_dung-luong-pin').find(
                    'p').text
            except:
                pin = None
            try:
                hedieuhanh = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_he-dieu-hanh').find(
                    'p').text
            except:
                hedieuhanh = None
            try:
                kichthuocmanhinh = soup.find('tr',
                                             class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_kich-thuoc-man-hinh').find(
                    'p').text
            except:
                kichthuocmanhinh = None
            try:
                ram = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_ram').find(
                    'p').text
            except:
                ram = None
            yield {
                'Tên sản phẩm': item.css('h2.woocommerce-loop-product__title::text').get(),
                'Giá sản phẩm': price,
                'Link': link,
                # 'Màu sắc': color,
                'Bộ nhớ trong': memory,
                'Camera chính': camera_chinh,
                'Camera phụ': camera_phu,
                'CPU': CPU,
                "Độ phân giải màn hình": dophangiai,
                'Pin': pin,
                # 'Hệ điều hành': hedieuhanh,
                'Kích thước màn hình': kichthuocmanhinh,
                'Bluetooth': '',
                'Ram': ram,
            }