from flask import Blueprint, render_template, request, redirect, url_for, session
from booknook.models.user_model import UserModel

bp = Blueprint("auth", __name__)


@bp.route("/")
@bp.route("/home")
def home():
    return render_template("auth/home.html")


@bp.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = UserModel.login(
            username=request.form["username"],
            password=request.form["password"]
        )

        if user:
            session["user"] = user[0]
            return redirect(url_for("books.index"))

        return render_template("auth/login.html", data="Invalid login")

    return render_template("auth/login.html", data="Log In")


@bp.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if UserModel.get_by_username(username):
            return render_template("auth/register.html", data="Username already in use")

        UserModel.create(username, password)
        user = UserModel.login(username, password)
        session["user"] = user[0]

        return redirect(url_for("books.index"))

    return render_template("auth/register.html", data="Sign Up")