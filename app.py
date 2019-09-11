from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
    {
        "name": "Store 1",
        "items": [
            {
                "name": "Item 1",
                "price": 15.99
            }
        ]
    }
]


@app.route('/')
def home():
    return 'Hello World!'


@app.route('/store', methods=["GET"])
def get_stores():
    return jsonify({"stores": stores})


@app.route('/store/<string:name>', methods=["GET"])
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)

        return jsonify({"message": "Store not found"})


@app.route('/store', methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }

    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>/item', methods=["GET"])
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})

        return jsonify({"message": "Store not found"})


@app.route('/store/<string:name>/item', methods=["POST"])
def create_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            request_data = request.get_json()
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            
            store["items"].append(new_item)
            return jsonify({"message": "Item added successfully"}, new_item)

        return jsonify({"message": "Store not found"})


if __name__ == '__main__':
    app.run(port=5000)
