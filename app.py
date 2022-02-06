import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
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
    return render_template("home.html")


@app.route("/customer")
def customer():
    return render_template("customer.html")


@app.route("/staff")
def staff():
    return render_template("staff.html")


@app.route("/login_staff", methods=["GET", "POST"])
def login_staff():
    if request.method == "POST":
        # check user is in db
        existing_user = mongo.db.users_staff.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check if passwords match
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(
                    url_for('account', username=session["user"]))

            else:
                # no password match
                flash("Incorrect username and/or password!")
                return redirect(url_for("staff"))

        else:
            # invalid username
            flash("Incorrect username and/or password!")
            return redirect(url_for("staff"))

    return render_template("staff_account.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if user is already in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists!")
            return redirect(url_for('home'))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put new user into session cookie
        session["user"] = request.form.get("username").lower()
        flash("Account successfully created!")
        return redirect(url_for('account', username=session["user"]))

    return render_template("account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check username is in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check password match
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(
                    url_for('account', username=session["user"]))

            else:
                # no password match
                flash("Incorrect username and/or password!")
                return redirect(url_for("login"))

        else:
            # invalid username
            flash("Incorrect username and/or password!")
            return redirect(url_for("login"))

    return render_template("account.html")


@app.route("/account/<username>", methods=["GET", "POST"])
def account(username):
    # get username from db
    username = mongo.db.staff_users.find_one(
        {"username": session["staff_user"]})["username"]
    return render_template("account.html", username=username)


@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        # check username is in db
        existing_user = mongo.db.staff_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check password match
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["staff_user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(
                        url_for('account', username=session["staff_user"]))

            else:
                # no password match
                flash("Incorrect username and/or password!")
                return redirect(url_for("staff"))

        else:
            # invalid username
            flash("Incorrect username and/or password!")
            return redirect(url_for("staff"))

    return render_template("account.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
