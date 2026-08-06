from flask import Blueprint, render_template, request, redirect
from models.product import Product

product_bp = Blueprint("product", __name__)

# ---------------- Products ----------------

@product_bp.route("/products")
def products():

    products = Product.get_all()

    return render_template(
        "products.html",
        products=products
    )


# ---------------- Add Product ----------------

@product_bp.route("/add_product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        Product.create(
            request.form["name"],
            request.form["category"],
            request.form["price"],
            request.form["stock"]
        )

        return redirect("/products")

    return render_template("add_product.html")


# ---------------- Edit Product ----------------

@product_bp.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if request.method == "POST":

        Product.update(
            id,
            request.form["name"],
            request.form["category"],
            request.form["price"],
            request.form["stock"]
        )

        return redirect("/products")

    product = Product.get_by_id(id)

    return render_template(
        "edit_product.html",
        product=product
    )


# ---------------- Delete Product ----------------

@product_bp.route("/delete_product/<int:id>")
def delete_product(id):

    Product.delete(id)

    return redirect("/products")