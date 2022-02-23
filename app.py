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


@app.route("/change_password/<employee_id>", methods=["GET", "POST"])
def change_password(employee_id):
    """gives user option to change their password"""
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
                        "change_password", username=session["user"]))
            else:
                # password doesn't match
                flash("Incorrect Password")
                return redirect(url_for('change_password'))

            # check if new passwords match
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            if new_password != confirm_password:
                flash("Your passwords don't match, try again")
                return redirect(url_for("change_password"))

            register_password = {
                "password": generate_password_hash(
                            request.form.get("new_password"))
            }
            mongo.db.users.update_one(
                {"_id": ObjectId(employee_id)}, {"$set": register_password})

            flash("Password changed!")
            employees = list(mongo.db.users.find())
            return render_template("login.html", employees=employees)

    employee = mongo.db.users.find_one({"_id": ObjectId(employee_id)})
    return render_template("change_password.html", employee=employee)


@app.route("/logout")
def logout():
    """log user out of account"""
    flash("You have logged out!")
    session.pop("user")
    return redirect(url_for('login'))


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


@app.route("/search_user", methods=["GET", "POST"])
def search_user():
    """query db for customer details"""
    query = request.form.get("query")
    employees = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("create_user.html", employees=employees)


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
    return redirect(url_for("get_users"))


@app.route("/account")
def account():
    """return account page"""
    return render_template("account.html")


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


@app.route("/view_customer/<customer_id>")
def view_customer(customer_id):
    """retrieve customer information from db"""
    customer = mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
    return render_template("view_customer.html", customer=customer)


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
        customer = mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
        return render_template("edit_customer.html", customer=customer)

    customer = mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
    return render_template("edit_customer.html", customer=customer)


@app.route("/delete_customer/<customer_id>")
def delete_customer(customer_id):
    """remove job from db"""
    mongo.db.customers.delete_one({"_id": ObjectId(customer_id)})
    flash("Customer Account Deleted!")
    return redirect(url_for("account"))


@app.route("/search_jobs", methods=["GET", "POST"])
def search_jobs():
    """query db for job details"""
    query = request.form.get("query")
    jobs = list(mongo.db.jobs.find({"$text": {"$search": query}}))
    return render_template("view_mwos.html", jobs=jobs)


@app.route("/view_jobs/<job_id>")
def view_jobs(job_id):
    """retrieve job information from db"""
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id)})
    return render_template("view_job.html", job=job)


@app.route("/edit_job/<job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    """edit order details"""
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        submit = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "address_street": request.form.get("address_street"),
            "address_city": request.form.get("address_city"),
            "address_county": request.form.get("address_county"),
            "postcode": request.form.get("postcode"),
            "tenure": request.form.get("tenure"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "keysafe": request.form.get("keysafe"),
            "keysafe_text": request.form.get("keysafe_text"),
            "int_grab": request.form.get("int_grab"),
            "int_grab_text": request.form.get("int_grab_text"),
            "ext_grab": request.form.get("ext_grab"),
            "ext_grab_text": request.form.get("ext_grab_text"),
            "drop_rail": request.form.get("drop_rail"),
            "drop_rail_text": request.form.get("drop_rail_text"),
            "newel": request.form.get("newel"),
            "newel_text": request.form.get("newel_text"),
            "stair_rail": request.form.get("stair_rail"),
            "stair_rail_text": request.form.get("stair_rail_text"),
            "handrail": request.form.get("handrail"),
            "handrail_text": request.form.get("handrail_text"),
            "step": request.form.get("step"),
            "step_text": request.form.get("step_text"),
            "ramp": request.form.get("ramp"),
            "ramp_text": request.form.get("ramp_text"),
            "shower": request.form.get("shower"),
            "shower_text": request.form.get("shower_text"),
            "other": request.form.get("other"),
            "other_text": request.form.get("other_text"),
            "ref_name": request.form.get("ref_name"),
            "team": request.form.get("team"),
            "ref_email": request.form.get("ref_email"),
            "ref_phone": request.form.get("ref_phone"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "amended_by": session["user"]
        }
        mongo.db.jobs.update_one(
            {"_id": ObjectId(job_id)}, {"$set": submit})

        flash("Minor Works Order Successfully Updated!")
        job = mongo.db.jobs.find_one({"_id": ObjectId(job_id)})
        return render_template("edit_job.html", job=job)

    job = mongo.db.job.find_one({"_id": ObjectId(job_id)})
    return render_template("edit_job.html", job=job)


@app.route("/add_job/<customer_id>", methods=["GET", "POST"])
def add_job(customer_id):
    """create job order record"""
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        job = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "address_street": request.form.get("address_street"),
            "address_city": request.form.get("address_city"),
            "address_county": request.form.get("address_county"),
            "postcode": request.form.get("postcode"),
            "tenure": request.form.get("tenure"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "keysafe": request.form.get("keysafe"),
            "keysafe_text": request.form.get("keysafe_text"),
            "int_grab": request.form.get("int_grab"),
            "int_grab_text": request.form.get("int_grab_text"),
            "ext_grab": request.form.get("ext_grab"),
            "ext_grab_text": request.form.get("ext_grab_text"),
            "drop_rail": request.form.get("drop_rail"),
            "drop_rail_text": request.form.get("drop_rail_text"),
            "newel": request.form.get("newel"),
            "newel_text": request.form.get("newel_text"),
            "stair_rail": request.form.get("stair_rail"),
            "stair_rail_text": request.form.get("stair_rail_text"),
            "handrail": request.form.get("handrail"),
            "handrail_text": request.form.get("handrail_text"),
            "step": request.form.get("step"),
            "step_text": request.form.get("step_text"),
            "ramp": request.form.get("ramp"),
            "ramp_text": request.form.get("ramp_text"),
            "shower": request.form.get("shower"),
            "shower_text": request.form.get("shower_text"),
            "other": request.form.get("other"),
            "other_text": request.form.get("other_text"),
            "ref_name": request.form.get("ref_name"),
            "team": request.form.get("team"),
            "ref_email": request.form.get("ref_email"),
            "ref_phone": request.form.get("ref_phone"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"],
            "amended_by": session["user"]
        }
        mongo.db.jobs.insert_one(job)
        flash("Minor Works Order Created")
        customer = mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
        return render_template("create_job.html", customer=customer)

    customer = mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
    return render_template("create_job.html", customer=customer)


@app.route("/delete_job/<job_id>")
def delete_job(job_id):
    """remove job from db"""
    mongo.db.jobs.delete_one({"_id": ObjectId(job_id)})
    flash("Minor Works Order Deleted!")
    return redirect(url_for("edit_job.html"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
