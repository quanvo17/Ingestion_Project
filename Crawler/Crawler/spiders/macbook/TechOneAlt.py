import scrapy
import re
import unicodedata

class TechOneAlt(scrapy.Spider):
    name = 'techonealt'
    allowed_domains = ['techone.vn']
    start_urls = ['https://www.techone.vn/macbook']
    lst_url = []
    lst_color = ['silver','space gray' , 'gray','rose gold' ,'gold']
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

    def PreprocessItem(self,item):
            f_item = dict()
            f_item['name'] = item['name']
            f_item['color'] = 'undefined'
            
            name = item['name'].lower()
            #Color

            for color in self.lst_color:
                if color in name:
                    f_item['color'] = color
                    break
                elif 'grey' in name or 'xám' in name:
                    f_item['color'] = 'gray'
                    break
                elif 'bạc' in name or 'sliver' in name:
                    f_item['color'] = 'silver'
                    break

            # Status 
            f_item['status'] = 'new'

            f_item['resolution'] = ''
            #Resolution
            
            if f_item['resolution'] == '':
                if 'air' in name :
                    f_item['resolution'] = '1560 x 1600'
                elif 'pro' in name:
                    if '13 inch' in name or '13"' in name or '13.3"' in name or '13.3 inch' in name or '13in' in name:
                        f_item['resolution'] = '1560 x 1600'
                    elif '15 inch' in name or '15"' in name or '15.4"' in name or '15.4 inch' in name or '15in' in name:
                        f_item['resolution'] = '2880 x 1800'
                    elif '16 inch' in name or '16"' in name:
                        f_item['resolution'] = '3072 x 1920'

            if f_item['resolution'] == '':
                for key in item.keys():
                    if 'W x H' in key:
                        f_item['resolution'] = item[key]
                        break
            
            #screen tech
            f_item['screentech'] = 'retina' 

            #screensize
            screensize = ''
            if 'air' in name:
                screensize ='13'
            elif '13 inch' in name or '13"' in name or '13.3"' in name or '13.3 inch' in name or '13in' in name:
                screensize = '13'
            elif '15 inch' in name or '15"' in name or '15.4"' in name or '15.4 inch' in name or '15in' in name:
                screensize = '15'
            elif '16 inch' in name or '16"' in name:
                screensize = '16'

            if screensize == '':
                for key in item.keys():
                    if 'Kích thước màn hình' in key:
                        screensize = item[key]
                        break
            f_item['screensize'] = screensize

            #cam 
            f_item['rear_cam']='720p FaceTime HD camera'
            f_item['front_cam'] = 'No'

            #pin
            pin = ''
            for key in item.keys():
                if 'tin pin' in key.lower() or 'sử dụng thông thường' in key.lower():
                    pin = item[key]
                    break
            if pin == '':
                pin = 'Pin liền'
            f_item['pin'] = pin

            #sim
            f_item['sim'] = 'No'

            #cpu
            meta_cpu = []
            cpu = ''
            for key in item.keys():
                if 'cpu' in key.lower() or 'chipset' in key.lower():
                    meta_cpu.append(item[key])
            
            cpu = ' '.join(meta_cpu)
            if cpu =='':
                cpu = "Undefinded"
            f_item['cpu'] = cpu
            #ram
            meta_ram = []
            ram = ''
            for key in item.keys():
                if 'ram' in key.lower() or 'bus' in key.lower():
                    meta_ram.append(item[key])

            ram = ' '.join(meta_ram)
            if ram == '':
                ram = "Undefinded"
            f_item['ram'] = ram

            #rom
            rom = ''
            for key in item.keys():
                if 'lượng đĩa cứng' in key.lower():
                    rom = item[key]
                    break
            if rom == '':
                if '512gb' in name:
                    rom = '512gb'
                elif '256gb' in name:
                    rom ='256gb'
                elif '128gb' in name:
                    rom = '128gb'
                elif '1tb' in name:
                    rom = '1tb'
                elif '2tb' in name:
                    rom = '2tb'

            f_item['rom'] = rom

            #os
            f_item['os'] = 'MacOS'
            #gpu

            gpu = ''
            for key in item.keys():
                if 'đồ họa' in key.lower():
                    gpu = item[key]
                    break
            if gpu == '':
                gpu = 'card onboard'
            f_item['gpu'] = gpu

            #size
            size = ''
            meta_size = []
            for key in item.keys():
                if 'mm' in key.lower():
                    meta_size.append(item[key])
            size = ' x '.join(meta_size)
            if size == '':
                size = 'undefined'
            f_item['size'] = size

            #weight

            w0 = ''
            for key in item.keys():
                if 'kg' in key.lower():
                    w0 = item[key]
                    break
            if w0 == '':
                if 'air' in name :
                    w0 = '1.3'
                elif '13' in f_item['screensize']:
                    w0 = '1.3'
                elif '15' in f_item['screensize']:
                    w0= '1.8'
                elif '16' in f_item['screensize']:
                    w0 = '2.0'
                else:
                    w0 = '1.2'
    
            f_item['weight'] = w0
            #tech
            f_item['tech'] = 'Mac'
            #wifi

            f_item['wifi'] = '"Wi-Fi 802.11 b/g/n/ac"'
            
            #bluetooth

            f_item['bluetoorh'] = 'yes'
            #port
            pot = ''
            for value in item.values():
                if 'thunderbolt' in str(value).lower() or ' port' in str(value).lower():
                    pot = value

            if pot == '':
                pot = 'Thunderbolt'
            f_item['port'] = pot
                
            f_item['price'] = item['price_sale']
            f_item['link'] = item['url']
            return f_item

    def parse_macbook(self, response, url):
        item = dict()
        item['name'] = response.css(
            '.header_content > h1 ::text').extract_first()

        price = response.css(
            '.product-info-box > div > div > ins > .woocommerce-Price-amount::text ').extract_first()
        if price == None:
            price = response.css(
                '.product-info-box > div > div  > .woocommerce-Price-amount > bdi::text ').extract_first()
        item['price_sale'] = price
        r_price = response.css(
            '.product-info-box > div > div > del > .woocommerce-Price-amount::text ').extract_first()
        if r_price:
            item['price'] = r_price

        lst_params = response.css(
            '#myModal12 > div > div  >  div.modal-body> table >tbody >tr')
        for params in lst_params:
            if len(params.css('td::text')) > 1:
                params_name = params.css('td::text').extract_first().strip()
                params_value = params.css('td::text').extract()[1].strip()
                
                item[params_name] = params_value

        item['url'] = url
        item['website'] = self.allowed_domains[0]
        item['count'] = 'color' in item.keys()
        f_item = self.PreprocessItem(item)
        yield f_item

   
