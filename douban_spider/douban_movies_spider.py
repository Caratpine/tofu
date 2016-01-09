#!usr/bin/env python
# coding=UTF-8
"""
    @author: corazon(Peibo Xu)
    @date: 2015-12-30
    @desc:
        crawl all douban movies by tags
"""
import requests
import json
import re
import sys
import time
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool
from tags import Movie_task_tags

reload(sys)
sys.setdefaultencoding('utf-8')


class DoubanMovieSpider(object):
    def __init__(self):
        self.s = requests.Session()
        self.header = {
            'Host': 'www.douban.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKi \
                    t/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Cache-Control': 'max-age=0',
        }

    def crawl_page(self, url):
        r = self.s.get(url, headers=self.header)
        if r.status_code == 200:
            return r.text
        else:
            return 'NULL'

    def parse_page(self, page):
        if page == 'NULL':
            return 'NULL'
        try:
            pattern = re.compile(r'<div class="mod movie-list">(.*)</div>.*?<div class="paginator">', re.S)
            content = pattern.findall(page)[0]
            mod_movie_list = html.fromstring(content.decode('utf-8'))
        except Exception, e:
            print "page error: %s" % str(e)
            return 'NULL'

        movie_list = list()
        for dl in mod_movie_list:
            movie = dict(id="NULL", tags="NULL", star=-1, name="NULL", url="NULL")

            try:
                movie['name'] = dl.xpath('.//a[@class="title"]/text()')[0].strip()
            except Exception, e:
                movie['name'] = 'NULL'

            try:
                title_url = dl.xpath('.//a[@class="title"]/@href')[0].strip()
                movie['id'] = filter(str.isdigit, title_url)
            except Exception, e:
                movie['id'] = 'NULL'

            try:
                movie['tags'] = dl.xpath('.//div[@class="desc"]/text()')[0].strip()
            except Exception, e:
                movie['tags'] = 'NULL'

            try:
                movie['star'] = float(dl.xpath('.//span[@class="rating_nums"]/text()')[0].strip())
            except Exception, e:
                movie['star'] = -1

            try:
                movie['url'] = dl.xpath('.//img/@src')[0].strip()
            except Exception, e:
                movie['url'] = 'NULL'

            movie_list.append(movie)

        return movie_list

    def single_task(self, url):
        page = self.crawl_page(url)

        result_movie_list = self.parse_page(page)
        if result_movie_list != 'NULL' and result_movie_list != []:
            print "%s is crawl ok!" % url
            time.sleep(2)
            return result_movie_list
        else:
            print "%s is crawl wrong!" % url
            with open('error_task.json', 'a+') as f:
                f.write(url + '\n')
            time.sleep(2)
            return 'NULL'

    def multi_crawl(self, tag):
        urls = list()

        url = 'http://www.douban.com/tag/' + tag + '/movie'
        for i in range(1, 35):
            newpage = url + '?start=' + str((i-1) * 15)
            urls.append(newpage)

        pool = ThreadPool(2)
        results = pool.map(self.single_task, urls)
        pool.close()
        pool.join()
        movie_list = [item for sublist in results if sublist != 'NULL' for item in sublist]

        movie_file_list = sorted(movie_list, key=lambda k: k['star'], reverse=True)

        with open('movies/' + 'movie_' + str(tag) + '.json', 'wb') as f:
            f.write(json.dumps(movie_file_list).decode('utf-8'))


if __name__ == '__main__':
    spider = DoubanMovieSpider()
    for v in Movie_task_tags:
        spider.multi_crawl(v)
        time.sleep(5)


