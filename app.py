import os

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from application.security import authenticate, identity
from application._resources.user_register import UserRegister
from application._resources.item import Item, ItemList
from application._resources.store import Store, StoreList
from application._static.configuration import dbLocation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///application/_static/data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret_key"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    from application.db import db # import here due to circular import
    db.init_app(app)
    app.run(port=5000, debug=True)