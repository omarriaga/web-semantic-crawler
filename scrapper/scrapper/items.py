# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArtistItem(scrapy.Item):
    name = scrapy.Field()
    bio = scrapy.Field()


class SongItem(scrapy.Item):
    artist = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class GenreItem(scrapy.Item):
    artist = scrapy.Field()
    genre = scrapy.Field()