from booknook.db import get_db

class UserModel:

    @staticmethod
    def get_by_username(username):
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                'SELECT * FROM "user" WHERE username = %s',
                (username,)
            )
            return cur.fetchone()

    @staticmethod
    def create(username, password):
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                'INSERT INTO "user" (username, password) VALUES (%s, %s)',
                (username, password)
            )
        db.commit()

    @staticmethod
    def login(username, password):
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                'SELECT * FROM "user" WHERE username = %s AND password = %s',
                (username, password)
            )
            return cur.fetchone()