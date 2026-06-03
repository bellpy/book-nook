from flask import Blueprint, render_template, request, redirect, url_for
from booknook.models.book_model import BookModel

bp = Blueprint("books", __name__)


@bp.route("/")
def index():
    books = BookModel.get_all()

    return render_template(
        "index.html",
        books=books,
    )


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