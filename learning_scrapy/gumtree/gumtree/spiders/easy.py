# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from gumtree.items import GumtreeItem
import socket
import datetime
from urllib.parse import urljoin

base_url = 'https://gumtree.com'


class EasySpider(CrawlSpider):
    name = 'easy'
    allowed_domains = ['gumtree.com']
    start_urls = ['https://www.gumtree.com/flats-houses/london']

    rules = (
        # horizontal crawl
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@data-analytics, "gaEvent:PaginationNext")]',
                           process_value=lambda x: urljoin(base_url, x)), follow=True),
        # vertical crawl
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@itemprop, "url")]',
                           process_value=lambda x: urljoin(base_url, x)),
                            callback='parse_item', follow=True)
    )

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
        l.add_xpath('description', '//p[@itemprop="description"]/text()',
                    MapCompose(str.strip), Join())
        l.add_xpath('image_urls', '//img[@itemprop="image"]/@src', TakeFirst())

        # item housekeeping values
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
