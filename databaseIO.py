# -*- coding: utf-8 -*-
import sqlite3
import psycopg2


import json, datetime, time, sys, os, re
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from abc import ABCMeta, abstractmethod
from glob import iglob
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']


def func_delete():
    db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    'db = sqlite3.connect("kkk.db")'
    cursor = db.cursor()
    cursor.execute('delete from last_id')

    db.commit()
    sql = 'select * from last_id'
    cursor.execute(sql)
    for row in cursor:
        print("****")
        print(row[0])
        print(row[1])

    db.close()


def func_drop():
    db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    'db = sqlite3.connect("kkk.db")'
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS last_id;')

    db.commit()

    print("success drop")

    db.close()

def func_exist():
    db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    'db = sqlite3.connect("kkk.db")'
    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS last_id(lid varchar(25),name bigint)')

    num = 114514810
    last_tweet_id = 1223372036854775807
    "str_last_tweet_id = 3147483647"

    cursor.execute("INSERT INTO last_id (lid, name) VALUES ('lid_last_id', %d);" % last_tweet_id)

    "cursor.execute('insert into last_id (lid, name) values (%s, %s)',('lid_last_id',num))"

    db.commit()

    sql = 'select * from last_id'
    cursor.execute(sql)
    "sql = 'select * from last_id where lid = ""First message""'"
    "for row in cursor.execute(sql):"
    for row in cursor:
        print("****")
        print(row[0])
        print(row[1])

    db.close()

def func_read():
    db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    'db = sqlite3.connect("kkk.db")'
    cursor = db.cursor()

    sql = 'SELECT * FROM last_id'
    cursor.execute(sql)
    "sql = 'select * from last_id where lid = ""First message""'"
    "for row in cursor.execute(sql):"
    for row in cursor:
        print("****")
        print(row[0])
        print(row[1])

    db.close()



#if __name__ == '__main__':
#    func_delete()
