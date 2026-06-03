from booknook.db import get_db

class UserModel:

    @staticmethod
    def get_by_username(username):
        db = get_db()

        return db.execute(
            "SELECT * FROM user WHERE username = ?",
            (username,),
        ).fetchone()