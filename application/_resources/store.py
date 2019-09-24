from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from .._models.store import StoreModel

from .._static.configuration import dbLocation


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {"message": "Store not found."}, 404


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating the store."}, 500

        return store, 201


    def put(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "A store with naem '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating the store."}, 500

        return {"message": "Store added."}, 200


    def delete(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted."}, 204



class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}, 200