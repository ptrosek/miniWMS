import flask
from flask_session import Session


app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False

Session(app)

@app.route("/")
def test():
    return flask.render_template("layout.html")