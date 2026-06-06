-- Reset schema
DROP TABLE IF EXISTS user_book;
DROP TABLE IF EXISTS book_genre;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS "user";

-- Create tables
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE author (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    isbn TEXT,
    page_count INTEGER,
    author_id INTEGER REFERENCES author(id),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    book_id INTEGER REFERENCES book(id),
    rating INTEGER,
    text TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE book_genre (
    book_id INTEGER REFERENCES book(id),
    genre_id INTEGER REFERENCES genre(id),
    PRIMARY KEY (book_id, genre_id)
);

CREATE TABLE user_book (
    user_id INTEGER REFERENCES "user"(id),
    book_id INTEGER REFERENCES book(id),
    status TEXT DEFAULT 'read',
    PRIMARY KEY (user_id, book_id)
);