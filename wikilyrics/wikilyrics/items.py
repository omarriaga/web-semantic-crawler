# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WikilyricsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArtistItem(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()


class SongItem(scrapy.Item):
    artist = scrapy.Field()
    name = scrapy.Field()
    urlYouTube = scrapy.Field()
    letra = scrapy.Field()
    album = scrapy.Field()
    musicBy = scrapy.Field()
    letraBy = scrapy.Field()


class GenreItem(scrapy.Item):
    name = scrapy.Field()
    stylisticOrigins = scrapy.Field()
    instrumentsUsed = scrapy.Field()
    description = scrapy.Field()


class AlbumItem(scrapy.Item):
    name = scrapy.Field()
    year = scrapy.Field()
    length = scrapy.Field()
    genre = scrapy.Field()
    urlWikipedia = scrapy.Field()
    imagen = scrapy.Field()


class RecoveryLabelItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    imagen = scrapy.Field()


class ArtistAlbumItem(scrapy.Item):
    artist = scrapy.Field()
    album = scrapy.Field()


class SongAlbumItem(scrapy.Item):
    song = scrapy.Field()
    album = scrapy.Field()


class ArtistGenreItem(scrapy.Item):
    artist = scrapy.Field()
    genre = scrapy.Field()


class RecoveryLabelArtistItem(scrapy.Item):
    recoveryLabel = scrapy.Field()
    artist = scrapy.Field()
