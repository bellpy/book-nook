from flask import Blueprint, render_template, request, redirect, url_for, session
from booknook.models.book_model import BookModel
import re

bp = Blueprint("books", __name__)


@bp.route("/index")
def index():
    books = BookModel.get_all(session["user"])
    return render_template("index.html", books=books)


@bp.route("/search")
def search():
    query = request.args.get("q", "")
    books = BookModel.get_all(session["user"])

    if query:
        pattern = re.compile(query, re.IGNORECASE)
        books = [
            b for b in books
            if pattern.search(b.get("title", "")) or pattern.search(b.get("author_name", ""))
        ]

    return render_template("index.html", books=books, query=query)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        genres = request.form.get("genres")

        BookModel.create(
            title=request.form["title"],
            isbn=request.form.get("isbn"),
            page_count=request.form.get("page_count"),
            author_name=request.form["author"],
            user_id=session["user"],
            genres=genres,
            rating=request.form.get("rating"),
            review_text=request.form.get("review"),
            status="read"
        )

        return redirect(url_for("books.index"))

    return render_template("create.html")


@bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    book = BookModel.get_by_id(id)

    if request.method == "POST":

        genres = request.form.get("genres")

        BookModel.update(
            book_id=id,
            title=request.form["title"],
            isbn=request.form.get("isbn"),
            page_count=request.form.get("page_count"),
            author_name=request.form["author"],
            genres=genres,  # ✅ NEW
            rating=request.form.get("rating"),
            review_text=request.form.get("review")
        )

        return redirect(url_for("books.detail", id=id))

    return render_template("update.html", book=book)

@bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    BookModel.delete(id)
    return redirect(url_for("books.index"))


@bp.route("/book/<int:id>")
def detail(id):
    book = BookModel.get_by_id(id)
    return render_template("detail.html", book=book)


@bp.route("/dashboard")
def fav_books():
    books = BookModel.get_fav_books()
    top_genre = BookModel.get_top_genre(session["user"])
    return render_template("stats.html", books=books, top_genre=top_genre)