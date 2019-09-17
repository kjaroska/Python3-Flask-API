from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.debug = True
app.secret_key = "secret_key"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [{"name": "chair", "price": 15.88}]


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404

    def post(self, name):
        item = next(filter(lambda i: i["name"] == name, items), None)
        if item is not None:
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = request.get_json(force=True)
        new_item = {"name": name, "price": data["price"]}
        items.append(new_item)
        return new_item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}, 204

    def put(self, name):
        parser.reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="This field cannot be left blank!")
        data = parser.parse_args()

        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            return item, 201


class ItemList(Resource):
    def get(self):
        return {"item": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000)
