# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import GenreItem
from pymaybe import maybe
import html2text


def extract_with_css(query, response):
    return maybe(response.css(query).extract_first()).strip()


class LyricallySpider(scrapy.Spider):
    name = "lyrically"
    domain = 'http://lyrics.wikia.com'
    allowed_domains = ["http://lyrics.wikia.com/"]
    start_urls = ['http://lyrics.wikia.com/wiki/Category:Genre']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        print("**llego***")
        for genre in response.css('div#mw-subcategories > div.mw-content-ltr > table > tr > td > ul > li'):
            genre_item = GenreItem()
            genre_item['name'] = \
                extract_with_css('a.CategoryTreeLabel.CategoryTreeLabelNs14.CategoryTreeLabelCategory::text', genre) \
                    .replace('Genre/', '')
            genre_url = \
                extract_with_css('a.CategoryTreeLabel.CategoryTreeLabelNs14.CategoryTreeLabelCategory::attr(href)',
                                 genre)
            yield Request(str(self.domain + genre_url), headers=self.headers, callback=self.parse_genre,
                          meta={'genre': genre_item})

        url_next = response.css('div.wikia-paginator > ul > li > a.paginator-next.button.secondary::attr(href)') \
            .extract_first()
        if url_next is not None:
            yield Request(url_next, headers=self.headers, callback=self.parse)

    def parse_genre(self, response):
        genre = response.meta['genre']
        genre['stylisticOrigins'] = extract_with_css('a.external.text::text', response)
        h = html2text.HTML2Text()
        h.ignore_links = True
        genre['description'] = h.handle(' '.join(response.css(
            'div.mw-content-ltr.mw-content-text > table tr:first-child td:last-child::text').extract()))
        yield genre
