from flask import Blueprint, render_template
from models.order import Order

sales_bp = Blueprint("sales", __name__)

@sales_bp.route("/sales")
def sales():

    return render_template(
        "sales.html",
        total_revenue=Order.total_revenue(),
        total_orders=Order.total_orders(),
        avg_order=5000,
        top_product="Laptop",
        months=["Jan","Feb","Mar","Apr","May","Jun"],
        revenues=[12000,15000,17000,20000,24000,30000],
        categories=["Electronics","Books","Fashion"],
        category_sales=[60,20,20]
    )