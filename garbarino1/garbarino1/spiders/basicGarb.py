# -*- coding: utf-8 -*-

import datetime
import urlparse
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from garbarino1.items import Garbarino1Item

class BasicgarbSpider(scrapy.Spider):
    name = "basicGarb"
    allowed_domains = ["www.garbarino.com"]
    start_urls = (
        'https://www.garbarino.com/producto/tv-led-3d-sony-65-4k-ultra-hd-xbr-65x905c/2cf5e5032a',
    )

    def parse(self, response):
        i = ItemLoader(item=Garbarino1Item() ,response=response)
        
        i.add_xpath('title','//*[@class="gb-main-detail-title"][1]/h1/text()',MapCompose(unicode.strip, unicode.title))
        i.add_xpath('price','//*[@class="gb-main-detail-prices-current"][1]/text()',MapCompose(lambda i: i.replace(',', ''), float),re='[,.0-9]+')
        i.add_xpath('description','/html/body/div[3]/div[1]/div[1]/h2/text()',MapCompose(unicode.strip), Join())
        i.add_xpath('image_urls','//*[@id="main-image"][1]/@src',MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        i.add_value('url', response.url)
        i.add_value('project', self.settings.get('BOT_NAME'))
        i.add_value('spider', self.name)
        i.add_value('server', socket.gethostname())
        i.add_value('date', datetime.datetime.now())

        return i.load_item()

