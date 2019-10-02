from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    get_jwt_claims,
    get_jwt_identity,
    fresh_jwt_required
)
from .._models.item import ItemModel

from .._static.configuration import dbLocation


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument("store_id", type=int, required=True, help="Every item needs a store id!")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found."}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(name, data["price"], data["store_id"])

        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return new_item, 201


    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            # add store_id update

        item.save_to_db()
        return item.json()


    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privilage required."}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}, 201
        
        return {"message": "Item not found."}, 404

        



class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200

        return {
            "items": [item["name"] for item in items],
            "message": "More data available after loggin in."}, 200