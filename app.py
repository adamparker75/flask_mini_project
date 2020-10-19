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
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)

"""
building the registration functionality
Always start by building the functionality
for the GET method, ie return render_template
We then ask if the request method is post
And check the db to see if the username exists and
then check it against what the user input on the form
If there is alrady a username we redirect them back
using the url_for to the register function.
We then create a variable called register, which gathers
the data on the form and acts as the else statement.
This data is stored in a dictionary
"""

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # If there is an existing user we flash this message
        if existing_user:
            flash("Username already exisits")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)  # Calls the users collection in our mongodb and uses the insert one method

        # put the new user into 'Session cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")     
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
