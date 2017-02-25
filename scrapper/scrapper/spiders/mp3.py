# -*- coding: utf-8 -*-
import scrapy
from pymaybe import maybe


class Mp3Spider(scrapy.Spider):
    name = "mp3"
    allowed_domains = ["mp3.com"]
    start_urls = ['http://mp3.com/artists/']

    def parse(self, response):
        for artist in response.css('ul.artist-list > li'):
            url = artist.css('a::attr(href)').extract_first()
            yield scrapy.Request(url, callback=self.parse_artist)

        next_page = response.css('a.next.button::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            next_page = response.css('div.filter_selection > span+a::attr(href)').extract_first()
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_artist(self, response):
        def extract_with_css(query):
            return maybe(response.css(query).extract_first()).strip()

        yield {
            'name': extract_with_css('div.box.artist.artist-page-padding-top > h1::text'),
            'genres': extract_with_css('div.artist-meta-info > div.tags::text'),
            'music': response.css('ol.top_tracks > li > a::text').extract(),
        }
