from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = "secret_key"
api = Api(app)

items = []


class Item(Resource):
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


class ItemList(Resource):
    def get(self):
        return {"item": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/item/<string:name>")


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000)
