from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db

bp = Blueprint("books", __name__)

@bp.route("/")
def index():
    db = get_db()
    books = db.execute(
        "SELECT * FROM book ORDER BY created DESC"
    ).fetchall()

    return render_template("books/index.html", books=books)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        review = request.form["review"]
        rating = request.form.get("rating")

        db = get_db()
        db.execute(
            "INSERT INTO book (title, author, review, rating, user_id) VALUES (?, ?, ?, ?, ?)",
            (title, author, review, rating, 1),  # temp user_id
        )
        db.commit()

        return redirect(url_for("books.index"))

    return render_template("books/create.html")


@bp.route("/update/<int:id>", methods=("GET", "POST"))
def update(id):
    db = get_db()
    book = db.execute(
        "SELECT * FROM book WHERE id = ?", (id,)
    ).fetchone()

    if request.method == "POST":
        db.execute(
            "UPDATE book SET title=?, author=?, review=?, rating=? WHERE id=?",
            (
                request.form["title"],
                request.form["author"],
                request.form["review"],
                request.form.get("rating"),
                id,
            ),
        )
        db.commit()

        return redirect(url_for("books.index"))

    return render_template("books/update.html", book=book)