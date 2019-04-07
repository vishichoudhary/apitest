import apitest.config as config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()


@app.before_request
def before_request():
    if request.mimetype == 'application/json':
        request.body = request.get_json()
    elif request.method == "POST":
        request.body = request.form


@app.route("/", methods=["GET"])
def who():
    return "hello world"
