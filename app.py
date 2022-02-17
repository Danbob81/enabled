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
    """render login page"""
    return render_template("login.html")


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

    return render_template("login.html")


@app.route("/get_users")
def get_users():
    """retrieve user information from db"""
    employees = list(mongo.db.users.find())
    return render_template("create_user.html", employees=employees)


@app.route("/users", methods=["GET", "POST"])
def users():
    """create user logins"""
    if request.method == "POST":
        # check if username already in db
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
        return redirect(url_for("get_users"))

    return render_template("create_user.html")


@app.route("/edit_user/<employee_id>", methods=["GET", "POST"])
def edit_user(employee_id):
    """edit user details"""
    if request.method == "POST":
        submit = {
            "username": request.form.get("username").lower(),
            "password": request.form.get("password"),
            "employee_name": request.form.get("employee_name"),
            "employee_email": request.form.get("employee_email")
        }
        mongo.db.users.update_one(
            {"_id": ObjectId(employee_id)}, {"$set": submit})

        flash("User successfully updated!")
        employees = list(mongo.db.users.find())
        return render_template("create_user.html", employees=employees)

    employee = mongo.db.users.find_one({"_id": ObjectId(employee_id)})
    return render_template("edit_user.html", employee=employee)


@app.route("/delete_user/<employee_id>")
def delete_user(employee_id):
    """remove user from db"""
    mongo.db.users.delete_one({"_id": ObjectId(employee_id)})
    flash("User deleted!")
    employees = list(mongo.db.users.find())
    return render_template("create_user.html", employees=employees)


@app.route("/logout")
def logout():
    """log user out of account"""
    flash("You have logged out!")
    session.pop("user")
    return redirect(url_for('login'))


@app.route("/account")
def account():
    """return account page"""
    return render_template("account.html")


# @app.route("/get_customers")
# def get_customers():
#     """retrieve customer record from db"""
#     customers = list(mongo.db.customers.find())
#     return render_template("account.html", customers=customers)


@app.route("/search_customer", methods=["GET", "POST"])
def search_customer():
    """query db for customer details"""
    query = request.form.get("query")
    customers = list(mongo.db.customers.find({"$text": {"$search": query}}))
    return render_template("account.html", customers=customers)


@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    """create customer record in db"""
    if request.method == "POST":
        customer = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "address_street": request.form.get("address_street"),
            "address_city": request.form.get("address_city"),
            "address_county": request.form.get("address_county"),
            "postcode": request.form.get("postcode"),
            "tenure": request.form.get("tenure"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "created_by": session["user"],
            "amended_by": session["user"]
        }
        mongo.db.customers.insert_one(customer)
        flash("Customer Record Successfully Created")
        return redirect(url_for("account"))

    return render_template("account.html")


@app.route("/customer_record")
def customer_record():
    """render customer record page"""
    query = request.form.get("query")
    customers = list(mongo.db.customers.find({"$text": {"$search": query}}))
    return render_template("customer.html", customers=customers)


@app.route("/edit_customer/<customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    """edit customer details"""
    if request.method == "POST":
        submit = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "address_street": request.form.get("address_street"),
            "address_city": request.form.get("address_city"),
            "address_county": request.form.get("address_county"),
            "postcode": request.form.get("postcode"),
            "tenure": request.form.get("tenure"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "amended_by": session["user"]
        }
        mongo.db.customers.update_one(
            {"_id": ObjectId(customer_id)}, {"$set": submit})

        flash("Customer Details Successfully Updated!")
        customers = list(mongo.db.customers.find())
        return render_template("account.html", customers=customers)

    customer = mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
    return render_template("edit_customer.html", customer=customer)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
