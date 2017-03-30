# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pymaybe import maybe
import html2text
from ..items import GenreItem, GenreArtistItem, ArtistItem, AlbumItem, SongItem, AlbumGenreItem, SongGenreItem


def extract_with_css(query, response):
    return maybe(response.css(query).extract_first()).strip()


class AllmusicSpider(scrapy.Spider):
    name = "allmusic"
    domain = 'http://www.allmusic.com'
    allowed_domains = ["www.allmusic.com"]
    start_urls = ['http://www.allmusic.com/genres']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers)

    def parse(self, response):
        for genre in response.css('div.genres > div.genre'):
            genre_item = GenreItem()
            genre_item['imagen'] = self.domain + extract_with_css('a.genre-image > img::attr(src)', genre)
            url = genre.css('a.genre-image::attr(href)').extract_first()
            yield Request(url, headers=self.headers, callback=self.parse_genre, meta={'genre': genre_item})

    def parse_genre(self, response):
        genre = response.meta['genre']
        genre['name'] = extract_with_css('h1.genre-name.headline::text', response)
        genre['descripcion'] = extract_with_css('p.description::text', response)
        yield genre

        url_artist = self.domain + extract_with_css('ul.tabs > li.tab.artists > a::attr(href)', response)
        print('url_artist ' + str(url_artist) + ' type ' + type(url_artist).__name__)
        if url_artist is not None:
            yield Request(str(url_artist), headers=self.headers, callback=self.parse_genre_artist,
                          meta={'genre': genre['name']})

        url_albums = extract_with_css('ul.tabs > li.tab.albums > a::attr(href)', response)
        if url_albums is not None:
            yield Request(str(self.domain + url_albums), headers=self.headers, callback=self.parse_genre_album,
                          meta={'genre': genre['name']})

        url_songs = extract_with_css('ul.tabs > li.tab.songs > a::attr(href)', response)
        if url_songs is not None:
            yield Request(str(self.domain + url_songs), headers=self.headers, callback=self.parse_genre_song,
                          meta={'genre': genre['name']})

    def parse_genre_artist(self, response):
        genre = response.meta['genre']
        for artist in response.css('div.artist-highlights-container > div'):
            genre_artist = GenreArtistItem()
            genre_artist['genre'] = genre
            genre_artist['artist'] = extract_with_css('a > div.info > div.artist::text', artist)
            yield genre_artist
            # ir por el perfil de artista
            artist_item = ArtistItem()
            artist_item['name'] = genre_artist['artist']
            url = artist.css('a::attr(href)').extract_first()
            if url is not None:
                yield Request(str(self.domain + url), headers=self.headers, callback=self.parse_artist,
                              meta={'artist': artist_item})

    def parse_artist(self, response):
        artist = response.meta['artist']
        artist['born'] = response.css('div.sidebar > section.basic-info > div.birth > div::text').extract_first()
        artist['active'] = response.css(
            'div.sidebar > section.basic-info > div.active-dates > div::text').extract_first()
        for genre in response.css('div.sidebar > section.basic-info > div.genre > div > a'):
            genre_artist = GenreArtistItem()
            genre_artist['genre'] = extract_with_css('a::text', genre)
            genre_artist['artist'] = artist['name']
            yield genre_artist

        url_bio = extract_with_css('ul.tabs > li.tab.biography > a::attr(href)', response)
        try:
            yield Request(str(self.domain + url_bio), headers=self.headers, callback=self.get_bio, meta={'artist': artist})
        except:
            yield artist

        url_albums = extract_with_css('ul.tabs > li.tab.discography > a::attr(href)', response)
        if url_albums is not None:
            yield Request(str(self.domain + url_albums), headers=self.headers, callback=self.parse_album,
                          meta={'artist': artist['name']})

        url_songs = response.css('ul.tabs > li.tab.songs > a::attr(href)').extract_first()
        if url_songs is not None:
            yield Request(str(self.domain + url_songs + '/all'), headers=self.headers, callback=self.parse_song,
                          meta={'artist': artist['name']})

    def get_bio(self, response):
        artist = response.meta['artist']
        h = html2text.HTML2Text()
        h.ignore_links = True
        artist['bio'] = h.handle(' '.join(response.css('section.biography > div.text > p::text').extract()))
        yield artist

    def parse_album(self, response):
        artist = response.meta['artist']
        for album in response.css('section.discography > table > tbody > tr'):
            album_item = AlbumItem()
            album_item['artist'] = artist
            album_item['name'] = extract_with_css('td.title > a::text', album)
            album_item['year'] = extract_with_css('td.year::text', album)
            yield album_item

    def parse_song(self, response):
        artist = response.meta['artist']
        h = html2text.HTML2Text()
        h.ignore_links = True
        for song in response.css('section.all-songs > table > tbody > tr'):
            song_item = SongItem()
            song_item['artist'] = artist
            song_item['name'] = h.handle(' '.join(song.css('td.title-composer > div.title').extract())).strip()
            url_song = song.css('td.title-composer > div.title > a::attr(href)').extract_first()
            try:
                yield Request(url_song, headers=self.headers, callback=self.get_album, meta={'song': song_item})
            except:
                yield song_item

        url_next = response.css('section.all-songs > div.pagination > span.next > a::attr(href)').extract_first()
        try:
            yield Request(url_next, headers=self.headers, callback=self.parse_song,
                          meta={'artist': artist})
        except:
            print('no more next link')

    def get_album(self, response):
        song = response.meta['song']
        song['album'] = response.css(
            'section.appearances > table > tbody > tr > td.artist-album > div.title > a::text').extract_first()
        yield song

    def parse_genre_album(self, response):
        genre = response.meta['genre']
        for album in response.css('section.album-highlights > div.album-highlights-container > div'):
            album_genre = AlbumGenreItem()
            album_genre['genre'] = genre
            album_genre['album'] = extract_with_css('a > div.info > div.title::text', album)
            yield album_genre

    def parse_genre_song(self, response):
        genre = response.meta['genre']
        for song in response.css('section.song-highlights > table  tr td.title'):
            song_genre = SongGenreItem()
            song_genre['genre'] = genre
            song_genre['song'] = song.css('a::text').extract_first()
            yield song_genre
