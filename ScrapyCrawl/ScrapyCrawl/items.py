# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapycrawlItem(scrapy.Item):
    # define the fields for your item here like:
    forum_title = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    crawl_date = scrapy.Field()
    comments = scrapy.Field()
    views = scrapy.Field()
    replies = scrapy.Field()
    avatar_details = scrapy.Field()

