import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_change_password import ChangePassword, ChangePasswordForm, SetPasswordForm
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    """render login page"""
    return render_template("login.html")


@app.route("/account")
def account():
    """render users account page"""
    return render_template("account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """log in to user account"""
    if request.method == "POST":
        # check username is in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                # flash("Welcome, {}".format(
                #     request.form.get("username")))
                return redirect(url_for(
                        "login", username=session["user"]))
            else:
                # password doesn't match
                flash("Incorrect Username and/or Password")
                return redirect(url_for('login'))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for('login'))

    return render_template("account.html")


@app.route("/users", methods=["GET", "POST"])
def users():
    """create user logins"""
    if request.method == "POST":
        # check is username already in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("users"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "employee_name": request.form.get("employee_name"),
            "employee_email": request.form.get("employee_email")
        }
        mongo.db.users.insert_one(register)

        flash("User successfully created!")
        return redirect(url_for("users"))

    return render_template("create_user.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """change users password"""
    return render_template("change_password.html")


@app.route("/get_users")
def get_users():
    """retrieve user information"""
    users = list(mongo.db.users.find())
    return render_template("create_user.html", users=users)


@app.route("/logout")
def logout():
    """log user out of account"""
    flash("You have logged out!")
    session.pop("user")
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
