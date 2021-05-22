# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SchemaItems(scrapy.Item):
    name = Field()
    color = Field()
    status = Field()    # cũ, mới
    resolution = Field()
    screentech = Field()
    screensize = Field()
    rear_cam = Field()
    front_cam = Field()
    pin = Field()
    sim = Field()
    cpu = Field()
    ram = Field()
    rom = Field()
    os = Field()
    gpu = Field()
    size = Field()
    weight = Field()
    tech = Field()
    wifi = Field()
    bluetooth = Field()
    port = Field()
    price = Field()
    link = Field()