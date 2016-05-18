# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from doubanmoive.doubanmoiveItem import DoubanmoiveItem
from doubanmoive.movieCommnetItem import MovieCommentItem
from doubanmoive.movieReviewItem import MovieReviewItem

class DoubanmoivePipeline(object):
    def __init__(self):
        self.file = codecs.open('data.dat', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        item_type = type(item)
        if item_type is DoubanmoiveItem:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape"))
        elif item_type is MovieCommentItem:
            self.comment_file = codecs.open('./subjects/comments/' + item['movie_id'] + '_comments.dat', mode='ab+', encoding='utf-8')
            comment = json.dumps(dict(item)) + '\n'
            self.comment_file.write(comment.decode("unicode_escape"))
        elif item_type is MovieReviewItem:
            self.review_file = codecs.open('./subjects/reviews/' + item['movie_id'] + '_review.dat', mode='ab+', encoding='utf-8')
            line = json.dumps(dict(item)) + '\n'
            self.review_file.write(line.decode("unicode_escape"))
        return item
