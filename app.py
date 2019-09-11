from flask import Flask

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
    pass


@app.route('/store/<string:name>', methods=["GET"])
def get_store(name):
    pass


@app.route('/store', methods=["POST"])
def create_store():
    pass


@app.route('/store/<string:name>/item', methods=["GET"])
def get_item_in_store(name):
    pass


if __name__ == '__main__':
    app.run(port=5000)
