# -*- coding: utf-8 -*-

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

db = psycopg2.connect(DATABASE_URL, sslmode = 'require')

def auth_adduser(user_id, at, ats, work, delete_time):
    #db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS userinfo (user_id varchar(60) unique,at varchar(60),ats varchar(60),work int,deletetime int);'
    
    cursor.execute(sql)
    db.commit()

    upsert = 'INSERT INTO userinfo (user_id, at, ats, work, deletetime) \
    VALUES (%s,%s,%s,%s,%s) \
    ON CONFLICT (user_id) \
    DO UPDATE SET at=%s, ats=%s;'
    upsert_param = [user_id, at, ats, work, delete_time, at, ats]

    cursor.execute(upsert,upsert_param)
    db.commit()

    #user_id, at, ats = auth_checkuser(user_id)

    """if user_id == None:
        cursor.execute(insert)
        db.commit()"""


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

def get_value(user_id):
    cursor = db.cursor()

    sql = 'select * from userinfo where user_id = %s;'

    cursor.execute(sql,[user_id])

    for row in cursor:
        if row[0] == user_id:
            return row
    return None

def set_value(user_id, work, delete_time):
    cursor = db.cursor()

    update = 'UPDATE userinfo \
    SET work=%s, deletetime=%s \
    WHERE user_id=%s;'

    cursor.execute(update,[work,delete_time,user_id])
    db.commit()

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
