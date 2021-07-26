# -*- coding: utf-8 -*-

#ツイートを投稿する

#import os, json, config
#import requests

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

AT = token["ACCESS_TOKEN"]
ATS = token["ACCESS_TOKEN_SECRET"]
USER_ID = token["USER_ID"]

##################################################################

twitter = OAuth1Session(CK, CS, AT, ATS)
posttweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authentication')
def authentication():
    title = 'ようこそ'
    message = 'ツイート内容を入力してください'

    authenticate_endpoint = twitter_auth.user_authentication()

    return redirect(authenticate_endpoint)

    #return #render_template('tweet.html',message=message,title=title)

@app.route('/verified/')
def verified():
    is_verified,name,screen_name = twitter_auth.user_verified()

    #return redirect('http://127.0.0.1:5000/')
    return render_template('verified.html',is_verified = is_verified,name=name,screen_name=screen_name)


@scheduler.scheduled_job('interval',minutes=1)
#@twische.scheduled_job('cron',minute=13,hour=16)
def delete_job():
    twitter_delete.deleteManager()

@scheduler.scheduled_job('interval',seconds=60)
#@twische.scheduled_job('cron',minute=13,hour=16)
def reply_job():
    print('***************************************')
    #main_autoreply.autoManager()

scheduler.start()

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
    
    
    











@app.route('/tweet')
def index():
    title = 'ようこそ'
    message = 'ツイート内容を入力してください'
    return render_template('tweet.html',
    message=message,title=title)

@app.route('/post', methods=['GET','POST'])
def post():
    title='ツイート'
    if request.method == 'POST':
        #リクエストフォームから「名前」を取得して
        tweettext = request.form['formtweettext']
        params = {"status":tweettext}

        response = twitter.post(posttweet_url,params = params)

        if response.status_code == 200:
            #index.htmlをレンダリングする
            return render_template('tweet.html',
            name=tweettext,title=title)
        else:
            message = '投稿失敗（エラーコード：'+ response.status_code +')'
            return render_template('tweet.html',
            message=message,title=title)
    else:
        #ERRORでリダイレクトする場合
        return redirect(url_for('index'))

