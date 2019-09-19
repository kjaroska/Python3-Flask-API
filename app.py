from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from application.security import authenticate, identity
from application.user_register import UserRegister
from application.models.item import Item, ItemList

app = Flask(__name__)
app.secret_key = "secret_key"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
