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

# creating sqlalchemy connection string and connecting the engine
try:
    txt = 'mysql://{duser}:{dpass}@localhost/miniwms'.format(duser = DB_USER, dpass = DB_PASS)
    engine = sa.create_engine(txt, echo=True, future=True)
    meta = sa.MetaData()
    Base = automap_base()
    Base.prepare(engine)
except:
    flask.abort(500)

# Show the metadata(used to create tables.txt)
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

# setting dbs later used to work with db data
dbs = sa.orm.Session(engine)

# create admin user 
def create_admin():
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
def operation_log(ot):
    o = operation(
        ops_type = ot,
        user_executing = flask.session["user_id"]
    )
    return o
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
        dbs.begin()
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
        dbs.add(operation_log(1))
        dbs.commit()
        # Redirect user to home page
        return flask.redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return flask.render_template("login.html")
@app.route('/logout')
def logout():
    # set the user id to none making login_required return false
    dbs.begin()
    dbs.add(operation_log(2))
    dbs.commit()
    flask.session["user_id"] = None
    return flask.redirect("/login")
@app.route("/category", methods=["GET","POST"])
@login_required
def cat():
    # check if the required elements were included
    if flask.request.method == "POST":
        if (not flask.request.form.get("name")) or (len(flask.request.form.get("name")) > 255):
            flask.flash("wrong name")
            return flask.redirect("/category")
        elif len(flask.request.form.get("desc")) > 1000:
            flask.flash("max amount of characters in description is 1000")
            return flask.redirect("/category")
        # transaction to add form data into the db
        try:
            dbs.begin()
            q = category(
                name = flask.request.form.get("name"),
                description = flask.request.form.get("desc")
                )
            dbs.add(q)
            dbs.add(operation_log(4))
            dbs.commit()
        except:
             flask.flash("error creating category")
             return flask.render_template("index.html")
        flask.flash("category created")
        return flask.render_template("index.html")
    else:
        return flask.render_template("category.html")
@app.route("/gtc", methods=["GET","POST"])
@login_required
def gtc():
    # check if the required elements were included
    if flask.request.method == "POST":
        if not flask.request.form.get("name"):
            flask.flash("name input blank")
            return flask.redirect("/")
        # transaction to input form data into db
        try:
            if flask.request.form.get("ean"):
                ean = flask.request.form.get("ean")
            else:
            # if the data was not inputed set variable to sql NULL
                ean = sa.sql.null()
            if flask.request.form.get("size"):
                size = flask.request.form.get("size")
            else:
                size = sa.sql.null()
            if flask.request.form.get("weight"):
                weight = flask.request.form.get("weight")
            else:
                weight = sa.sql.null()
            if flask.request.form.get("pt") != 'None':
                pt = flask.request.form.get("pt")
            else:
                pt = sa.sql.null()
            # flask.request.form.getlist("cc")
            dbs.begin()
            q = good_type(
                 name = flask.request.form.get("name"),
                 ean = ean,
                 size = size,
                 weight = weight,
                 package_type_gt = pt
                 )
            dbs.add(q)
            # inputing data into db without needing to commit it to be able to retrive q.id
            dbs.flush()
            if flask.request.form.get("cc"):
                for i in range(len(flask.request.form.getlist("cc"))):
                    p = type__category(
                        categoryid = flask.request.form.getlist("cc")[i],
                        type_id = q.id
                    )
                    dbs.add(p)
                    # print(p.type_id)
            dbs.add(operation_log(4))
            dbs.commit()
        except:
            flask.flash("error in database")
            return flask.redirect("/")
        flask.flash("good type created")
        return flask.redirect("/")
    else:
        try:
            # get data from the db saved as a list to make it iterable in jinjja and viewed as select
            dbs.begin()
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
        except:
            flask.flash("error rendering webiste")
            return flask.redirect('/')
@app.route("/org",methods=["GET", "POST"])
@login_required
def org():
    # works the same way as POST part of gtc
    if flask.request.method == "POST":
        if not flask.request.form.get("name"):
            flask.flash("name not inputed")
            return flask.redirect("/org")
        name = flask.request.form.get("name")
        if not flask.request.form.get("name"):
            flask.flash("mail not inputed")
            return flask.redirect("/org")
        mail = flask.request.form.get("mail")
        if flask.request.form.get("bi"):
            bi = flask.request.form.get("bi")
        else:
            bi = sa.sql.null()
        if flask.request.form.get("address"):
            adr = flask.request.form.get("address")
        else:
            adr = sa.sql.null()
        try:
            dbs.begin()
            q = outside_org(
                name = name,
                mail = mail,
                bank_info = bi,
                addres = adr
            )
            dbs.add(q)
            dbs.add(operation_log(4))
            dbs.commit()
        except:
            flask.flash("database error")
            return flask.redirect("/")
        flask.flash("org created")
        return flask.redirect("/")
    else:
        return flask.render_template("org.html")
@app.route("/warehouse",methods=["GET", "POST"])
@login_required
def war():
    if flask.request.method == "POST":
        if not flask.request.form.get("name"):
            flask.flash("name not inputed")
            return flask.redirect("/org")
        name = flask.request.form.get("name")
        if not flask.request.form.get("address"):
            ads = sa.sql.null()
        else:
            ads = flask.request.form.get("address")
        if not flask.request.form.get("city"):
            city = sa.sql.null()
        else:
            city = flask.request.form.get("city")
        if not flask.request.form.get("state"):
            state = sa.sql.null()
        else:
            state = flask.request.form.get("state")
        if not flask.request.form.get("country"):
            country = sa.sql.null()
        else:
            country = flask.request.form.get("country")
        if not flask.request.form.get("desc"):
            desc = sa.sql.null()
        else:
            desc = flask.request.form.get("desc")
        if not flask.request.form.get("size"):
            size = sa.sql.null()
        else:
            size = flask.request.form.get("size")
        try:
            dbs.begin()
            ww = warehouse(
                name = name,
                addres =  ads,
                city = city,
                state = state,
                country = country,
                size = size,
                description = desc
            )
            dbs.add(ww)
            dbs.flush()
            if flask.request.form.getlist("cc"):
                for cat in flask.request.form.getlist("cc"):
                    wp = warehouse__category(
                        idwarehouse = ww.id,
                        idcategory = cat
                    )
                    dbs.add(wp)
            for i in range(int(flask.request.form.get("num"))):
                if not flask.request.form.get("name{}".format(i)):
                    zn = sa.sql.null()
                else:
                    zn = flask.request.form.get("name{}".format(i))
                zr = int(flask.request.form.get("rows{}".format(i)))
                zc = int(flask.request.form.get("columns{}".format(i)))
                if not flask.request.form.get("cells{}".format(i)):
                    hh = None
                    zh = sa.sql.null()
                else:
                    hh = 1
                    zh = int(flask.request.form.get("cells{}".format(i)))
                for r in range(zr):
                    for c in range(zc):
                        if hh == 1:
                            for h in range(zh):
                                q = position(
                                    row = r,
                                    column = c,
                                    cell = h,
                                    warehouse_pos = ww.id,
                                    zone = zn
                                )
                                dbs.add(q)
                        else:
                                q = position(
                                    row = r,
                                    column = c,
                                    warehouse_pos = ww.id,
                                    zone = zn
                                )
                                dbs.add(q)
            dbs.add(operation_log(4))
            dbs.commit()
            flask.flash("warehouse succesfully cretated")
            return flask.redirect("/")
        except:
            flask.flash("error in database connection")
            return flask.redirect("/")
    else:
        try:
            listc = []
            dbs.begin()
            cats = dbs.scalars(sa.select(category))
            for catly in cats:
                listc.append({'name': catly.name, 'id': catly.id})
            dbs.commit()
            return flask.render_template("warehouse.html",cats = listc)
        except:
            flask.flash("error rendering webiste")
            return flask.redirect('/')
@app.route("/receipt",methods=["GET", "POST"])
@login_required
def rec():
    if flask.request.method == "POST":
        supp = flask.request.form.get("supp")
        usera =flask.session["user_id"]
        if flask.request.form.get("uu") == "any":
            usere = sa.sql.null()
        else:
            usere = flask.request.form.get("uu")
        print(flask.request.form.get("arrpos"))
        pos = int(flask.request.form.get("arrpos"))
        print(pos)
        arrival = flask.request.form.get("arrival")
        if not flask.request.form.get("comment"):
            com = sa.sql.null()
        else:
            com = flask.request.form.get("comment")
        try:
            dbs.begin()
            q = receipt(
                supplier = supp,
                user_executing = usere,
                user_approving = usera,
                position_re = pos,
                arrival = arrival,
                comment = com
            )
            dbs.add(q)
            op = operation_log(3)
            dbs.add(op)
            dbs.flush()
            for i in range(int(flask.request.form.get("num"))):
                gt_type = flask.request.form.get("gtt{}".format(i))
                # print(gt_type)
                gt_amount = int(flask.request.form.get("gtn{}".format(i)))
                if not flask.request.form.get("gtc{}".format(i)):
                    gt_comment = sa.sql.null()
                else:
                    gt_comment = flask.request.form.get("gtc{}".format(i))
                for j in range(gt_amount):
                    k = record(
                        comment = gt_comment,
                        type = gt_type,
                        receipt_rec = q.id,
                        current_position = pos,
                        last_update = q.time_info
                    )
                    dbs.add(k)
                    dbs.flush()
                    l = record_ops(
                        record_id = k.id,
                        ops_id = op.id
                    )
                    dbs.add(l)
                dbs.commit()
            flask.flash("reciept created")
            return flask.redirect("/")
        except:
            flask.flash("error creating receipt")
            return flask.redirect("/")
    else:
        dbs.begin()
        list_s = []
        suppliers = dbs.scalars(sa.select(outside_org))
        for sup in suppliers:
            list_s.append({'name': sup.name, 'id': sup.id})
        list_u = []
        users = dbs.scalars(sa.select(user))
        for u in users:
            list_u.append({'id': u.id, 'name': u.name, 'first_name': u.first_name, 'last_name': u.last_name})
        list_p = []
        positions = dbs.scalars(sa.select(position))
        for pos in positions:
            list_p.append({'id': pos.id, 'row': pos.row, 'column': pos.column, 'cell': pos.cell, 'zone': pos.zone, 'warehouse_pos': pos.warehouse_pos})
        list_g = []
        goods = dbs.scalars(sa.select(good_type))
        for good in goods:
            list_g.append({'id': good.id, 'name':good.name, 'ean': good.ean})
        dbs.commit()
        return flask.render_template("receipt.html", suppliers = list_s, users = list_u, positions = list_p, goods = list_g)