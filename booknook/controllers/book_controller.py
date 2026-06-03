from flask import Blueprint, render_template, request, redirect, url_for
from booknook.models.book_model import BookModel
import re

bp = Blueprint("books", __name__)


@bp.route("/")
def index():
    books = BookModel.get_all()

    return render_template(
        "index.html",
        books=books,
    )

@bp.route("/search")
def search():
    query = request.args.get("q", "")

    books = BookModel.get_all()

    if query:
        pattern = re.compile(query, re.IGNORECASE)

        books = [
            book for book in books
            if pattern.search(book["title"] or "") 
            or pattern.search(book["author"] or "")
        ]

    return render_template("index.html", books=books, query=query)

@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":

        BookModel.create(
            title=request.form["title"],
            author=request.form["author"],
            review=request.form["review"],
            rating=request.form.get("rating"),
            user_id=1,  # placeholder
        )

        return redirect(url_for("books.index"))

    return render_template("create.html")


@bp.route("/update/<int:id>", methods=("GET", "POST"))
def update(id):

    book = BookModel.get_by_id(id)

    if request.method == "POST":

        BookModel.update(
            book_id=id,
            title=request.form["title"],
            author=request.form["author"],
            review=request.form["review"],
            rating=request.form.get("rating"),
        )

        return redirect(url_for("books.index"))

    return render_template(
        "update.html",
        book=book,
    )

@bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    BookModel.delete(id)
    return redirect(url_for("books.index"))

@bp.route("/book/<int:id>")
def detail(id):
    book = BookModel.get_by_id(id)
    print(book)

    return render_template(
        "detail.html",
        book=book
    )