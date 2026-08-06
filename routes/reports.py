from flask import Blueprint, render_template
from models.customer import Customer
from models.product import Product
from models.order import Order

reports_bp = Blueprint("reports", __name__)

reports = Blueprint("reports", __name__)

@reports.route("/reports")
def report_page():

    return render_template(
        "reports.html",
        revenue=Order.total_revenue(),
        orders=Order.total_orders(),
        customers=len(Customer.get_all()),
        products=len(Product.get_all()),
        recent_orders=Order.get_all()
    )