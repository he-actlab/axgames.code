from flask import Flask, session
from flask.ext.session import Session
from flask.ext.uuid import FlaskUUID
from flask_bootstrap import Bootstrap

app = Flask(__name__)

import gatech.select_game
import gatech.game1_acceptable.acceptable
import gatech.game2_winabatt.winabatt
import gatech.game3_qna.qna

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)
FlaskUUID(app)
Bootstrap(app)
app.debug = True
app.secret_key = '\xc9\x93\xd6\x9d\x9b\x99d\xf6\x04\xcf%\xac\xc5\x00\xf0\xb1\x97U\xb4S\x805y'