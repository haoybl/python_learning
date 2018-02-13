# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from gumtree.items import GumtreeItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import datetime
import socket
from urllib.parse import urljoin


class ManualSpider(scrapy.Spider):
    '''
    creating contracts

    @url https://www.gumtree.com/p/property-to-rent/very-large-1-bedroom-flat-with-own-garden-plaistow-canning-town-e13/1281556866
    @returns items 1
    @scrapes address date description image_urls price project server spider title url
    '''
    name = 'manual'
    allowed_domains = ["gumtree.com"]
    base_url = 'https://www.gumtree.com'
    start_urls = [
         'https://www.gumtree.com/flats-houses/london',
         ]

    def parse(self, response):

        # get next page [horizontal crawl]
        next_page_selector = response.xpath('//*[contains(@data-analytics, "gaEvent:PaginationNext")]/@href')
        for url in next_page_selector.extract():
            #print('####{}####'.format(urljoin(self.base_url, url)))
            yield Request(urljoin(self.base_url, url))


        # get next item [vertical crawl]
        next_item_selector = response.xpath('//*[contains(@itemprop, "url")]/@href')
        for url in next_item_selector.extract():
            if url.startswith('/p'):
                #print('####{}####'.format(urljoin(self.base_url, url)))
                yield Request(urljoin(self.base_url, url),
                              callback=self.parse_item)

    def parse_item(self, response):

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