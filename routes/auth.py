from flask import Blueprint, render_template, request, redirect, flash, session
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.login(email, password)

        if user:
            return redirect("/dashboard")

        flash("Invalid email or password")

    return render_template("login.html")
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        User.create(name, email, password)

        flash("Registration Successful")

        return redirect("/login")

    return render_template("register.html")