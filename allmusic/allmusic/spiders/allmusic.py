# -*- coding: utf-8 -*-
import scrapy


class AllmusicSpider(scrapy.Spider):
    name = "allmusic"
    allowed_domains = ["http://www.allmusic.com/genres"]
    start_urls = ['http://http://www.allmusic.com/genres/']

    def parse(self, response):
        pass
