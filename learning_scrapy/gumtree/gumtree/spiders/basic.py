# -*- coding: utf-8 -*-
import scrapy
from gumtree.items import GumtreeItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import datetime
import socket


class BasicSpider(scrapy.Spider):
    '''
    creating contracts

    @url https://www.gumtree.com/p/property-to-rent/very-large-1-bedroom-flat-with-own-garden-plaistow-canning-town-e13/1281556866
    @returns items 1
    @scrapes address date description image_urls price project server spider title url
    '''
    name = 'basic'
    allowed_domains = ['gumtree.com']
    start_urls = [
         'https://www.gumtree.com/p/property-to-rent/very-large-1-bedroom-flat-with-own-garden-plaistow-canning-town-e13/1281556866',
         ]

    def parse(self, response):

        # create the loader using the response
        l = ItemLoader(item=GumtreeItem(), response=response)

        # item value fields
        l.add_xpath('title', '//h1[@id="ad-title"]/text()',
                    MapCompose(str.strip, str.title))
        l.add_xpath('price', '//strong[starts-with(@class, "ad-price")]/text()',
                    MapCompose(lambda x: x.replace(',', ''), float), re='[.,0-9]+')
        l.add_xpath('address', '//span[@itemprop="address"]/text()',
                    MapCompose(str.strip))
        l.add_xpath('description','//p[@itemprop="description"]/text()',
                    MapCompose(str.strip), Join())
        l.add_xpath('image_urls', '//img[@itemprop="image"]/@src', TakeFirst())

        # item housekeeping values
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()