import os
from pathlib import Path
import sqlite3
import random
from typing import Any
import tempfile

DATABASE_PATH = os.environ.get("DIS_DATABASE", "app.db")

class Database:
    def __init__(self):
        if not Path(DATABASE_PATH).exists():
            print("New database. Applying db-init/*.sql")
            connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            cur = connection.cursor()
            sql_scripts = os.listdir("db-init")
            sql_scripts.sort()
            for path in sql_scripts:
                with open(f"db-init/{path}", "r") as file:
                    print(f"Applying {path}...")
                    _ = cur.executescript(file.read())
            connection.commit()
            self.connection = connection
            self.fill_with_fake_data()
        else:
            self.connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)


    def query(self, query: str, parameters = ()) -> sqlite3.Cursor:
        return self.connection.cursor().execute(query, parameters)

    def query_json(self,query: str, parameters = ()) -> list[dict[str,Any]]:
        cursor = self.query(query, parameters)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def commit(self):
        self.connection.commit()

    def fill_with_fake_data(self):
        _fill_with_fake_users(self)


def _fill_with_fake_users(database: Database):
    first_names = [
        "John",
        "Jill",
        "Jack",
        "Andrea",
        "Will",
        "Simon",
        "Gwen",
        "Phillip",
        "Water",
    ]
    last_names = [
        "Hancock",
        "Hugh Mann",
        "Reel Per Sun",
        "Nut Bott",
        "J. Fry",
        "Doe",
        "Witherspoon",
        "Bottle",
    ]
    for _ in range(50):
        try:
            name = random.choice(first_names)
            username = name + " " + random.choice(last_names)
            email = f"{name.lower()}{random.randint(111,999)}@di.ku.dk"
            database.query("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, "1234"))
        except:
            pass
    database.commit()

def _fill_with_fake_products(database: Database):
    raise NotImplemented()