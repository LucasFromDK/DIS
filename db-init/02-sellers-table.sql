CREATE TABLE sellers(
  id              INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
  userid          INTEGER UNIQUE,
  excrow_balance  INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(userid) REFERENCES users(id)
)