import flask
import os
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from helpers import login_required
import blabel

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
#               print(f"{c} ({c.type})")
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
move = Base.classes.move
move__record = Base.classes.move__record
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
    # getting data from the form and inputing to db
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
            # flushing the db to get warehouse id
            dbs.flush()
            # creating all of the possible positions within range
            if flask.request.form.getlist("cc"):
                for cat in flask.request.form.getlist("cc"):
                    wp = warehouse__category(
                        idwarehouse = ww.id,
                        idcategory = cat
                    )
                    dbs.add(wp)
            num = flask.request.form.get("num")
            if not num:
                flask.flash("error handling the form. contact your system administrator")
                return flask.redirect("/issue")
            for i in range(int(num)):
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
        # get all of the categories from the database
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
    # same as before
    if flask.request.method == "POST":
        supp = flask.request.form.get("supp")
        usera =flask.session["user_id"]
        if flask.request.form.get("uu") == "any":
            usere = sa.sql.null()
        else:
            usere = flask.request.form.get("uu")
        # print(flask.request.form.get("arrpos"))
        pos = int(flask.request.form.get("arrpos"))
        # print(pos)
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
            # creating records and operations for goods in the receipt
            num = flask.request.form.get("num")
            if not num:
                flask.flash("error handling the form. contact your system administrator")
                return flask.redirect("/issue")
            for i in range(int(num)):
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
        try:
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
        except:
            flask.flash("cannot load website. contact your system administrator")
            return flask.redirect("/")
@app.route("/issue",methods=["GET","POST"])
@login_required
def iss():
    if flask.request.method == "POST":
        supp = flask.request.form.get("supp")
        usera =flask.session["user_id"]
        if flask.request.form.get("uu") == "any":
            usere = sa.sql.null()
        else:
            usere = flask.request.form.get("uu")
        # print(flask.request.form.get("deppos"))
        pos = int(flask.request.form.get("deppos"))
        # print(pos)
        deps = flask.request.form.get("deptime")
        if not flask.request.form.get("comment"):
            com = sa.sql.null()
        else:
            com = flask.request.form.get("comment")
        num = flask.request.form.get("num")
        if not num:
            flask.flash("error handling the form. contact your system administrator")
            return flask.redirect("/issue")
        try:
            dbs.begin()
            q = issue(
                customer = supp,
                user_executing = usere,
                user_approving = usera,
                position_is = pos,
                comment = com,
                departure = deps
            )
            dbs.add(q)
            op = operation_log(6)
            dbs.add(op)
            dbs.flush()
            for i in range(int(num)):
                gtt = flask.request.form.get("gtt{}".format(i))
                gtn = int(flask.request.form.get("gtn{}".format(i)))
                recs = dbs.query(record).where(sa.and_(record.issue_rec == None, record.type == gtt))
                amount_of_recs = recs.count()
                if gtn > amount_of_recs:
                    dbs.rollback()
                    flask.flash("not enough of goods of said amount in warehouses")
                    return flask.redirect("/")
                for idx, rec in enumerate(recs):
                    if idx == gtn:
                        break
                    stmt = sa.update(record).where(record.id == rec.id).values(issue_rec = q.id)
                    dbs.execute(stmt)
                    k = record_ops(
                        record_id = rec.id,
                        ops_id = op.id
                    )
                    dbs.add(k)
            dbs.commit()
            flask.flash("stock issue created")
            return flask.redirect("/")
        except:
            flask.flash("error creating the issue. Contact your system administrator")
            return flask.redirect("/")
    else:
        try:
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
            goods = dbs.query(good_type, sa.func.count(record.id)).join(record).where(record.issue_rec == None).group_by(record.type)
            print(goods)
            for good in goods:
                list_g.append({'id': good.good_type.id, 'name':good.good_type.name, 'ean': good.good_type.ean, 'amount': good[1]})
            dbs.commit()
            return flask.render_template("issue.html",  suppliers = list_s, users = list_u, positions = list_p, goods = list_g)
        except:
            flask.flash("cannot load website. contact your system administrator")
            return flask.redirect("/")
@app.route("/move", methods=["POST","GET"])
@login_required
def movcre():
    if flask.request.method == "POST":
        endpos = flask.request.form.get("endpos")
        usera = flask.session["user_id"]
        if flask.request.form.get("uu") == "any":
            usere = sa.sql.null()
        else:
            usere = flask.request.form.get("uu")
        if not flask.request.form.get("comment"):
            com = sa.sql.null()
        else:
            com = flask.request.form.get("comment")
        recs = flask.request.form.getlist("recon")
        try:
            dbs.begin()
            q = move(
                end_pos = endpos,
                user_approving = usera,
                comment = com,
                user_executing = usere
            )
            dbs.add(q)
            dbs.flush()
            for rec in recs:
                sp = dbs.scalar(sa.select(record.current_position).where(record.id == rec))
                r = move__record(
                    move_id = q.id,
                    record_id = rec,
                    start_pos = sp,
                    end_pos = endpos,
                )
                dbs.add(r)
            dbs.commit()
            flask.flash("move action succesfuly created")
            return flask.redirect("/")
        except:
            flask.flash("error while creating a move action")
            return flask.redirect("/")
    else:
        try:
            dbs.begin()
            positions = dbs.scalars(sa.select(position))
            list_p = []
            for pos in positions:
                list_p.append({'id': pos.id, 'row': pos.row, 'column': pos.column, 'cell': pos.cell, 'zone': pos.zone, 'warehouse_pos': pos.warehouse_pos})
            records = dbs.scalars(sa.select(record))
            list_r = []
            for rec in records:
                list_r.append({'id': rec.id, 'type': rec.type, 'current_position': rec.current_position})
            users = dbs.scalars(sa.select(user))
            list_u = []
            for u in users:
                list_u.append({'id': u.id, 'name': u.name, 'first_name': u.first_name, 'last_name': u.last_name})
            dbs.commit()
            return flask.render_template("move.html", positions = list_p, record = list_r, users = list_u)
        except:
            flask.flash("cannot load website. contact your system administrator")
            return flask.redirect('/')
@app.route("/lookup", methods=["GET","POST"])
@login_required
def loku():
    if flask.request.method == "POST":
        if not flask.request.form.get("idl"):
            flask.flash("query not valid")
            return flask.redirect("/")
        que = flask.request.form.get("idl")
        qq = que.split("-")
        if not (qq[0] == "rec" or qq[0] == "iss" or qq[0] == "mov" or qq[0] == "pos" or qq[0] == "rei" or qq[0] == "typ"):
            flask.flash("prefix not valid")
            return flask.redirect("/")
        return flask.redirect("/lkres?t={}&id={}".format(qq[0],qq[1]))
    return flask.render_template("lookup.html")
@app.route("/lkres", methods = ["GET"])
@login_required
def lokres():
    tt = flask.request.args.get("t")
    ii = flask.request.args.get("id")
    if tt == "rec":
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(record).where(record.id == ii)).first()
            if not q:
                raise
            r = dbs.scalars(sa.select(move).join(move__record).where(move__record.record_id == q.id))
            return flask.render_template("rec-res.html", rec = q, moves = r), dbs.commit()
        except:
            flask.flash("cannot load lookup. check your id")
            return flask.redirect("/")
    elif tt == "iss":
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(issue).where(issue.id == ii)).first()
            if not q:
                raise
            r = dbs.scalars(sa.select(record).where(record.issue_rec == q.id)).all()
            return flask.render_template("iss-res.html", iss = q, recs = r), dbs.commit()
        except:
            flask.flash("cannot load lookup. check your id")
            return flask.redirect("/")
    elif tt == "rei":
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(receipt).where(receipt.id == ii)).first()
            if not q:
                raise
            r = dbs.scalars(sa.select(record).where(record.receipt_rec == q.id)).all()
            return flask.render_template("rei-res.html", rei = q, recs = r), dbs.commit()
        except:
            flask.flash("cannot load lookup. check your id")
            return flask.redirect("/")
    elif tt == "mov":
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(move).where(move.id == ii)).first()
            if not q:
                raise
            r = dbs.scalars(sa.select(move__record).where(move__record.move_id == q.id)).all()
            return flask.render_template("mov-res.html", mov = q, recs = r), dbs.commit()
        except:
            flask.flash("cannot load lookup. check your id")
            return flask.redirect("/")
    elif tt == "pos": 
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(position).where(position.id == ii)).first()
            if not q:
                raise
            r = dbs.scalars(sa.select(record).where(record.current_position == q.id)).all()
            return flask.render_template("pos-res.html", pos = q, recs = r), dbs.commit()
        except:
            flask.flash("cannot load lookup. check your id")
            return flask.redirect("/")   
    elif tt == "typ":
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(good_type).where(good_type.id == ii)).first()
            if not q:
                raise
            r = dbs.scalars(sa.select(record).where(record.type == q.id)).all()
            return flask.render_template("typ-res.html", typ = q, recs = r), dbs.commit()
        except:
            flask.flash("cannot load lookup. check your id")
            return flask.redirect("/")
    else:
        flask.flash("cannot load lookup. check your id and type")
        return flask.redirect("/")
@app.route("/register", methods = ["GET","POST"])
@login_required
def register():
    if flask.request.method == "POST":
        try:
            if not flask.request.form.get("name"):
                raise
            else:
                nn = flask.request.form.get("name")
            if not flask.request.form.get("password"):
                raise
            else:
                ps = flask.request.form.get("password")
            if not flask.request.form.get("mail"):
                mail = sa.sql.null()
            else:
                mail = flask.request.form.get("mail")
            if not flask.request.form.get("phone"):
                phone = sa.sql.null()
            else:
                phone = flask.request.form.get("phone")
            if not flask.request.form.get("fname"):
                fname = sa.sql.null()
            else:
                fname = flask.request.form.get("fname")
            if not flask.request.form.get("lname"):
                lname = sa.sql.null()
            else:
                lname = flask.request.form.get("lname")
            if not flask.request.form.getlist("tt"):
                raise
            else:
                tt = flask.request.form.getlist("tt")
            dbs.begin()
            q = user(
                name = nn,
                hash = generate_password_hash(ps, method='pbkdf2:sha256', salt_length=8),
                mail = mail,
                phone = phone,
                first_name = fname,
                last_name = lname
            )
            dbs.add(q)
            dbs.flush()
            for t in tt:
                w = user__user_type(
                    user_id = q.id,
                    type_id = int(t)
                )
                dbs.add(w)
            flask.flash("user created")
            dbs.commit()
            return flask.redirect("/")
        except:
            flask.flash("error creating a user")
            return flask.redirect("/")
    else:
        try:
            dbs.begin()
            q = dbs.scalars(sa.select(user_type))
            return flask.render_template("register.html", types = q), dbs.commit()
        except:
            flask.flash("cannot load website. contact your system administrator")
            return flask.redirect("/")
@app.route("/test")
def test():
    label = blabel.LabelWriter("./templates/labels/label_move.html", default_stylesheets=("./static/label_a4.css",))
    records = [
        dict(sample_id="2137", sample_name = "lalala")
    ]
    return label.write_labels(records, target="test.pdf")