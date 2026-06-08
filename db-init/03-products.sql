CREATE TABLE products(
  id          INTEGER         UNIQUE PRIMARY KEY AUTOINCREMENT,
  sellerid    INTEGER         REFERENCES sellers(id) ON DELETE CASCADE,
  name        VARCHAR[100]    NOT NULL,
  description VARCHAR[400]    NOT NULL DEFAULT "",
  price       INTEGER         NOT NULL DEFAULT 0,
  units       INTEGER         NOT NULL DEFAULT 0,
  createdOn   LONG            NOT NULL DEFAULT (STRFTIME('%s', 'now'))
)