from flask import Flask, session
from flask.ext.session import Session
from flask.ext.uuid import FlaskUUID
from flask_bootstrap import Bootstrap

import os
import redis
from datetime import timedelta

app = Flask(__name__)

import gatech.select_game
import gatech.game1_acceptable.acceptable
import gatech.game2_winabatt.winabatt
import gatech.game3_qna.qna
import gatech.result.result
from gatech.conf import wait_minutes_for_newplayer

# SESSION_TYPE = 'filesystem'
SESSION_TYPE = 'redis'
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)
#redisIn = Redis()
SESSION_REDIS = r
app.config.from_object(__name__)
Session(app)
FlaskUUID(app)
Bootstrap(app)
app.debug = True
app.secret_key = '\xc9\x93\xd6\x9d\x9b\x99d\xf6\x04\xcf%\xac\xc5\x00\xf0\xb1\x97U\xb4S\x805y'
os.system("echo wait_minutes_for_newplayer = " + str(wait_minutes_for_newplayer))
app.permanent_session_lifetime = timedelta(minutes=wait_minutes_for_newplayer)
os.system('echo app configuration done')