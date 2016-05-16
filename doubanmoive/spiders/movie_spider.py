# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from doubanmoive.items import DoubanmoiveItem
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
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/comments')), callback="set_comments")
    ]

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanmoiveItem()
        page_link = response._url
        pattern = re.compile(r'\d+')
        item['id'] = pattern.findall(page_link)
        # item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        self.get_name(sel, item)
        item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        if sel.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract():
            item['actor'] = sel.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract()
        elif sel.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract() \
                and sel.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract()[0] == unicode('主演'):
            item['actor'] = sel.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        else:
            item['actor'] = []
        item['desc'] = sel.xpath('//*[@id="link-report"]/span[1]/text()').extract()
        return item

    def get_name(self, response, item):
        name = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['name'] = name
