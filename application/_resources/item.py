from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from .._models.item import ItemModel

from .._static.configuration import dbLocation


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found."}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(name, data["price"])

        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return new_item, 201


    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"])
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json()


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}, 204



class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200
        # [item.json() for item in ItemModel.query.all()]