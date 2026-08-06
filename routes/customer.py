from flask import Blueprint, render_template, request, redirect
from models.customer import Customer

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/customers")
def customers():

    customers = Customer.get_all()

    return render_template(
        "customers.html",
        customers=customers
    )


@customer_bp.route("/add_customer", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        Customer.create(
            request.form["name"],
            request.form["email"],
            request.form["city"],
            request.form["state"]
        )

        return redirect("/customers")

    return render_template("add_customer.html")


@customer_bp.route("/delete_customer/<int:id>")
def delete_customer(id):

    Customer.delete(id)

    return redirect("/customers")