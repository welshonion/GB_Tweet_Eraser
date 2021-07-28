# -*- coding: utf-8 -*-

#ツイートを投稿する

#for local
#import config
#config.write_environ()

import os,json
from flask import Flask, render_template, request, redirect, url_for, session
from requests_oauthlib import OAuth1Session
from apscheduler.schedulers.background import BackgroundScheduler

import twitter_auth
import twitter_delete
import postTweet

app = Flask(__name__)

scheduler = BackgroundScheduler(daemon = True)

#app.config['SECRET_KEY'] = os.urandom(24)

"""TOKEN_PATH= 'token.json'

with open(TOKEN_PATH, mode='r') as f:
    token=json.load(f)
f.close()"""

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

#twitter = OAuth1Session(CK, CS, AT, ATS)
posttweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

@scheduler.scheduled_job('interval',minutes=5)
#@twische.scheduled_job('cron',minute=13,hour=16)
def delete_job():
    print('twitter_delete.deleteManager()')
    twitter_delete.deleteManager()
"""
@scheduler.scheduled_job('interval',seconds=60)
#@twische.scheduled_job('cron',minute=13,hour=16)
def reply_job():
    print('***************************************')
    #main_autoreply.autoManager()
"""

scheduler.start()

if __name__ == '__main__':
    #app.debug = True
    app.run(threaded=True)
