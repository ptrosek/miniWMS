from sqlite3 import Cursor
import flask
import os
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

from helpers import login_required
app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)
# db setup
DB_USER = os.environ.get("DB_USER_MWS")
DB_PASS = os.environ.get("DB_PASS_MWS")
mysql_config = {
    'user':DB_USER,
    'password':DB_PASS,
    'host':'localhost',
    'database':'miniwms',
    'port':'3306',
    # 'ssl_disabled': True
}
mydb = mysql.connector.connect(**mysql_config)
cursor=mydb.cursor()
print(mydb)
@app.route("/")
@login_required
def index_worker():
    return flask.render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    flask.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if flask.request.method == "POST":

        # Ensure username was submitted
        if not flask.request.form.get("username"):
            return flask.abort(400)

        # Ensure password was submitted
        elif not flask.request.form.get("password"):
            return flask.abort(400)

        # Query database for username
        rows = 123

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], flask.request.form.get("password")):
            return flask.abort(400)

        # Remember which user has logged in
        flask.session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return flask.redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return flask.render_template("login.html")
mydb.close()