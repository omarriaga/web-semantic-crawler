# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pymaybe import maybe
from ..items import GenreItem, GenreArtistItem


def extract_with_css(query, response):
    return maybe(response.css(query).extract_first()).strip()


class AllmusicSpider(scrapy.Spider):
    name = "allmusic"
    allowed_domains = ["www.allmusic.com"]
    start_urls = ['http://www.allmusic.com/genres']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        for genre in response.css('div.genres > div.genre'):
            genre_item = GenreItem()
            genre_item['imagen'] = extract_with_css('a.genre-image > img::attr(src)', genre)
            url = genre.css('a.genre-image::attr(href)').extract_first()
            yield Request(url, headers=self.headers, callback=self.parse_genre, meta={'genre': genre_item})

    def parse_genre(self, response):
        genre = response.meta['genre']
        genre['name'] = extract_with_css('h1.genre-name.headline::text', response)
        genre['descripcion'] = extract_with_css('p.description::text', response)
        yield genre
