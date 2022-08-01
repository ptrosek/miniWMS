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
# get login data for mysql server 
DB_USER = os.environ.get('DB_USER_MWS')
# print(DB_USER)
DB_PASS = os.environ.get('DB_PASS_MWS')
# print(DB_PASS)
txt = 'mysql://{duser}:{dpass}@localhost/miniwms'.format(duser = DB_USER, dpass = DB_PASS)
engine = sa.create_engine(txt, echo=True, future=True)
meta = sa.MetaData()
Base = automap_base()
Base.prepare(engine)
# Show the metadata
# for t in Base.metadata.sorted_tables:
#           conn = engine.connect()
#           print(f"\nTable {t.name}:")
#           for c in t.columns:
            #   print(f"{c} ({c.type})")
#           conn.close()
# setting allisases for tables
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

# test query
# conn = engine.connect()
# t = dbs.query(good_type).all()
# for r in t:
#      print(r.name)
# print(t)
# conn.close()

# create admin user 
def create_admin():
    dbs = sa.orm.Session(engine)
    dbs.begin()
    admin = user(
        id = 1,
        name = "admin",
        hash = generate_password_hash("admin", method='pbkdf2:sha256', salt_length=8)
    )
    dbs.add(admin)
    dbs.commit()
    return
# create_admin()

# clearing logged in people
@app.route("/")
@login_required
def index_worker():
    return flask.render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    flask.session["user_id"] = None
    # User reached route via POST (as by submitting a form via POST)
    if flask.request.method == "POST":
        # Ensure username was submitted
        if not flask.request.form.get("uid"):
            flask.flash("username not entered")
            return flask.redirect("/login")
        # Ensure password was submitted
        elif not flask.request.form.get("pass"):
            flask.flash("password not entered")
            return flask.redirect("/login")
        # Query database for username
        dbs = sa.orm.Session(engine)
        rows = dbs.query(user).filter_by(name=flask.request.form.get("uid")).first()
        # print(rows.name)
        # print(rows.hash)
        # print(generate_password_hash("admin", method='pbkdf2:sha256', salt_length=8))
        # print(check_password_hash(rows.hash, flask.request.form.get("pass")))
        # Ensure username exists and password is correct
        if not check_password_hash(rows.hash, flask.request.form.get("pass")):
              flask.flash("password and user name dont match")
              return flask.render_template("login.html")

        # # Remember which user has logged in
        flask.session["user_id"] = rows.id
        dbs.commit()
        # Redirect user to home page
        return flask.redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return flask.render_template("login.html")
@app.route('/logout')
def logout():
    flask.session["user_id"] = None
    return flask.redirect("/login")
@app.route("/category", methods=["GET","POST"])
def cat():
    if flask.request.method == "POST":
        if (not flask.request.form.get("name")) or (len(flask.request.form.get("name")) > 255):
            flask.flash("wrong name")
            return flask.redirect("/category")
        elif len(flask.request.form.get("desc")) > 1000:
            flask.flash("max amount of characters in description is 1000")
            return flask.redirect("/category")
        try:
            dbs = sa.orm.Session(engine)
            q = category(
                name = flask.request.form.get("name"),
                description = flask.request.form.get("desc")
                )
            dbs.add(q)
            dbs.commit()
        except:
             flask.flash("error creating category")
             return flask.render_template("index.html")
        flask.flash("category created")
        return flask.render_template("index.html")
    else:
        return flask.render_template("category.html")
@app.route("/gtc", methods=["GET","POST"])
def gtc():
    if flask.request.method == "POST":
        if not flask.request.form.get("name"):
            flask.flash("name input blank")
            return flask.redirect("/")
        try:
            dbs = sa.orm.Session(engine)
            if flask.request.form.get("ean"):
                ean = flask.request.form.get("ean")
            else:
                ean = "NULL"
            if flask.request.form.get("size"):
                size = flask.request.form.get("size")
            else:
                size = "NULL"
            if flask.request.form.get("weight"):
                weight = flask.request.form.get("weight")
            else:
                weight = "NULL"
            if flask.request.form.get("pt"):
                pt = flask.request.form.get("pt")
            else:
                pt = "NULL"
            flask.request.form.getlist("cc")
            q = good_type(
                 name = flask.request.form.get("name"),
                 ean = ean,
                 size = size,
                 weight = weight,
                 package_type_gt = pt
                 )
            dbs.add(q)
            dbs.commit()
        except:
            flask.flash("name input blank")
            return flask.redirect("/")
        flask.flash("good type created")
        return flask.redirect("/")
    else:
        dbs = sa.orm.Session(engine)
        types = dbs.scalars(sa.select(package_type))
        listt = []
        for type in types:
            listt.append({'name': type.name, 'id': type.id})
            # print(type.name)
        listc = []
        cats = dbs.scalars(sa.select(category))
        for catly in cats:
            listc.append({'name': catly.name, 'id': catly.id})
        dbs.commit()
        # print(list)
        return flask.render_template("gtc.html", types=listt, cats=listc)
