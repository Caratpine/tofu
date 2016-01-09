#!usr/bin/env python
# coding=UTF-8

import sys
import re
import requests
import json
from lxml import html

reload(sys)
sys.setdefaultencoding('utf-8')


def crawl_book_tags():
    url = 'http://book.douban.com/tag/?icn=index-nav'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'book.douban.com',
        'Referer': 'http://book.douban.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    }

    r = requests.get(url, headers=headers)
    return r.text


def parse_page(page):
    pattern = re.compile(r'<div class="article">(.*)</div>.*?<div class="aside">', re.S)
    try:
        result = pattern.findall(page)[0].strip()

        dom = html.fromstring(result.decode('utf-8'))
        tags = dom[1]

        tag_dict = dict()
        for div in tags:
            tag_title = div.xpath('.//a[@class="tag-title-wrapper"]/@name')[0].strip()
            tbody = div.xpath('.//tbody')[0]
            tag_list = list()
            for tr in tbody:
                tag = tr.xpath('.//a/text()')
                tag_list.extend(tag)
            tag_dict[tag_title] = tag_list

        with open('index.html', 'wb') as f:
            f.write(json.dumps(tag_dict))

    except Exception, e:
        print 'ERROR'


if __name__ == '__main__':
    page = crawl_book_tags()
    parse_page(page)