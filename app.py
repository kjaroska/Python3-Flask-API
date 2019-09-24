import os

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from application._resources.user_register import UserRegister, User, UserLogin
from application._resources.item import Item, ItemList
from application._resources.store import Store, StoreList
from application._static.configuration import dbLocation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///application/_static/data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True # Flask extensions can return their internal exceptions and custom errors
app.secret_key = "secret_key"
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity): #identity => user.id
    if identity == 1: #configurable
        return {"is_admin": True}
    
    return {"is_admin": False}
    

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

@app.route('/')
def home():
    return render_template("index.html")

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from application.db import db # import here due to circular import
    db.init_app(app)
    app.run(port=5000, debug=True)