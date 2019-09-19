import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from ..resources.configuration import dbLocation


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank!")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(dbLocation)
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name),)
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert_item(cls, new_item):
        connection = sqlite3.connect(dbLocation)
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (new_item["name", new_item["price"]]))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect(dbLocation)
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()



    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item

        return {"message": "Item not found."}, 404


    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        new_item = {"name": name, "price": data["price"]}

        try:
            self.insert_item(new_item)
        except:
            return {"message": "An error occured inserting the item."}, 500

        return new_item, 201


    def delete(self, name):
        connection = sqlite3.connect("/")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "Item deleted"}, 204


    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                self.insert_item(updated_item)
            except:
                return {"message": "An error occured inserting the item."}, 500
        else:
            try:
                self.update_item(updated_item)
            except:
                return {"message": "An error occured updating the item."}, 500

        return updated_item



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect(dbLocation)
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})
        
        connection.close()
        return {"items": items}, 200