import os
from pathlib import Path
import sqlite3

DATABASE_PATH = "app.db"

class Database:
    def __init__(self):
        self.connection = init_database()

    def query(self, query: str, parameters = ()) -> sqlite3.Cursor:
        return self.connection.cursor().execute(query, parameters)

    def commit(self):
        self.connection.commit()

def init_database() -> sqlite3.Connection:
    if Path(DATABASE_PATH).exists():
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        return connection

    print("New database. Applying db-init/*.sql")
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    cur = connection.cursor()
    for path in os.listdir("db-init"):
        with open(f"db-init/{path}", "r") as file:
            print(f"Applying {path}...")
            _ = cur.execute(file.read())
    connection.commit()
    return connection

def fill_database_with_mock_data():
    raise NotImplemented()