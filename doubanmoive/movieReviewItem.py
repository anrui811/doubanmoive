# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MovieReviewItem(Item):
    # define the fields for your item here like:
    movie_id = Field()
    speaker_id = Field()
    speaker_name = Field()
    title = Field()
    score = Field()
    date = Field()
    useful_num = Field()
    useless_num = Field()
    content = Field()
    comments = Field()
