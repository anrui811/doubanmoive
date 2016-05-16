# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from doubanmoive.doubanmoiveItem import DoubanmoiveItem
from doubanmoive.movieCommnetItem import MovieCommentItem
from scrapy.http import Request
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


class MoiveSpider(CrawlSpider):
    name = "doubanmovie"
    allowed_domains = ["movie.douban.com"]
    # 华语
    start_urls = ["https://movie.douban.com/tag/%E5%8D%8E%E8%AF%AD"]
    rules = [
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/tag/%E5%8D%8E%E8%AF%AD?.*'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')), callback="parse_item"),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/comments?.*')), callback="get_comments"),
    ]

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanmoiveItem()
        self.get_id(response, item)
        self.get_name(sel, item)
        self.get_year(sel, item)
        self.get_score(sel, item)
        self.get_director(sel, item)
        self.get_classification(sel, item)
        self.get_actor(sel, item)
        self.get_desc(sel, item)
        self.get_comment_url(sel, item)
        self.crawl_comment(sel, item)
        return item

    def get_id(self, response, item):
        page_link = response._url
        pattern = re.compile(r'\d+')
        item['id'] = pattern.findall(page_link)

    def get_name(self, response, item):
        name = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['name'] = name

    def get_year(self, response, item):
        year = response.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['year'] = year

    def get_score(self, response, item):
        score = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['score'] = score

    def get_director(self, response, item):
        director = response.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['director'] = director

    def get_classification(self, response, item):
        classification = response.xpath('//span[@property="v:genre"]/text()').extract()
        item['classification'] = classification

    def get_actor(self, response, item):
        if response.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract():
            actor = response.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract()
        elif response.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract() \
                and response.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract()[0] == unicode('主演'):
            actor = response.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        else:
            actor = []
        item['actor'] = actor

    def get_desc(self, response, item):
        desc = response.xpath('//*[@id="link-report"]/span[1]/text()').extract()
        item['desc'] = desc

    def crawl_comment(self, response, item):
        request = Request('https://movie.douban.com/subject/' + str(item['id'][0]) + "/comments?.*", callback="get_comments")
        print request

    def get_comments(self, response):
        commentItem = MovieCommentItem()
        res = Selector(response)
        commentItem['name'] = res.xpath('//*[@id="comments"]/div[1]/div[2]/h3/span[2]/a/text()').extract()
        return commentItem

    def get_comment_url(self, response, item):
        comment_url = 'https://movie.douban.com/subject/' + str(item['id'][0]) + "/comments?.*"
        # item['name'] = name
        print comment_url