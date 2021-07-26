# -*- coding: utf-8 -*-

#ユーザーのツイートを表示

#import config

import os,json
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import psycopg2
from datetime import datetime

import databaseIO

TOKEN_PATH= 'token.json'

with open(TOKEN_PATH, mode='r') as f:
    token=json.load(f)
f.close()

##################################################################
## トークン関連

CK = os.environ.get('CONSUMER_KEY', '0')
CS = os.environ.get('CONSUMER_SECRET', '0')
#CK = config.CONSUMER_KEY
#CS = config.CONSUMER_SECRET

#AT = token["ACCESS_TOKEN"]
#ATS = token["ACCESS_TOKEN_SECRET"]
#USER_ID = token["USER_ID"]

##################################################################

DELETE_WORD = '参戦ID'
DELETE_VERIFY_WORD = '参加者募集'

'urlをあらかじめ取得しておく'

baseurl = "https://api.twitter.com/1.1/statuses/"


user_timeline_url = baseurl + "user_timeline.json"
home_timeline_url = baseurl + "home_timeline.json"
posttweet_url = baseurl + "update.json"
checklimit_url = "https://api.twitter.com/1.1/application/rate_limit_status.json"

global last_tweet_id

last_tweet_id = 0


database = []

def deleteManager():
    global database

    #データベースからユーザー情報を取得して格納
    database = databaseIO.auth_getalluser()

    #各ユーザーに対してユーザータイムラインを確認して削除
    for row in database:
        deleteUserTweet(row)

    return

def deleteUserTweet(userinfo):

    session = OAuth1Session(CK, CS, userinfo[1], userinfo[2])

    'checkAccessLimit():回数制限の問い合わせ'
    checkAccessLimit(session)
    '上で勝手にスリープまでやってくれる'
    'getTimelines():タイムラインの取得'
    checkFromTL(session)

    return 

def checkAccessLimit(session):
    unavailableCnt = 0
    while True:
        '通信が正常か（セッションを設ける）'
        res_cl = session.get(checklimit_url)
        '正常でないならERROR'
        if res_cl.status_code == 503:
            if unavailableCnt > 3:
                raise Exception('Twitter API error %d' % res_cl.status_code)
            unavailableCnt += 1
            print('Service Unavailable 503')
            waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            continue

        unavailableCnt = 0

        if res_cl.status_code != 200:
            raise Exeprion('Twitter API error %d' % res_cl.status_code)

        '正常ならセッションから残り回数とリセット時間をintで取得'

        res_cl_text = json.loads(res_cl.text)
        remaining = int(res_cl_text['resources']['statuses']['/statuses/home_timeline']['remaining'])
        reset = int(res_cl_text['resources']['statuses']['/statuses/home_timeline']['reset'])

        print('remaining:%d' % remaining)
        print('reset:%d' % reset)

        '残りの時間が0ならリセットまで待つ:waitUntilReset(reset)'
        'それ以外ならbreak'

        if(remaining == 0):
            waitUntilReset(reset)
        else:
            break


def checkFromTL(session):

    global last_tweet_id
    #global db

    params = {
        'exclude_replies':False,
        #'exclude_replies': json.get('exclude_replies',False),
        #'since_id':last_tweet_id,
        'count':200,
        'trim_user':False,
        'tweet_mode':'extended',
    }

    res_htl = session.get(user_timeline_url, params = params)

    if res_htl.status_code == 200:
        timelines = json.loads(res_htl.text)

        firstline  = True

        for line in timelines:
            if(DELETE_WORD in line['full_text']):
                
                print(DELETE_WORD)
                print(line['id'])

                if(DELETE_VERIFY_WORD in line['full_text']):
                    print(DELETE_VERIFY_WORD)
                    delete_tweet(session,line['id'])

            print(line['user']['name']+'::'+line['full_text'])
            print(line['created_at'])
            created_at = datetime.strptime(line['created_at'], '%a %b %d %H:%M:%S %z %Y')
            print(created_at)
            print("***************************************")

    else:
        print('Failed:%d' % res_htl.status_code)


def delete_tweet(session,tweet_id):
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
    destroy_url = "https://api.twitter.com/1.1/statuses/destroy/" + str(tweet_id) + ".json"


    try:
        res = session.post(destroy_url)

        if res.status_code == 200:
            print("Destroy Success.")
        else:
            print("Destroy Failed. :%d"% res.status_code)
    except:
        print('Destory Failed.:exception')

    return

"""
def func_read_last_id():
    global last_tweet_id

    try:
        db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        print("db connect")
        cursor = db.cursor()
        print('cursor')

        cursor.execute('CREATE TABLE IF NOT EXISTS last_id(lid varchar(20),name varchar(20))')
        print('create_table')
    except:
        print('connect error')

    #db = sqlite3.connect("sample.db")
    print("read table")

    sql_last_id = 'SELECT * FROM last_id;'
    print("param ok")
    cursor.execute(sql_last_id)
    print("success select")
    for row in cursor:
        last_tweet_id = row[1]
        last_tweet_id=int(last_tweet_id)
        print(last_tweet_id)

    db.close()


def func_write_last_id():
    global last_tweet_id

    #db = sqlite3.connect("sample.db")
    #cursor = db.cursor()

    try:
        db = psycopg2.connect(DATABASE_URL, sslmode = 'require')
        print("db connect")
        cursor = db.cursor()
        print('cursor')

        cursor.execute('CREATE TABLE IF NOT EXISTS last_id(lid varchar(25),name bigints)')
        print('create_table')
    except:
        print('connect error')


    print("create or exist table")

    try:
        print('delete')
        cursor.execute('delete from last_id')
        db.commit()

    except:
        print('maybe delete first or error')


    print("insert params")
    print(last_tweet_id)

    #cursor.execute(insert_sql,insert_sql_params)
    cursor.execute("INSERT INTO last_id (lid, name) VALUES ('lid_last_id', %d);" % last_tweet_id)

    print("execute insert")

    db.commit()

    print("commit")

    sql_last_id = 'SELECT * FROM last_id;'
    cursor.execute(sql_last_id)
    for row in cursor:
        print("row is")
        last_tweet_id = row[1]
        print(last_tweet_id)

    db.close()

"""



if __name__ == '__main__':

    'いつかは（継承で）要らなくなる場所'
    '関数呼び出し用'

    'autoManager呼び出し'
    deleteManager()


