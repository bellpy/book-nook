from booknook.db import get_db
from psycopg2.extras import RealDictCursor


class BookModel:

    @staticmethod
    def get_all(user_id):
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    b.*,
                    a.name AS author_name,
                    ub.status
                FROM book b
                LEFT JOIN author a ON b.author_id = a.id
                LEFT JOIN user_book ub ON ub.book_id = b.id
                WHERE ub.user_id = %s
                ORDER BY b.created DESC
            """, (user_id,))

            return cur.fetchall()

    @staticmethod
    def get_by_id(book_id):
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    b.*,
                    a.name AS author_name
                FROM book b
                LEFT JOIN author a ON b.author_id = a.id
                WHERE b.id = %s
            """, (book_id,))

            book = cur.fetchone()

            # attach genres
            cur.execute("""
                SELECT g.name
                FROM genre g
                JOIN book_genre bg ON bg.genre_id = g.id
                WHERE bg.book_id = %s
            """, (book_id,))

            book["genres"] = [g["name"] for g in cur.fetchall()]

            # attach reviews
            cur.execute("""
                SELECT r.*, u.username
                FROM review r
                JOIN "user" u ON u.id = r.user_id
                WHERE r.book_id = %s
                ORDER BY r.created DESC
            """, (book_id,))

            book["reviews"] = cur.fetchall()

            return book

    @staticmethod
    def create(title, isbn, page_count, author_name, user_id, genres=None, rating=None, review_text=None, status="read"):
        db = get_db()

        with db.cursor() as cur:

            # 1. get or create author
            cur.execute("SELECT id FROM author WHERE name = %s", (author_name,))
            author = cur.fetchone()

            if author:
                author_id = author[0]
            else:
                cur.execute(
                    "INSERT INTO author (name) VALUES (%s) RETURNING id",
                    (author_name,)
                )
                author_id = cur.fetchone()[0]

            # 2. create book
            cur.execute("""
                INSERT INTO book (title, isbn, page_count, author_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (title, isbn, page_count, author_id))

            book_id = cur.fetchone()[0]

            # 3.5 handle genres
            if genres:
                genre_list = [g.strip() for g in genres.split(",") if g.strip()]

                for genre_name in genre_list:

                    # get or create genre
                    cur.execute("SELECT id FROM genre WHERE name = %s", (genre_name,))
                    genre = cur.fetchone()

                    if genre:
                        genre_id = genre[0]
                    else:
                        cur.execute(
                            "INSERT INTO genre (name) VALUES (%s) RETURNING id",
                            (genre_name,)
                        )
                        genre_id = cur.fetchone()[0]

                    # link book ↔ genre
                    cur.execute("""
                        INSERT INTO book_genre (book_id, genre_id)
                        VALUES (%s, %s)
                    """, (book_id, genre_id))

            # 3. user-book relation
            cur.execute("""
                INSERT INTO user_book (user_id, book_id, status)
                VALUES (%s, %s, %s)
            """, (user_id, book_id, status))

            # 4. optional review
            if rating or review_text:
                cur.execute("""
                    INSERT INTO review (user_id, book_id, rating, text)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, book_id, rating, review_text))

        db.commit()

    @staticmethod
    def update(book_id, title, isbn, page_count, author_name, genres=None, rating=None, review_text=None):
        db = get_db()

        with db.cursor() as cur:

            # --- 1. get or create author ---
            cur.execute("SELECT id FROM author WHERE name = %s", (author_name,))
            author = cur.fetchone()

            if author:
                author_id = author[0]
            else:
                cur.execute(
                    "INSERT INTO author (name) VALUES (%s) RETURNING id",
                    (author_name,)
                )
                author_id = cur.fetchone()[0]

            # --- 2. update book ---
            cur.execute("""
                UPDATE book
                SET title=%s,
                    isbn=%s,
                    page_count=%s,
                    author_id=%s
                WHERE id=%s
            """, (title, isbn, page_count, author_id, book_id))

            # --- 3. update genres (replace strategy) ---
            if genres is not None:
                # remove old links
                cur.execute("DELETE FROM book_genre WHERE book_id = %s", (book_id,))

                genre_list = [g.strip() for g in genres.split(",") if g.strip()]

                for genre_name in genre_list:

                    cur.execute("SELECT id FROM genre WHERE name = %s", (genre_name,))
                    genre = cur.fetchone()

                    if genre:
                        genre_id = genre[0]
                    else:
                        cur.execute(
                            "INSERT INTO genre (name) VALUES (%s) RETURNING id",
                            (genre_name,)
                        )
                        genre_id = cur.fetchone()[0]

                    cur.execute("""
                        INSERT INTO book_genre (book_id, genre_id)
                        VALUES (%s, %s)
                    """, (book_id, genre_id))

            # --- 4. update review (replace user's review for this book) ---
            if rating or review_text:

                # get user_id for this book-user relationship
                cur.execute("""
                    SELECT user_id
                    FROM user_book
                    WHERE book_id = %s
                    LIMIT 1
                """, (book_id,))

                user_row = cur.fetchone()

                if user_row:
                    user_id = user_row[0]

                    # delete old review by this user for this book
                    cur.execute("""
                        DELETE FROM review
                        WHERE book_id = %s AND user_id = %s
                    """, (book_id, user_id))

                    # insert updated review
                    cur.execute("""
                        INSERT INTO review (user_id, book_id, rating, text)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, book_id, rating, review_text))

            db.commit()

    @staticmethod
    def delete(book_id):
        db = get_db()

        with db.cursor() as cur:
            cur.execute("DELETE FROM review WHERE book_id = %s", (book_id,))
            cur.execute("DELETE FROM user_book WHERE book_id = %s", (book_id,))
            cur.execute("DELETE FROM book_genre WHERE book_id = %s", (book_id,))
            cur.execute("DELETE FROM book WHERE id = %s", (book_id,))

        db.commit()

    @staticmethod
    def get_fav_books():
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT b.*, AVG(r.rating) AS avg_rating
                FROM book b
                JOIN review r ON r.book_id = b.id
                GROUP BY b.id
                ORDER BY avg_rating DESC NULLS LAST
            """)

            return cur.fetchall()
        
    @staticmethod
    def get_top_genre(user_id):
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT g.name, COUNT(*) AS count
                FROM genre g
                JOIN book_genre bg ON g.id = bg.genre_id
                JOIN user_book ub ON ub.book_id = bg.book_id
                WHERE ub.user_id = %s
                GROUP BY g.name
                ORDER BY count DESC
                LIMIT 1
            """, (user_id,))

            return cur.fetchone()