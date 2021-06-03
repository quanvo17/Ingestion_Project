import scrapy


class TechOne(scrapy.Spider):
    name = 'macbook_TechOne'
    allowed_domains = ['techone.vn']
    start_urls = ['https://www.techone.vn/macbook']
    lst_url = []

    def parse(self, response):
        for page_url in response.css('.cats-child-destop > li > a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(page_url), callback=self.parse_page)

    def parse_page(self, response):
        for item_url in response.css('.product_item_link > .product_item_img > a::attr(href)').extract():
            if item_url not in self.lst_url:
                self.lst_url.append(item_url)
                yield scrapy.Request(response.urljoin(item_url), callback=self.parse_macbook, cb_kwargs={'url': item_url})
        
        next_page = response.css('.next::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_page)

    def parse_macbook(self, response, url):
        item = dict()
        item['name'] = response.css('.header_content > h1 ::text').extract_first()

        price = response.css('.product-info-box > div > div > ins > .woocommerce-Price-amount::text ').extract_first()
        if price == None:
            price = response.css('.product-info-box > div > div  > .woocommerce-Price-amount > bdi::text ').extract_first()
        item['price_sale'] = price
        r_price = response.css('.product-info-box > div > div > del > .woocommerce-Price-amount::text ').extract_first()
        if r_price:
            item['price'] = r_price

        lst_params =  response.css('#myModal12 > div > div  >  div.modal-body> table >tbody >tr')
        for params in lst_params:
            if len(params.css('td::text')) > 1:
                params_name = params.css('td::text').extract_first().strip()
                params_value = params.css('td::text').extract()[1].strip()

                if 'CPU' in params_name or 'cpu' in params_name:
                    params_name = 'cpu'
                elif 'RAM' in params_name or 'ram' in params_name:
                    params_name = 'ram'
                elif 'đĩa cứng' in params_name:
                    params_name = 'rom'

                item[params_name] = params_value

        item['url'] = url
        item['website'] = self.allowed_domains[0]

        yield item
