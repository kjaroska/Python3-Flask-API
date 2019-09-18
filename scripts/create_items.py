import sqlite3

connection = sqlite3.connect("../resources/data.db")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

insert_item = "INSERT INTO items VALUES (null, 'test', 10.99)"
cursor.execute(insert_item)

connection.commit()
connection.close()
