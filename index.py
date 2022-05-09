# -*- coding: utf-8 -*-

#for local
#import config
#config.write_environ()

import os,json
from flask import Flask, render_template, request, redirect, url_for, session
from requests_oauthlib import OAuth1Session
from datetime import timedelta

import twitter_auth
import twitter_delete
import postTweet
import databaseIO

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.permanent_session_lifetime = timedelta(minutes=5)

#session.permanent = True
#scheduler = BackgroundScheduler(daemon = True)


##################################################################
## トークン関連

CK = os.environ.get('CONSUMER_KEY', '0')
CS = os.environ.get('CONSUMER_SECRET', '0')

##################################################################

is_verified = False
name = ""
screen_name = ""

w = ('stop','running')

@app.route('/')
def index():
    session['is_verified'] = False
    session['auth_process'] = False
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    session['auth_process'] = True
    authorize_endpoint = twitter_auth.user_authorize()

    return redirect(authorize_endpoint)

@app.route('/authenticate')
def authenticate():
    session['auth_process'] = True
    authenticate_endpoint = twitter_auth.user_authenticate()

    return redirect(authenticate_endpoint)
    #return #render_template('tweet.html',message=message,title=title)

"""@app.route('/verified')
def verified():
    is_verified,name,screen_name = twitter_auth.user_verified()

    #return redirect('http://127.0.0.1:5000/')
    return render_template('verified.html',is_verified = is_verified,name=name,screen_name=screen_name)


@app.route('/setting_authenticate')
def authenticate():

    authenticate_url = twitter_auth.user_authenticate_setting()

    return redirect(authenticate_url)

    #return #render_template('tweet.html',message=message,title=title)
"""

@app.route('/setting', methods=['GET','POST'])
def setting():
    global is_verified, name, screen_name

    user_id = ""

    if session.get('is_verified') != True:
        session['is_verified'] = False

    if session.get('auth_process') != True:
        print("no auth_process")
        session['auth_process'] = False


    if session['auth_process'] == True :
        try:
            twitter_auth.user_verified()
            print("verify success")
            session['auth_process'] = False
        except:
            print("verify failed")
            session['auth_process'] = False
            return render_template('setting.html',is_verified = False)
    else:
        if session['is_verified'] == True:
            #設定保存時
            if(request.form["work"]=='running'):
                work_value = 1
            else:
                work_value = 0

            print("asdf")

            delete_list = 0

            if(request.POST["deleteword_id"]):
                delete_list += 1

            if(request.POST["deleteword_rpg"]):
                delete_list += 2

            if(request.POST["deleteword_free"]):
                delete_list += 4

            delete_word = request.form["deleteword_free_text"]


            databaseIO.set_value(session['user_id'], work_value, request.form["deletetime"], delete_list, delete_word)

            print(request.form["work"])
            print(request.form["deletetime"])
            #param = json.loads(request.data.decode('utf-8'))
            #print(param["work"])
            #print(param.get('deletetime'))

            print("verified")
        else:
            print("invalid transition")
            session['auth_process'] = False
            return render_template('setting.html',is_verified = False)

    user_id = session['user_id']

    userinfo = databaseIO.get_value(user_id)

    is_verified = session['is_verified']
    name = session['name']
    screen_name = session['screen_name']
    work = userinfo[3]
    delete_time = userinfo[4]

    deleteword_id = userinfo[5]%2
    deleteword_rpg = int((userinfo[5]%4)/2)
    deleteword_free = int(userinfo[5]/4)

    deleteword_free_text_pre = userinfo[6]

    print(name)

    return render_template('setting.html',is_verified = is_verified,name=name,screen_name=screen_name,work=w[work],delete_time=delete_time, deleteword_id=deleteword_id,deleteword_rpg=deleteword_rpg,deleteword_free=deleteword_free,deleteword_free_text_pre=deleteword_free_text_pre)


@app.route('/delete', methods=['GET','POST'])
def delete():

    if request.method == 'POST':
        databaseIO.auth_deleteuser(session['user_id'])
        print("delete")
        return render_template('delete.html',deleted=True)
    else:
        return render_template('delete.html',deleted=False)

    return render_template('delete.html',deleted=False)

if __name__ == '__main__':
    #app.debug = True
    app.run(threaded=True)
    