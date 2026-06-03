DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS "user";

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    review TEXT,
    rating INTEGER,
    user_id INTEGER REFERENCES "user"(id),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);