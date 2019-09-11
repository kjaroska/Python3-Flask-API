from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item

        return {"item": name}

    def post(self, name):
        new_item = {"name": name, "price": 15.99}
        items.append(new_item)
        return new_item, 201


api.add_resource(Item, "/item/<string:name>")


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000)
