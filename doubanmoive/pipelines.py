# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import types


class DoubanmoivePipeline(object):
    def __init__(self):
        self.file = codecs.open('data.dat', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        mydict = {}
        mydict.update({'name': item['name'][0], 'score': item['score'], 'classification': item['classification'],
                       'director': item['director'], 'actor': item['actor'], 'year': item['year']})
        line = json.dumps(mydict) + '\n'
        self.file.write(line.decode("unicode_escape"))
        self.subject_file = codecs.open('./subjects/' + item['id'][0] + '.dat', mode='wb', encoding='utf-8')
        subject = {}
        subject.update({'name': item['name'][0], 'desc': item['desc']})
        sub_line = json.dumps(subject) + '\n'
        self.subject_file.write(sub_line.decode("unicode_escape"))
        return item
