# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest


class BricksetSpider(scrapy.Spider):
    name = 'brickset_spider'
    allowed_domains = ['brickset.com']
    start_urls = ['https://brickset.com/sets/category-Normal']

    def parse(self, response):

        brickset_path = "//article[@class='set']"

        for brickset in response.xpath(brickset_path):

            name_selector = './/h1/a//text()'
            img_selector = './a/img/@src'
            col_name_selector = ".//dt/text()"
            col_val_selector = './/dd/text()'

            table_data = dict(zip(brickset.xpath(col_name_selector).extract(),
                                  brickset.xpath(col_val_selector).extract()))
            # item yield
            yield {
                'name': "".join(brickset.xpath(name_selector).extract()),
                'image': brickset.xpath(img_selector).extract_first(),
                'pieces': table_data.get('Pieces'),
            }

        # go to the next page (recursively)
        next_page_url = brickset.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url:
            yield Request(
                url=next_page_url,
                callback=self.parse)



#/html/body/div[2]/div/div/section/article[6]/div[2]/div[3]/dl/dd[1]