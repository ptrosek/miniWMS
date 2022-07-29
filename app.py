import flask
from flask_session import Session

from helpers import login_required
app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False

Session(app)
@app.route("/")
@login_required
def index_worker():
    return flask.render_template("index.html")

@app.route("/login")
def login():
    return flask.render_template("login.html")