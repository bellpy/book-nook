from booknook.db import get_db
from psycopg2.extras import RealDictCursor

class BookModel:

    @staticmethod
    def get_all(bid):
        db = get_db()
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT * FROM book WHERE user_id = %s ORDER BY created DESC
                """,
                (bid,)
                )
            return cur.fetchall()

    @staticmethod
    def get_by_id(book_id):
        db = get_db()
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM book WHERE id = %s",
                (book_id,),
            )
            return cur.fetchone()

    @staticmethod
    def create(title, author, review, rating, user_id):
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO book (title, author, review, rating, user_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (title, author, review, rating, user_id),
            )

    @staticmethod
    def update(book_id, title, author, review, rating):
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                """
                UPDATE book
                SET title=%s, author=%s, review=%s, rating=%s
                WHERE id=%s
                """,
                (title, author, review, rating, book_id),
            )

    @staticmethod
    def delete(book_id):
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                "DELETE FROM book WHERE id = %s",
                (book_id,)
            )
        db.commit()

    @staticmethod
    def get_fav_books():
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT * FROM book 
                WHERE rating = (SELECT MAX(rating) AS highest_rating 
                FROM book)
                ORDER BY created DESC
                """
            )

            return cur.fetchall()