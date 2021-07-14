# -*- coding: utf-8 -*-

#ツイートを投稿する

import json, config
from requests_oauthlib import OAuth1Session

TOKEN_PATH= 'token.json'

with open(TOKEN_PATH, mode='r') as f:
    token=json.load(f)
f.close()

##################################################################
## トークン関連

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET

AT = token["ACCESS_TOKEN"]
ATS = token["ACCESS_TOKEN_SECRET"]
USER_ID = token["USER_ID"]

##################################################################


def tweet():
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"

    twitter = OAuth1Session(CK, CS, AT, ATS)



    print("内容")
    #tweet = input(">>")
    print("***************************************")

    tweet = "イズミヤ～"

    params = {"status" : tweet}

    res = twitter.post(tweet_url, params = params)

    if res.status_code == 200:
        print("Success.")
    else:
        print("Failed. :%d"% res.status_code)

    return 
