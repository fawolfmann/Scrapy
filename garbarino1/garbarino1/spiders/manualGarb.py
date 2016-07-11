# -*- coding: utf-8 -*-
import scrapy


class ManualgarbSpider(scrapy.Spider):
    name = "manualGarb"
    allowed_domains = ["www.garbarino.com"]
    start_urls = (
        'http://www.www.garbarino.com/',
    )

    def parse(self, response):
        pass
