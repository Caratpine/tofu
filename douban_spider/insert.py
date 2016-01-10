#!usr/bin/env python
# coding=UTF-8
"""
    @author: Corazon(Peibo Xu)
    @date: 2016-01-09
    @desc:
        insert movies data
"""

import db
import sys
import json
from tags import Movie_tags
import MySQLdb

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

def insert_movie():
    with open('movie_list.json', 'rb') as f:
        movie = json.loads(f.read())

    movie_list = list()
    for val in movie:
        id = val[0]
        name = val[1]
        star = '%.1f' % val[2]
        url = val[3]
        movie_tuple = (id, name, star, url)
        print movie_tuple
        movie_list.append(movie_tuple)

    print len(movie_list)
    db.insert_movies(movie_list)


def insert_movie_tag():
    with open('movie_tag', 'rb') as f:
        movie_tag = json.loads(f.read())

    movie_tag_list = list()
    for val in movie_tag:
        movie_tag_tuple = (val[0], val[1])
        movie_tag_list.append(movie_tag_tuple)

    db.insert_movie_tags(movie_tag_list)


def select_specified_tags():
    db = MySQLdb.connect("localhost", "root", "root", "tofu", charset="utf8")
    cursor = db.cursor()
    for i, val in enumerate(Movie_tags):
        sql = "SELECT * FROM tags WHERE tag_name = '%s'" % (val)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                id = row[0]
                name = row[1]
                print i, id, name
        except Exception, e:
            print "%s" % str(e)

if __name__ == '__main__':
    insert_movie()
    insert_tag()
    insert_movie_tag()
    select_specified_tags()
