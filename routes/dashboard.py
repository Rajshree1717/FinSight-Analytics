from flask import Blueprint, render_template
from models.customer import Customer
from models.product import Product
from models.order import Order

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():

    customers = len(Customer.get_all())
    products = len(Product.get_all())

    orders = Order.total_orders()
    revenue = Order.total_revenue()

    return render_template(
        "dashboard.html",
        customers=customers,
        products=products,
        orders=orders,
        revenue=revenue
    )