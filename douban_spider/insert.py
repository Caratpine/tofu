#!usr/bin/env python
# coding=UTF-8

import db
import sys
import json
from tags import Movie_tags
from tag_list import tag_list

reload(sys)
sys.setdefaultencoding('utf-8')


def collect_tags():
    tag_list = list()
    for val in Movie_tags:
        with open('movies/movie_' + val + '.json', 'rb') as f:
            movie = json.loads(f.read())
            for m in movie:
                t = m['tags'].split('/')
                for v in t:
                    tag = v.strip()
                    if tag not in tag_list:
                        tag_list.append(tag)

    with open('tag_list.py', 'wb') as f:
        f.write(json.dumps(tag_list))


def insert_tag():
    with open('tag_list.json', 'rb') as f:
        tags = json.loads(f.read())

    tag_list = list()
    for val in tags:
        tag_tuple = (val, )
        tag_list.append(tag_tuple)

    db.insert_tags(tag_list)


if __name__ == '__main__':
    insert_tag()