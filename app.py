import os

from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

from application._resources.user_register import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from application._resources.item import Item, ItemList
from application._resources.store import Store, StoreList
from application._static.configuration import dbLocation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///application/_static/data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True # Flask extensions can return their internal exceptions and custom errors
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "secret_key"
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity): #identity => user.id
    if identity == 1: #configurable
        return {"is_admin": True}
    
    return {"is_admin": False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

@jwt.expired_token_loader # if user token is expired during request
def expired_token_callback():
    return jsonify({
        "description": "The token has expired.",
        "error": "token_expired"
    }), 401
    
@jwt.invalid_token_loader # user sends non-jwt valid token
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed.",
        "error": "invalid_token"
    }), 401

@jwt.unauthorized_loader # no jwt token in request
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not cointain an access token.",
        "error": "authorization_required"
    }), 401

@jwt.needs_fresh_token_loader
def tokent_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
    }), 401


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

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