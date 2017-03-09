# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class AllmusicPipeline(object):
    def process_item(self, item, spider):
        return item

def item_type(item):
    return type(item).__name__.replace('Item', '').lower()  # TeamItem => team


CSVDir = '/Users/juan/dumps/'


class MultiCSVItemPipeline(object):
    SaveTypes = ['artist', 'song', 'genre']

    def __init__(self):
        self.files = dict([(name, open(CSVDir + name + '.csv', 'w+b')) for name in self.SaveTypes])
        self.exporters = dict([(name, CsvItemExporter(self.files[name], True, ';', delimiter=';')) for name in self.SaveTypes])
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item
