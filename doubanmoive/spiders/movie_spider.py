# -*- coding: utf-8 -*-
import urllib

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from doubanmoive.doubanmoiveItem import DoubanmoiveItem
from doubanmoive.movieCommnetItem import MovieCommentItem
from doubanmoive.movieReviewItem import MovieReviewItem
from scrapy.http import Request, FormRequest

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


class MoiveSpider(CrawlSpider):
    name = "doubanmovie"
    allowed_domains = ["movie.douban.com"]
    # 华语
    # start_urls = ["https://movie.douban.com/tag/%E7%BE%8E%E5%9B%BD", "https://movie.douban.com/tag/%E6%97%A5%E6%9C%AC",
    #               "https://movie.douban.com/tag/%E9%A6%99%E6%B8%AF", "https://movie.douban.com/tag/%E8%8B%B1%E5%9B%BD",
    #               "https://movie.douban.com/tag/%E4%B8%AD%E5%9B%BD", "https://movie.douban.com/tag/%E6%B3%95%E5%9B%BD",
    #               "https://movie.douban.com/tag/%E9%9F%A9%E5%9B%BD", "https://movie.douban.com/tag/%E5%8F%B0%E6%B9%BE",
    #               "https://movie.douban.com/tag/%E5%BE%B7%E5%9B%BD", "https://movie.douban.com/tag/%E6%84%8F%E5%A4%A7%E5%88%A9",
    #               "https://movie.douban.com/tag/%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86", "https://movie.douban.com/tag/%E5%8D%B0%E5%BA%A6",
    #               "https://movie.douban.com/tag/%E5%86%85%E5%9C%B0", "https://movie.douban.com/tag/%E6%B3%B0%E5%9B%BD",
    #               "https://movie.douban.com/tag/%E8%A5%BF%E7%8F%AD%E7%89%99", "https://movie.douban.com/tag/%E6%AC%A7%E6%B4%B2"]
    start_urls = ["https://movie.douban.com/tag/%E7%BE%8E%E5%9B%BD"]

    rules = [
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/tag/%E7%BE%8E%E5%9B%BD?.*'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/$')), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/reviews$'))),
        Rule(LinkExtractor(
            allow=(r'https://movie.douban.com/subject/\d+/reviews\?start=[1-9][0-9]*\&filter=\&limit=20'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/review/\d+/$')), callback="parse_review"),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/comments$')), callback="parse_comments",
             follow=True),
        Rule(LinkExtractor(
            allow=(r'https://movie.douban.com/subject/\d+/comments\?start=[1-9][0-9]*\&limit=20\&sort=new_score$')),
             callback="parse_comments", follow=True)
    ]

    def __init__(self):
        super(MoiveSpider, self).__init__()
        self.http_user = '877279443@qq.com'
        self.http_pass = 'AR12345678'
        self.formdata = {"redir": "https://movie.douban.com/tag/%E7%BE%8E%E5%9B%BD",
                         "form_email": '877279443@qq.com',
                         "form_password": 'AR12345678',
                         "login": u'登录'
                         }
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Connection': 'keep-alive'
                        }

    def start_requests(self):
        yield Request('https://www.douban.com/accounts/login',
                      meta={'cookiejar': 1},
                      headers=self.headers,
                      callback=self.post_login
                      )

    def post_login(self, response):
        print 'Preparing login'
        self.get_captcha(response)
        return FormRequest.from_response(response,
                                         headers=self.headers,
                                         formdata=self.formdata,
                                         callback=self.after_login,
                                         dont_filter=True)

    def get_captcha(self, response):
        print 'get_captcha'
        page = response.text
        soup = BeautifulSoup(page, "html.parser")
        captchaAddr = soup.find('img', id='captcha_image')['src']

        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captchaID = re.findall(reCaptchaID, page)

        urllib.urlretrieve(captchaAddr, "captcha.jpg")
        captcha = raw_input('please input the captcha:')

        self.formdata['captcha-solution'] = captcha
        self.formdata['captcha-id'] = captchaID

    def after_login(self, response):
        print 'after_login'
        print response.url
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanmoiveItem()
        self.get_movie_id(response, item)
        self.get_movie_name(sel, item)
        self.get_movie_year(sel, item)
        self.get_movie_score(sel, item)
        self.get_movie_director(sel, item)
        self.get_movie_classification(sel, item)
        self.get_movie_actor(sel, item)
        self.get_movie_desc(sel, item)
        return item

    def get_movie_id(self, response, item):
        page_link = response._url
        pattern = re.compile(r'\d+')
        item['id'] = pattern.findall(page_link)[0]

    def get_movie_name(self, selector, item):
        name = selector.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        item['name'] = name

    def get_movie_year(self, selector, item):
        year = selector.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')[0]
        item['year'] = year

    def get_movie_score(self, selector, item):
        if selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract():
            score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()[0]
        else:
            score = ""
        item['score'] = score

    def get_movie_director(self, selector, item):
        director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['director'] = director

    def get_movie_classification(self, selector, item):
        classification = selector.xpath('//span[@property="v:genre"]/text()').extract()
        item['classification'] = classification

    def get_movie_actor(self, selector, item):
        if selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract():
            actor = selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract()
        elif selector.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract() \
                and selector.xpath('//*[@id="info"]/span[2]/span[1]/text()').extract()[0] == unicode('主演'):
            actor = selector.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        else:
            actor = []
        item['actor'] = actor

    def get_movie_desc(self, selector, item):
        desc = selector.xpath('//*[@id="link-report"]/span[1]/text()').extract()[0]
        item['desc'] = desc

    def parse_comments(self, response):
        sel = Selector(response)
        url = response._url
        movie_id = url.split('/')[-2]
        commentItems = sel.xpath('//*[@class="comment-item"]').extract()
        comments = []
        for commentItem in commentItems:
            item = MovieCommentItem()
            item['movie_id'] = movie_id
            item['speaker_id'] = \
            Selector(text=commentItem).xpath('//*[@class="comment-info"]/a/@href').extract()[0].split('/')[-2]
            item['speaker_name'] = Selector(text=commentItem).xpath('//*[@class="comment-info"]/a/text()').extract()[0]
            score_class = Selector(text=commentItem).xpath('//*[@class="comment-info"]/span[1]/@class').extract()[0]
            pattern = re.compile(r'\d+')
            if pattern.findall(score_class):
                item['score'] = pattern.findall(score_class)[0]
            if Selector(text=commentItem).xpath('//*[@class="comment"]/p/text()').extract():
                item['content'] = Selector(text=commentItem).xpath('//*[@class="comment"]/p/text()').extract()[
                    0].strip()
            if Selector(text=commentItem).xpath('//*[@class="comment-info"]/span[2]/text()').extract():
                item['date'] = Selector(text=commentItem).xpath('//*[@class="comment-info"]/span[2]/text()').extract()[
                    0].strip()
            if Selector(text=commentItem).xpath('//*[@class="comment-vote"]/span/text()').extract():
                item['useful_num'] = \
                Selector(text=commentItem).xpath('//*[@class="comment-vote"]/span/text()').extract()[0]
            comments.append(item)
        return comments

    def parse_review(self, response):
        item = MovieReviewItem()
        sel = Selector(response)
        item['movie_id'] = sel.xpath('//*[@id="fixedInfo"]/div[1]/a/@href').extract()[0].split('/')[-2]
        item['speaker_id'] = \
        sel.xpath('//*[@id="content"]/div/div[1]/div/div/div[1]/p[1]/a[2]/@href').extract()[0].split('/')[-2]
        item['speaker_name'] = sel.xpath('//*[@property="v:reviewer"]/text()').extract()[0]
        item['title'] = sel.xpath('//*[@id="content"]/h1/span/text()').extract()[0]
        item['score'] = sel.xpath('//*[@property="v:rating"]/text()').extract()[0]
        item['date'] = sel.xpath('//*[@property="v:dtreviewed"]/text()').extract()[0]
        if sel.xpath('//*[@class="main-panel-useful"]/span[1]/em/text()').extract():
            item['useful_num'] = sel.xpath('//*[@class="main-panel-useful"]/span[1]/em/text()').extract()[0]
        else:
            item['useful_num'] = 0
        if sel.xpath('//*[@class="main-panel-useful"]/span[2]/em/text()').extract():
            item['useless_num'] = sel.xpath('//*[@class="main-panel-useful"]/span[2]/em/text()').extract()[0]
        else:
            item['useless_num'] = 0
        item['content'] = sel.xpath('//*[@id="link-report"]/div/text()').extract()
        return item
