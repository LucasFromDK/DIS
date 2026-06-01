CREATE TABLE users(
  id       INTEGER      UNIQUE PRIMARY KEY AUTOINCREMENT,
  username VARCHAR[64]  UNIQUE NOT NULL,
  email    VARCHAR[64]  UNIQUE NOT NULL,
  /* Insecure asf, but wdgaf */
  password VARCHAR[64]  NOT NULL,
  lastSeen long
)
