#!/usr/bin/env python
# coding=UTF-8

"""
    @author: Corazon (Peibo Xu)
    @date: 2016-01-09
    @desc:
        Database operation
"""

import sys
import MySQLdb

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PWD = 'root'
MYSQL_DB ='tofu'


def get_connection():
    return connect()


def connect():
    conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, \
            db=MYSQL_DB)
    return conn


def execute_sqls(sql, args=None):
    ret = 0
    try:
        conn = get_connection()
        cur = conn.cursor()
        ret = cur.executemany(sql, args)
        conn.commit()
    except MySQLdb.Error, e:
        print "execute_sqls error: %s" %str(e)
        return False
    finally:
        cur.close()

    return ret


def insert_movies(args):
    sql = "INSERT INTO movies (movie_id, name, star, image_url) \
     VALUES (%s, %s, %s, %s)"

    return execute_sqls(sql, args)

def insert_tags(args):
    sql = "INSERT INTO tags (tag_name) \
    VALUES (%s)"

    return execute_sqls(sql, args)

def insert_movie_tags(args):
    sql = "INSERT INTO movietags (movie_id, tag_id) \
     VALUES (%s, %s)"

    return execute_sqls(sql, args)

