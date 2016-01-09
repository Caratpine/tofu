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


def filter_movie():
    movie_id = list()
    movie_list = list()
    movie_tag = list()
    with open('tag_list.json', 'rb') as f:
        tags = json.loads(f.read())

    for val in Movie_tags:
        with open('movies/movie_' + val + '.json', 'rb') as f:
            movie = json.loads(f.read())
            for m in movie:
                if m['id'] not in movie_id:
                    movie_id.append(m['id'])
                    tag = m['tags'].strip().split('/')
                    movie_list.append([m['id'], m['name'], m['star'], m['url']])
                    for t in tag:
                        tag_id = tags.index(t.strip()) + 1
                        movie_tag.append([m['id'], tag_id])

    print len(movie_id)

    with open('movie_list.json', 'wb') as f:
        f.write(json.dumps(movie_list))

    with open('movie_tag', 'wb') as f:
        f.write(json.dumps(movie_tag))



if __name__ == '__main__':
    filter_movie()
