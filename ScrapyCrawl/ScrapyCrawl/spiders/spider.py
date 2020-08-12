# -*- coding: utf-8 -*-
"""
In this module, you can find the OnionSpider class.
It's a spider to crawl the tor network.
"""
import scrapy
from scrapy import Request
from ..items import ScrapycrawlItem
import datetime
import reg as regex


class Spider(scrapy.Spider):
    base_url = 'http://avengersdutyk3xf.onion/'
    name = 'crawler'
    allowed_domains = ['onion']
    start_urls = [
        'http://avengersdutyk3xf.onion/index.php',
        'http://avengersdutyk3xf.onion/forum-5.html'
    ]
    items = ScrapycrawlItem()

    avatar_details = dict()
    avatar_details['avatar_name'] = 'Dwider'
    avatar_details['avatar_pass'] = 'qwerty123'
    avatar_details['avatar_email'] = 'Dwider@mail.com'
    avatar_details['avatar_user'] = 'Admin'

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return scrapy.FormRequest.from_response(response,
                                                self.start_urls[0],
                                                callback=self.forward_url,
                                                formdata={'my_post_key': token,
                                                          'username': self.avatar_details['avatar_name'],
                                                          'password': self.avatar_details['avatar_pass']})

    def forward_url(self, response):
        all_forums_url = self.start_urls[1]
        yield Request(all_forums_url, callback=self.crawl_forum)

    # add all forums to DB
    def crawl_forum(self, response):
        for href in response.css('table.tborder a::attr(href)').extract():
            if str(href).__contains__('forum'):
                yield Request(url=self.base_url + str(href), callback=self.start_crawl_posts)

    def start_crawl_posts(self, response):
        inlinerow_posts = response.xpath('.//tr[@class="inline_row"]')
        crawl_date = datetime.datetime.now().strftime('%d-%m-%y')
        forum_title = response.xpath('.//td[@class="thead"]/div/strong/text()').get()

        for tr_posts in inlinerow_posts:
            try:
                title = tr_posts.xpath('.//span[@class=" subject_old"]/a/text()').get()
                if title is None:
                    title = tr_posts.xpath('.//span[@class=" subject_new"]/a/text()').get()

                link = tr_posts.xpath('.//span[@class=" subject_old"]//@href').get()

                if link is not None:
                    replies = tr_posts.xpath('.//td[contains(@class,"forumdisplay_regular")]/a/text()').get()
                    views = tr_posts.xpath('.//*[contains(@class,"forumdisplay_regular")]')[4].xpath('.//text()').get()
                    comments_list = list()

                    yield Request(url=self.base_url + link,
                                  callback=self.comment_crawler,
                                  meta={'forum_title': forum_title,
                                        'title': title,
                                        'link': self.base_url+link,
                                        'crawl_date': crawl_date,
                                        'replies': replies,
                                        'views': views,
                                        'comments_list': comments_list})
            except:
                pass

        pagination = response.xpath('//div[@class="pagination"]')
        pages = pagination.xpath('.//a[@class="pagination_next"]')

        if pages.get() is not None:
            next_href_page = self.base_url + pages.xpath('@href').get()
            yield Request(url=next_href_page, callback=self.start_crawl_posts, meta=response.meta)

    def comment_crawler(self, response):
        posts = response.xpath('//div[@class="post "]')
        comments_list = response.meta.get('comments_list')
        urls = set()
        emails = set()
        bitcoins_address = set()

        for comment in posts:
            author_link = comment.css('span.largetext a::attr(href)').get()
            author_name = comment.css('span.largetext a::text').get()
            author_name_temp = comment.css('span.largetext a')
            if author_name is None:
                author_name = author_name_temp.xpath('.//span[contains(@style,"color")]//text()').get()

            comment_date = comment.xpath('.//div[2]/div[1]/span//text()').get()
            if not str(comment_date).__contains__("-"):
                comment_date = comment.xpath('.//span[@class="post_date"]//@title').get()

            # if user is a guest
            try:
                posts_count = comment.xpath('.//div[1]/div[3]//text()')[1].get().split(':')[1].strip()
                author_joined = comment.xpath('.//div[1]/div[3]//text()')[3].get().split(':')[1].strip()
                author_joined = datetime.datetime.strptime("1 " + author_joined, '%d %b %Y').strftime("%d-%m-%y")
            except:
                posts_count = 0
                author_joined = comment_date

            comment_body = ' '.join(comment.xpath('.//div[contains(@id, "pid_")]//text()').getall())
            urls.update(regex.url(comment_body))
            bitcoins_address.update(regex.bitcoin(comment_body))
            emails.update(regex.email(comment_body))

            user_details = dict()
            user_details['user_link'] = author_link
            user_details['user_name'] = author_name
            user_details['posts_count'] = posts_count
            user_details['comment_date'] = comment_date
            user_details['comment_body'] = comment_body
            user_details['joined_date'] = author_joined
            if len(urls) is 0:
                user_details['urls_regex'] = list()
            else:
                user_details['urls_regex'] = list(urls)
            if len(bitcoins_address) is 0:
                user_details['bitcoin_regex'] = list()
            else:
                user_details['bitcoin_regex'] = list(bitcoins_address)
            if len(emails) is 0:
                user_details['emails_regex'] = list()
            else:
                user_details['emails_regex'] = list(emails)

            comments_list.append(user_details)

        pagination = response.xpath('//div[@class="pagination"]')
        pages = pagination.xpath('.//a[@class="pagination_next"]')

        if pages.get() is not None:
            next_href_page = self.base_url + pages.xpath('@href').get()
            yield Request(url=next_href_page, callback=self.comment_crawler, meta=response.meta)

        else:
            self.items['comments'] = comments_list
            self.items['forum_title'] = response.meta.get('forum_title')
            self.items['title'] = response.meta.get('title')
            self.items['link'] = response.meta.get('link')
            self.items['crawl_date'] = response.meta.get('crawl_date')
            self.items['replies'] = response.meta.get('replies')
            self.items['views'] = response.meta.get('views')
            self.items['avatar_details'] = self.avatar_details

            yield self.items

