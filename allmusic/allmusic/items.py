# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class AllmusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GenreItem(Item):
    name = Field()
    imagen = Field()
    descripcion = Field()


class GenreArtistItem(Item):
    genre = Field()
    artist = Field()


class AlbumGenreItem(Item):
    genre = Field()
    album = Field()


class SongGenreItem(Item):
    genre = Field()
    song = Field()


class ArtistItem(Item):
    name = Field()
    imagen = Field()
    bio = Field()
    born = Field()
    active = Field()


class AlbumItem(Item):
    name = Field()
    year = Field()
    artist = Field()


class SongItem(Item):
    name = Field()
    artist = Field()
    album = Field()
