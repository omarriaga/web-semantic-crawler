# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import AlbumItem, ArtistItem, SongItem
from pymaybe import maybe
import html2text


def extract_with_css(query, response):
    return maybe(response.css(query).extract_first()).strip()


class AlbumSpider(scrapy.Spider):
    name = "album"
    domain = 'http://lyrics.wikia.com'
    start_urls = ['http://lyrics.wikia.com/wiki/Category:Albums_by_Artist']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def parse(self, response):
        for artist_dom in response.css('div#mw-subcategories > div.mw-content-ltr > table > tr > td > ul > li'):
            artist = ArtistItem()
            artist['name'] = \
                extract_with_css('a.CategoryTreeLabel.CategoryTreeLabelNs14.CategoryTreeLabelCategory::text',
                                 artist_dom).replace('Albums by', '')
            artist_url = \
                extract_with_css('a.CategoryTreeLabel.CategoryTreeLabelNs14.CategoryTreeLabelCategory::attr(href)',
                                 artist_dom)
            yield Request(str(self.domain + artist_url), headers=self.headers, callback=self.parse_artist,
                          meta={'artist': artist})

        url_next = response.css('div.wikia-paginator > ul > li > a.paginator-next.button.secondary::attr(href)') \
            .extract_first()
        if url_next is not None:
            yield Request(url_next, headers=self.headers, callback=self.parse)

    def parse_artist(self, response):
        artist = response.meta['artist']
        yield artist
        for albums in response.css('div#mw-pages div.mw-content-ltr ul li'):
            album_url = extract_with_css('a::attr(href)', albums)
            print(album_url)
            yield Request(str(self.domain + album_url), headers=self.headers, callback=self.parse_albums,
                          meta={'artist': artist})

    def parse_albums(self, response):
        artist = response.meta['artist']
        album = AlbumItem()
        album['artist'] = artist['name']
        album['name'] = extract_with_css('div.plainlinks > div:first-child b::text', response)
        album['year'] = extract_with_css('div.plainlinks > table:nth-child(1n) tr td:last-child::text',
                                         response)
        album['length'] = extract_with_css('div.plainlinks > table:nth-child(2n) tr td:last-child::text',
                                           response)
        yield album
        for songs in response.css('div#mw-content-text > ol > li'):
            song = SongItem()
            song['artist'] = artist['name']
            song['name'] = extract_with_css('b > a::text', songs)
            song['album'] = album['name']
            url_song = songs.css('b > a::attr(href)').extract_first()
            if url_song is not None:
                yield Request(str(self.domain + url_song), headers=self.headers, callback=self.parse_song,
                              meta={'song': song})
            else:
                yield song

    def parse_song(self, response):
        song = response.meta['song']
        h = html2text.HTML2Text()
        h.ignore_links = True
        song['letra'] = h.handle(' '.join(response.css('div.lyricbox::text').extract()))
        song['musicBy'] = \
            h.handle(' '.join(response.css('table.song-credit-box tr:first-child td:last-child::text').extract()))
        song['letraBy'] = \
            h.handle(' '.join(response.css('table.song-credit-box tr:nth-child(2n) td:last-child::text').extract()))
        yield song