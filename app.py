import flask
import os
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from helpers import login_required
app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
# db setup
DB_USER = os.environ.get('DB_USER_MWS')
# print(DB_USER)
DB_PASS = os.environ.get('DB_PASS_MWS')
# print(DB_PASS)
txt = 'mysql://{duser}:{dpass}@localhost/miniwms'.format(duser = DB_USER, dpass = DB_PASS)
engine = sa.create_engine(txt, echo=False, future=True)
meta = sa.MetaData()
# conn = engine.connect()
Base = automap_base()
Base.prepare(engine)
dbs = sa.orm.Session(engine)
# Show the metadata
# for t in Base.metadata.sorted_tables:
#           print(f"\nTable {t.name}:")
#           for c in t.columns:
            #   print(f"{c} ({c.type})")
good_type = Base.classes.good_type
category = Base.classes.category
operation_type = Base.classes.operation_type
outside_org = Base.classes.outside_org
package_type = Base.classes.package_type
user = Base.classes.user
user_type = Base.classes.user_type
warehouse = Base.classes.warehouse
position = Base.classes.position
user__user_type = Base.classes.user__user_type
warehouse__category = Base.classes.warehouse__category
issue = Base.classes.issue
operation = Base.classes.operation
receipt = Base.classes.receipt
type__category = Base.classes.type__category
record = Base.classes.record
record_ops = Base.classes.record_ops
t = dbs.query(good_type).all()
for r in t:
     print(r.name)
print(t)
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
        