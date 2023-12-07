# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstacraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class FollowData(scrapy.Item):
    followers = scrapy.Field()
    following = scrapy.Field()