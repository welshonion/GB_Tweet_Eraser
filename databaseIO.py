# -*- coding: utf-8 -*-
#import sqlite3
#import psycopg2


#import json, datetime, time, sys, os, re
#from requests_oauthlib import OAuth1Session
#from urllib.parse import parse_qsl
#from abc import ABCMeta, abstractmethod
#from glob import iglob
#import psycopg2

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

db = psycopg2.connect(DATABASE_URL, sslmode = 'require')

def auth_adduser(user_id, at, ats, delete_time):
    #db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS userinfo (user_id varchar(60),at varchar(60),ats varchar(60),deletetime int);'
    
    cursor.execute(sql)
    db.commit()

    #num = 114514810
    #last_tweet_id = 1223372036854775807
    "str_last_tweet_id = 3147483647"

    insert = "INSERT INTO userinfo (user_id, at, ats, deletetime) VALUES ('%s', '%s', '%s', %d);" % (user_id, at, ats, delete_time)

    user_id, at, ats = auth_checkuser(user_id)

    if user_id == None:
        cursor.execute(insert)
        db.commit()


    #sql = 'select * from userinfo'
    #cursor.execute(sql)
    "sql = 'select * from last_id where lid = ""First message""'"
    "cursor.execute(sql):"
    """for row in cursor:
        print("****")
        print(row[0])
        print(row[1])"""

    #db.close()

    return

def auth_checkuser(user_id):
    #db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = db.cursor()

    sql = 'select * from userinfo;'

    cursor.execute(sql)

    for row in cursor:
        if row[0] == user_id:
            return row[1],row[2],row[3]

    return None, None, None

def auth_getalluser():
    cursor = db.cursor()

    sql = 'select * from userinfo;'

    cursor.execute(sql)

    return cursor

def auth_deleteuser(user_id):
    #db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = db.cursor()
    cursor.execute("delete from userinfo where user_id = '%s';" % (user_id))

    db.commit()
    #db.close()

    return

def auth_deleteall():
    #db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = db.cursor()
    cursor.execute('delete from userinfo;')

    db.commit()
    #db.close()

    return

def auth_drop():
    #db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS userinfo;')

    db.commit()
    #db.close()

    return



#if __name__ == '__main__':
#    func_delete()
