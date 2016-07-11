# -*- coding: utf-8 -*-
import scrapy
import datetime
import urlparse

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

from garbarino1.items import Garbarino1Item


class Garba1Spider(CrawlSpider):
    name = 'garba1'
    allowed_domains = ["www.garbarino.com"]
    start_urls = ('https://www.garbarino.com/productos/televisores-y-video/4272',)

    rules = (
            Rule(LinkExtractor(restrict_xpaths='//*[@class="ng-isolate-scope"]'),callback='parse_item'),)

    def parse_item(self, response):
        i = ItemLoader(item=Garbarino1Item() ,response=response)
        
        i.add_xpath('title','//*[@class="gb-main-detail-title"][1]/@h1/text()',MapCompose(unicode.strip, unicode.title))
        i.add_xpath('price','//*[@class="gb-main-detail-prices-current"][1]/text()',MapCompose(lambda i: i.replace(',', ''), float),re='[,.0-9]+')
        i.add_xpath('description','*[//@class="gb-main-detail-description"][1]/text()',MapCompose(unicode.strip), Join())
        i.add_xpath('image_urls','//*[@id="main-image"][1]/@src',MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        i.add_value('url', response.url)
        i.add_value('project', self.settings.get('BOT_NAME'))
        i.add_value('spider', self.name)
        i.add_value('server', socket.gethostname())
        i.add_value('date', datetime.datetime.now())

        return i.load_item()
