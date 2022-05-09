# -*- coding: utf-8 -*-

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

scheduler = BackgroundScheduler(daemon = True,job_defaults={'max_instances': 5})

##################################################################
## トークン関連

CK = os.environ.get('CONSUMER_KEY', '0')
CS = os.environ.get('CONSUMER_SECRET', '0')

##################################################################

@scheduler.scheduled_job('interval',minutes=5)
def delete_job():
    twitter_delete.deleteManager()

scheduler.start()

if __name__ == '__main__':
    #app.debug = True
    app.run(threaded=True)
