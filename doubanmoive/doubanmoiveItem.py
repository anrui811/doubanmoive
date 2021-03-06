# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DoubanmoiveItem(Item):
    # define the fields for your item here like:
    id = Field()
    name = Field()
    year = Field()
    score = Field()
    director = Field()
    classification = Field()
    actor = Field()
    desc = Field()
    comments = Field()
    reviews = Field()
    alias = Field()
    screenwriter = Field()
    initialReleaseDate = Field()
