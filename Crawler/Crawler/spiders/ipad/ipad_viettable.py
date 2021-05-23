# import scrapy
# from scrapy_splash import SplashRequest
# from scrapy import *
# import requests
# from bs4 import BeautifulSoup
# from Crawler.matching import *
#
#
# class ipad_viettable(scrapy.Spider):
#     name = 'ipad_viettable'
#     start_urls = ["https://www.viettablet.com/may-tinh-bang"]
#     script = """
#             function main(splash)
#                 local url = splash.args.url
#                 assert(splash:go(url))
#                 assert(splash:wait(1))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#                 assert(splash:wait(2))
#                 assert(splash:runjs('try{document.getElementsByClassName("more_load_page ")[0].click()}catch(e){}'))
#
#                 return {
#                     html = splash:html(),
#                     url = splash:url(),
#                 }
#             end
#             """
#
#     def start_requests(self):
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#         for url in self.start_urls:
#             yield SplashRequest(
#                 url,
#                 callback=self.parse,
#                 headers=headers,
#                 meta={
#                     "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
#                 },
#             )
#
#     def parse(self, response):
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#
#         items = response.css('div.product_list_column5')
#         for item in items:
#             thongtin = dict()
#             thongtin['name'] = item.css('a.product-title::text').get()
#             thongtin['price'] = item.css('span.price-num::text').get()
#             link = item.css('a')[0].attrib['href']
#             thongtin['link'] = link
#             req = requests.get(link, headers=headers)
#             soup = BeautifulSoup(req.text, "lxml")
#             informations = soup.find('div', class_='sattribute-product').find('ul').find_all('li')
#             for information in informations:
#                 print(information)
#                 label = str(information.css('::text').get()).split(':')[0]
#
#             yield thongtin
