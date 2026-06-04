from booknook.db import get_db
import random

class UserModel:

    @staticmethod
    def get_by_username(username):
        db = get_db()

        with db.cursor() as cur: 
            cur.execute(
                """
                SELECT * FROM "user" WHERE username = %s
                """,
                (username,)
            )
            return cur.fetchone()
    
    @staticmethod
    def create(username, password):
        db = get_db()

        with db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO "user" (id, username, password)
                VALUES (%s, %s, %s)
                """,
                (random.randint(3, 100), username, password)
            )

    @staticmethod
    def login(username, password):
        db = get_db()

        with db.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM "user" WHERE username = %s AND password = %s
                """,
                (username, password)
            )
            return cur.fetchone()