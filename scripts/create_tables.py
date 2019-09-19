import sqlite3
from ..resources.configuration import dbLocation

connection = sqlite3.connect(dbLocation)
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()
