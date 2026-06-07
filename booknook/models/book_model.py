from booknook.db import get_db
from psycopg2.extras import RealDictCursor


class BookModel:

    # -- Helpers -- 
    @staticmethod
    def _get_or_create_author(cur, author_name):
        cur.execute(
            """
            INSERT INTO author (name)
            VALUES (%s)
            ON CONFLICT (name)
            DO UPDATE SET name = EXCLUDED.name
            RETURNING id
            """, (author_name,)
        )

        return cur.fetchone()[0]

    @staticmethod
    def _get_or_create_genre(cur, genre_name):
        cur.execute(
            """
            INSERT INTO genre (name)
            VALUES (%s)
            ON CONFLICT (name)
            DO UPDATE SET name = EXCLUDED.name
            RETURNING id
            """, (genre_name,)
        )

        return cur.fetchone()[0]

    @staticmethod
    def _set_genres(cur, book_id, genres):
        cur.execute(
            "DELETE FROM book_genre WHERE book_id = %s",
            (book_id,)
        )

        if not genres:
            return

        genre_list = [g.strip() for g in genres.split(",") if g.strip()]

        for genre_name in genre_list:
            genre_id = BookModel._get_or_create_genre(cur, genre_name)

            cur.execute(
                """
                INSERT INTO book_genre (book_id, genre_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """, (book_id, genre_id)
            )
    
    # -- Queries --
    @staticmethod
    def get_all(user_id):
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    b.*,
                    a.name AS author_name,
                    ub.status
                FROM book b
                LEFT JOIN author a ON b.author_id = a.id
                LEFT JOIN user_book ub ON ub.book_id = b.id
                WHERE ub.user_id = %s
                ORDER BY b.created DESC
                """, (user_id,)
            )

            return cur.fetchall()

    @staticmethod
    def get_by_id(book_id):
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    b.*,
                    a.name AS author_name
                FROM book b
                LEFT JOIN author a ON b.author_id = a.id
                WHERE b.id = %s
                """, (book_id,)
            )

            book = cur.fetchone()

            if not book:
                return None

            cur.execute(
                """
                SELECT g.name
                FROM genre g
                JOIN book_genre bg ON bg.genre_id = g.id
                WHERE bg.book_id = %s
                """, (book_id,)
            )

            book["genres"] = [row["name"] for row in cur.fetchall()]

            cur.execute(
                """
                SELECT r.*, u.username
                FROM review r
                JOIN "user" u ON u.id = r.user_id
                WHERE r.book_id = %s
                ORDER BY r.created DESC
                """, (book_id,)
            )

            book["reviews"] = cur.fetchall()

            return book

    @staticmethod
    def create(
        title,
        isbn,
        page_count,
        author_name,
        user_id,
        genres=None,
        rating=None,
        review_text=None,
        status="read"
    ):
        db = get_db()

        with db:
            with db.cursor() as cur:

                author_id = BookModel._get_or_create_author(
                    cur,
                    author_name
                )

                cur.execute(
                    """
                    INSERT INTO book (
                        title,
                        isbn,
                        page_count,
                        author_id
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        title,
                        isbn,
                        page_count,
                        author_id
                    )
                )

                book_id = cur.fetchone()[0]

                BookModel._set_genres(
                    cur,
                    book_id,
                    genres
                )

                cur.execute(
                    """
                    INSERT INTO user_book (
                        user_id,
                        book_id,
                        status
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        user_id,
                        book_id,
                        status
                    )
                )

                if rating is not None or review_text:
                    cur.execute(
                        """
                        INSERT INTO review (
                            user_id,
                            book_id,
                            rating,
                            text
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            user_id,
                            book_id,
                            rating,
                            review_text
                        )
                    )

    @staticmethod
    def update(
        book_id,
        title,
        isbn,
        page_count,
        author_name,
        genres=None,
        rating=None,
        review_text=None
    ):
        db = get_db()

        with db:
            with db.cursor() as cur:

                author_id = BookModel._get_or_create_author(
                    cur,
                    author_name
                )

                cur.execute(
                    """
                    UPDATE book
                    SET
                        title = %s,
                        isbn = %s,
                        page_count = %s,
                        author_id = %s
                    WHERE id = %s
                    """,
                    (
                        title,
                        isbn,
                        page_count,
                        author_id,
                        book_id
                    )
                )

                if genres is not None:
                    BookModel._set_genres(
                        cur,
                        book_id,
                        genres
                    )

                if rating is not None or review_text:

                    cur.execute(
                        """
                        SELECT user_id
                        FROM user_book
                        WHERE book_id = %s
                        LIMIT 1
                        """,
                        (book_id,)
                    )

                    user_row = cur.fetchone()

                    if user_row:
                        user_id = user_row[0]

                        cur.execute(
                            """
                            DELETE FROM review
                            WHERE book_id = %s
                            AND user_id = %s
                            """,
                            (
                                book_id,
                                user_id
                            )
                        )

                        cur.execute(
                            """
                            INSERT INTO review (
                                user_id,
                                book_id,
                                rating,
                                text
                            )
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                user_id,
                                book_id,
                                rating,
                                review_text
                            )
                        )

    @staticmethod
    def delete(book_id):
        db = get_db()

        with db:
            with db.cursor() as cur:
                cur.execute("DELETE FROM review WHERE book_id = %s", (book_id,))
                cur.execute("DELETE FROM book_genre WHERE book_id = %s", (book_id,))
                cur.execute("DELETE FROM user_book WHERE book_id = %s", (book_id,))
                cur.execute("DELETE FROM book WHERE id = %s", (book_id,))

    @staticmethod
    def get_fav_books():
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    b.id,
                    b.title,
                    b.created,
                    a.name AS author_name,
                    COALESCE(AVG(r.rating), 0) AS avg_rating
                FROM book b
                LEFT JOIN review r ON r.book_id = b.id
                LEFT JOIN author a ON b.author_id = a.id
                GROUP BY b.id, a.name
                ORDER BY avg_rating DESC NULLS LAST
            """)

            return cur.fetchall()
        
    @staticmethod
    def get_top_genre(user_id):
        db = get_db()

        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    g.name,
                    COUNT(*) AS count
                FROM genre g
                JOIN book_genre bg
                    ON g.id = bg.genre_id
                JOIN user_book ub
                    ON ub.book_id = bg.book_id
                WHERE ub.user_id = %s
                GROUP BY g.name
                ORDER BY count DESC
                LIMIT 1
                """,
                (user_id,)
            )

            return cur.fetchone()