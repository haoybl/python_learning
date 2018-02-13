# -*- coding: utf-8 -*-
import scrapy


class RedditbotSpider(scrapy.Spider):
    name = 'redditbot'
    allowed_domains = ['www.reddit.com/r/gameofthrones/']
    start_urls = ['http://www.reddit.com/r/gameofthrones//']

    def parse(self, response):

        # extract each fields [list]
        titles = response.xpath('//p[@class="title"]/a/text()').extract()
        votes = response.xpath('//div[@class="score unvoted"]/@title').extract()
        comments = response.xpath('//a[@data-event-action="comments"]/text()').extract()
        dates = response.xpath('//time[@class="live-timestamp"]/@title').extract()

        for title, vote, num_comment, date in zip(titles, votes, comments, dates):

            scrape_info = {
                'title':title,
                'vote': vote,
                'comment':num_comment,
                'date':date,
            }

            yield scrape_info



