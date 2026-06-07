CREATE TABLE users(
  id       INTEGER      UNIQUE PRIMARY KEY AUTOINCREMENT,
  username VARCHAR[64]  UNIQUE NOT NULL,
  email    VARCHAR[64]  UNIQUE NOT NULL,
  /* Insecure but this is not a CyberSec Course */
  password VARCHAR[64]  NOT NULL
)
