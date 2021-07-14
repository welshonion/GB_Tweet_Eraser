# -*- coding: utf-8 -*-

#OauthTokenを取得
#仮想環境のアクティベート忘れずに

import config

import os,json
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from flask import Flask, render_template, request, redirect

TOKEN_PATH= 'token.json'

app = Flask(__name__)


##################################################################
## トークン関連

CK = os.environ.get('CONSUMER_KEY', '0')
CS = os.environ.get('CONSUMER_SECRET', '0')
#CK = config.CONSUMER_KEY
#CS = config.CONSUMER_SECRET

OT = ""
OV = ""

##################################################################


def user_authentication():

    with open(TOKEN_PATH, mode='r') as f:
        token=json.load(f)
    f.close()

    #Authenticate_URLを取得
    #ユーザー連携後にoauth_tokenとoauth_verifierを取得

    #oauth_callback = "https://twitter.com"
    oauth_callback = "http://127.0.0.1:5000/verified/"

    twitter = OAuth1Session(CK,CS)
    request_token_url = "https://api.twitter.com/oauth/request_token"

    response = twitter.post(
        request_token_url,
        params={'oauth_callback':oauth_callback}
    )

    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    authenticate_url = "https://api.twitter.com/oauth/authenticate"
    authorize_url = "https://api.twitter.com/oauth/authorize"
    #authenticate_endpoint = "%s?oauth_token=%s" \
    #%(authorize_url,request_token['oauth_token'])

    authenticate_endpoint = authorize_url + "?oauth_token=" + request_token['oauth_token'] 

    asdf = authorize_url + "?oauth_token=" + request_token['oauth_token'] 

    print(authenticate_endpoint)

    token["AUTHENTICATE_URL"] = authenticate_endpoint
    token["OAUTH_TOKEN"] = ""
    token["OAUTH_VERIFIER"] = ""

    with open(TOKEN_PATH, mode='w') as f:
        json.dump(token,f,indent=4)
    f.close()


    return authenticate_endpoint # Googleにリダイレクトする


def user_verified():

    with open(TOKEN_PATH, mode='r') as f:
        token=json.load(f)
    f.close()

    #ユーザーのoauthtoken
    OT = request.args.get('oauth_token')
    OV = request.args.get('oauth_verifier')

    print(OT)
    print(OV)

    #アクセストークンとアクセストークンシークレットを取得
    twitter = OAuth1Session(CK, CS, OT, OV)

    access_token_url = "https://api.twitter.com/oauth/access_token"
    user_show_url = "https://api.twitter.com/1.1/users/show.json"

    response = twitter.post(
        access_token_url,
        params = {'oauth_verifier':OV}
    )
    #print(oauth_verifier)

    print(response.status_code)

    access_token = dict(parse_qsl(response.content.decode('utf-8')))

    print(access_token)

    token["ACCESS_TOKEN"] = access_token['oauth_token']
    token["ACCESS_TOKEN_SECRET"] = access_token['oauth_token_secret']
    token["USER_ID"] = access_token['user_id']

    with open(TOKEN_PATH, mode='w') as f:
        json.dump(token,f,indent=4)
    f.close()


    twitter = OAuth1Session(CK, CS, token["ACCESS_TOKEN"], token["ACCESS_TOKEN_SECRET"])

    params = {"user_id" : token["USER_ID"]}

    response = twitter.get(user_show_url, params=params)

    results = json.loads(response.text)

    is_verified = False
    name = ""
    screen_name = ""

    if response.status_code == 200:
        name = results['name']
        screen_name = results['screen_name']
        is_verified = True
    else:
        print("Failed:%d" %response.status_code)

    #return redirect('http://127.0.0.1:5000/')
    return is_verified,name,screen_name

@app.route('/')
def index():
    title = "ようこそ"
    message = "こんにちはハローワールド"
    return render_template('index.html', message=message,title=title)

if __name__ == '__main__':
    app.run()


#ログインした状態でURLにアクセスし
#config.pyのOAUTH_TOKEN、OAUTH_VERIFIERを更新



#with open(TOKEN_PATH, mode='w') as f:
#    json.dump(token,f,indent=4)
#f.close()
