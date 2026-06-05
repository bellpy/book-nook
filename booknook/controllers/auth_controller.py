from flask import Blueprint, render_template, request, redirect, url_for, session
from booknook.models.user_model import UserModel

bp = Blueprint("auth", __name__,) #url_prefix="/auth"

@bp.route("/")
@bp.route("/home")
def home():

    return render_template('auth/home.html')

@bp.route("/auth/login", methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = UserModel.login(username=username, password=password)

        if user:
            session['user'] = user[0]
            return redirect(url_for('books.index'))
        else: 
            ret_str = "Invalid login. Try again."
            return render_template('auth/login.html', data=ret_str)
        
    else:
        ret_str = "Log In"
        return render_template('auth/login.html', data=ret_str)
    
@bp.route("/auth/register", methods=("GET", "POST"))
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        if UserModel.get_by_username(username=username):
            ret_str = "Username already in use. Try again."
            return render_template('auth/register.html', data=ret_str)
        else:
            UserModel.create(username=username, password=password)
            session['user'] = UserModel.login(username=username, password=password)[0]
            return redirect(url_for('books.index'))
    else:
        ret_str = "Sign Up"
        return render_template('auth/register.html', data=ret_str)