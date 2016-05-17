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
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/$')), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/comments$')), callback="parse_comments", follow=True),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/comments\?start=[1-9]+&limit=20&sort=new_score$')),callback="parse_comments", follow=True)
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
        # self.get_comment_url(sel, item)
        # self.crawl_comment(sel, item)
        return item

    def get_id(self, response, item):
        page_link = response._url
        pattern = re.compile(r'\d+')
        item['id'] = pattern.findall(page_link)

    def get_name(self, selector, item):
        name = selector.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['name'] = name

    def get_year(self, selector, item):
        year = selector.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['year'] = year

    def get_score(self, selector, item):
        score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['score'] = score

    def get_director(self, selector, item):
        director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['director'] = director

    def get_classification(self, selector, item):
        classification = selector.xpath('//span[@property="v:genre"]/text()').extract()
        item['classification'] = classification

    def get_actor(self, selector, item):
        if selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract():
            actor = selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract()
        elif selector.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract() \
                and selector.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract()[0] == unicode('主演'):
            actor = selector.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        else:
            actor = []
        item['actor'] = actor

    def get_desc(self, selector, item):
        desc = selector.xpath('//*[@id="link-report"]/span[1]/text()').extract()
        item['desc'] = desc

    def parse_comments(self, response):
        commentItem = MovieCommentItem()
        sel = Selector(response)
        commentItem['name'] = sel.xpath('//*[@id="comments"]/div[1]/div[2]/h3/span[2]/a/text()').extract()
        return commentItem