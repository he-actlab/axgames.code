from flask import Flask, session
from flask.ext.session import Session
from flask.ext.uuid import FlaskUUID
from flask_bootstrap import Bootstrap

app = Flask(__name__)

import gatech.select_game
import gatech.game1_acceptable
import gatech.game2_winbatt
import gatech.game3_qna

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
FlaskUUID(app)
Bootstrap(app)