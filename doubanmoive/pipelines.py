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
        self.comment_file_dict = {}
        self.review_file_dict = {}

    def process_item(self, item, spider):
        item_type = type(item)
        if item_type is DoubanmoiveItem:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape"))
        elif item_type is MovieCommentItem:
            filename = item['movie_id'] + '_comments.dat'
            if filename not in self.comment_file_dict.keys():
                self.comment_file = codecs.open('./subjects/comments/' + filename, mode='wb', encoding='utf-8')
                self.comment_file_dict[filename] = self.comment_file
            else:
                self.comment_file = self.comment_file_dict[filename]
            comment = json.dumps(dict(item)) + '\n'
            self.comment_file.write(comment.decode("unicode_escape"))
        elif item_type is MovieReviewItem:
            filename = item['movie_id'] + '_review.dat'
            if filename not in self.review_file_dict.keys():
                self.review_file = codecs.open('./subjects/reviews/' + filename, mode='wb', encoding='utf-8')
                self.review_file_dict[filename] = self.review_file
            else:
                self.review_file = self.review_file_dict[filename]
            line = json.dumps(dict(item)) + '\n'
            self.review_file.write(line.decode("unicode_escape"))
        return item
