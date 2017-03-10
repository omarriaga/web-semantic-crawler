# -*- coding: utf-8 -*-
import scrapy


class AllmusicSpider(scrapy.Spider):
    name = "allmusic"
    allowed_domains = ["www.allmusic.com"]
    start_urls = ['http://www.allmusic.com/genres/']

    def parse(self, response):
        pass
