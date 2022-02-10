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
    """render home page"""
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """log in to user account"""
    if request.method == "POST":
        # check username is in db
        existing_user = mongo.db.users_staff.find_one(
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
                return redirect(url_for('home'))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for('home'))

    return render_template("account.html")


# @app.route("/account", methods=["POST", "GET"])
# def account():
#     """render account page"""
#     return render_template("account.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
