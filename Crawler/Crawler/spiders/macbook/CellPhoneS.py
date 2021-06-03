import scrapy
from scrapy import item


class MacbookCellphonesSpider(scrapy.Spider):
    name = 'macbook_CellphoneS'
    allowed_domains = ['cellphones.com.vn']
    start_urls = ['https://cellphones.com.vn/laptop/mac.html',
                  'https://cellphones.com.vn/laptop/mac.html?p=2']
    handle_httpstatus_list = [301]

    def parse(self, response):
        # Request tới từng sản phẩm có trong danh sách các Macbook dựa vào href
        for product in response.css(".list-laptop > ul > li"):
            # item = DemoScrapyItem()
            # item['product_name'] = product.css('div > a > h3 ::text').extract()[0]  # Tên macbook
            # #item['product_name'] = "XXXXXX"
            # item['price_sale'] = product.css('.price-box > p.special-price > span::text').extract_first()

            # item['price'] = product.css('.price-box > p.old-price > span::text').extract_first()

            # item['rate_average'] = 'abc'
            if(len(product.css(".lt-product-group-cau-hinh > table > tr > td"))):
                cpu = product.css(
                    ".lt-product-group-cau-hinh > table > tr > td ")[1].css("::text").extract_first()
                vga = product.css(
                    ".lt-product-group-cau-hinh > table > tr > td ")[3].css("::text").extract_first()
                dr = product.css(
                    ".lt-product-group-cau-hinh > table > tr > td ")[5].css("::text").extract_first()
            else:
                cpu = ""
                vga = ""
                dr = ""
            item_url = product.css(
                ".lt-product-group-info > a ::attr(href)").extract_first()
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_macbook, cb_kwargs={'cpu': cpu, 'vga': vga, 'dr': dr, "url": item_url})

    def parse_macbook(self, response, cpu, vga, dr, url):
        item = dict()

        item['name'] = response.css(
            'div.topview > h1 ::text').extract_first()
        item['price_sale'] = response.css(
            'p.special-price > span::text').extract_first()
        item['price'] = response.css(
            'p.old-price > span::text').extract_first()
        item['cpu'] = cpu
        item['gpu'] = vga

        lst_params = response.css('#tskt > tr')
        for params in lst_params:
            if len(params.css('td')) > 1:
                params_name = params.css('td::text').extract_first()
                if 'RAM' in params_name or 'ram' in params_name:
                    params_value = params.css('td::text').extract()[1]
                    item['ram'] = params_value

        item['rom'] = dr
        item['url'] = url
        item['website'] = self.allowed_domains[0]

        yield item