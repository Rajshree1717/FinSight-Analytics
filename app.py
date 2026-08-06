from flask import Flask, render_template, request, redirect, Response
from config import Config
from flask_mysqldb import MySQL
import csv
import io
from routes.auth import auth_bp


app = Flask(__name__)

app.config.from_object(Config)



mysql = MySQL(app)



# Register Blueprint
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return redirect("/login")
# ================= HOME =================

@app.route("/")
def index():
    return render_template("index.html")



# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    cursor.execute(
        "SELECT IFNULL(SUM(total_amount),0) FROM orders"
    )
    revenue = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "dashboard.html",
        customers=customers,
        products=products,
        orders=orders,
        revenue=revenue
    )



# ================= CUSTOMERS =================

@app.route("/customers")
def customers():

    cursor = mysql.connection.cursor()

    search = request.args.get("search")

    if search:

        cursor.execute("""
            SELECT *
            FROM customers
            WHERE customer_name LIKE %s
        """,
        ('%' + search + '%',))

    else:

        cursor.execute(
            "SELECT * FROM customers"
        )


    customers = cursor.fetchall()

    cursor.close()

    return render_template(
        "customers.html",
        customers=customers
    )




@app.route("/edit_customer/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        city = request.form["city"]
        state = request.form["state"]

        cursor.execute("""
            UPDATE customers
            SET customer_name=%s,
                email=%s,
                city=%s,
                state=%s
            WHERE customer_id=%s
        """, (name, email, city, state, id))

        mysql.connection.commit()
        cursor.close()

        return redirect("/customers")

    cursor.execute("SELECT * FROM customers WHERE customer_id=%s", (id,))
    customer = cursor.fetchone()
    cursor.close()

    return render_template("edit_customer.html", customer=customer)
@app.route("/delete_customer/<int:id>")
def delete_customer(id):

    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM customers WHERE customer_id=%s", (id,))
    mysql.connection.commit()

    cursor.close()

    return redirect("/customers")
@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        city = request.form["city"]
        state = request.form["state"]

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO customers
            (customer_name, email, city, state)
            VALUES (%s, %s, %s, %s)
        """, (name, email, city, state))

        mysql.connection.commit()
        cursor.close()

        return redirect("/customers")

    return render_template("add_customer.html")
# ================= PRODUCTS =================


@app.route("/products")
def products():

    cursor = mysql.connection.cursor()


    search = request.args.get("search")


    if search:

        cursor.execute("""
            SELECT *
            FROM products
            WHERE product_name LIKE %s
        """,
        ('%' + search + '%',))


    else:

        cursor.execute(
            "SELECT * FROM products"
        )


    products = cursor.fetchall()

    cursor.close()


    return render_template(
        "products.html",
        products=products
    )




@app.route("/add_product", methods=["GET","POST"])
def add_product():


    if request.method=="POST":


        name = request.form["name"]

        category = request.form["category"]

        price = request.form["price"]

        stock = request.form["stock"]



        cursor=mysql.connection.cursor()


        cursor.execute("""
            INSERT INTO products
            (product_name,category,price,stock)
            VALUES(%s,%s,%s,%s)
        """,
        (
            name,
            category,
            price,
            stock
        ))


        mysql.connection.commit()

        cursor.close()


        return redirect("/products")


    return render_template(
        "add_product.html"
    )




@app.route("/delete_product/<int:id>")
def delete_product(id):

    cursor=mysql.connection.cursor()


    cursor.execute(
        "DELETE FROM products WHERE product_id=%s",
        (id,)
    )


    mysql.connection.commit()

    cursor.close()


    return redirect("/products")

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        cursor.execute("""
            UPDATE products
            SET
                product_name=%s,
                category=%s,
                price=%s,
                stock=%s
            WHERE product_id=%s
        """, (name, category, price, stock, id))

        mysql.connection.commit()
        cursor.close()

        return redirect("/products")

    cursor.execute(
        "SELECT * FROM products WHERE product_id=%s",
        (id,)
    )

    product = cursor.fetchone()
    cursor.close()

    return render_template(
        "edit_product.html",
        product=product
    )

# ================= SALES ANALYTICS =================
@app.route("/sales")
def sales():

    cursor = mysql.connection.cursor()

    # ---------------- Total Revenue ----------------
    cursor.execute("""
        SELECT IFNULL(SUM(total_amount), 0)
        FROM orders
    """)
    total_revenue = float(cursor.fetchone()[0] or 0)

    # ---------------- Total Orders ----------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
    """)
    total_orders = cursor.fetchone()[0]

    # ---------------- Average Order ----------------
    avg_order = 0
    if total_orders > 0:
        avg_order = round(total_revenue / total_orders, 2)

    # ---------------- Top Product ----------------
    cursor.execute("""
        SELECT
            p.product_name,
            SUM(oi.quantity) AS qty
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name
        ORDER BY qty DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if row:
        top_product = row[0]
    else:
        top_product = "N/A"

    # ---------------- Monthly Revenue ----------------
    cursor.execute("""
        SELECT
            YEAR(order_date) AS yr,
            MONTH(order_date) AS month_no,
            DATE_FORMAT(MIN(order_date), '%b') AS month_name,
            SUM(total_amount) AS revenue
        FROM orders
        GROUP BY
            YEAR(order_date),
            MONTH(order_date)
        ORDER BY
            YEAR(order_date),
            MONTH(order_date)
    """)

    result = cursor.fetchall()

    months = []
    revenues = []

    for row in result:
        months.append(row[2])
        revenues.append(float(row[3]))

    # ---------------- Category Sales ----------------
    cursor.execute("""
        SELECT
            p.category,
            SUM(oi.quantity * oi.price) AS total
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY
            p.category
        ORDER BY total DESC
    """)

    category_result = cursor.fetchall()

    categories = []
    category_sales = []

    for row in category_result:
        categories.append(row[0])
        category_sales.append(float(row[1]))

    cursor.close()

    return render_template(
        "sales.html",
        total_revenue=total_revenue,
        total_orders=total_orders,
        avg_order=avg_order,
        top_product=top_product,
        months=months,
        revenues=revenues,
        categories=categories,
        category_sales=category_sales
    )

@app.route("/add_sale", methods=["POST"])
def add_sale():

    customer_name = request.form["customer"]
    product_name = request.form["product"]
    quantity = int(request.form["quantity"])
    price = float(request.form["price"])

    cursor = mysql.connection.cursor()

    # Get Customer ID
    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_name=%s",
        (customer_name,)
    )
    customer = cursor.fetchone()

    if not customer:
        cursor.close()
        return "Customer not found"

    customer_id = customer[0]

    # Get Product ID
    cursor.execute(
        "SELECT product_id FROM products WHERE product_name=%s",
        (product_name,)
    )
    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"

    product_id = product[0]

    total = quantity * price

    # Insert into Orders
    cursor.execute("""
        INSERT INTO orders
        (customer_id, order_date, total_amount)
        VALUES (%s, CURDATE(), %s)
    """, (customer_id, total))

    order_id = cursor.lastrowid

    # Insert into Order Items
    cursor.execute("""
        INSERT INTO order_items
        (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
    """, (
        order_id,
        product_id,
        quantity,
        price
    ))

    mysql.connection.commit()
    cursor.close()

    return redirect("/sales")

        


    



    

# ================= REPORTS =================


@app.route("/reports")
def reports():

    cursor=mysql.connection.cursor()


    cursor.execute(
        "SELECT IFNULL(SUM(total_amount),0) FROM orders"
    )

    revenue=cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )

    orders=cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    customers=cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    products=cursor.fetchone()[0]



    cursor.execute("""
        SELECT
        o.order_id,
        c.customer_name,
        o.order_date,
        o.total_amount

        FROM orders o

        JOIN customers c

        ON o.customer_id=c.customer_id

        ORDER BY o.order_date DESC

        LIMIT 10

    """)


    recent_orders=cursor.fetchall()


    cursor.close()



    return render_template(
        "reports.html",
        revenue=revenue,
        orders=orders,
        customers=customers,
        products=products,
        recent_orders=recent_orders
    )



# ================= CSV EXPORT =================


@app.route("/export/customers")
def export_customers():


    cursor=mysql.connection.cursor()


    cursor.execute(
        "SELECT * FROM customers"
    )


    rows=cursor.fetchall()


    cursor.close()



    output=io.StringIO()


    writer=csv.writer(output)



    writer.writerow([
        "ID",
        "Name",
        "Email",
        "City",
        "State"
    ])


    for row in rows:

        writer.writerow(row)



    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=customers.csv"
        }
    )

@app.route("/export/sales")
def export_sales():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            c.customer_name,
            p.product_name,
            oi.quantity,
            oi.price,
            (oi.quantity * oi.price) AS total,
            o.order_date
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        ORDER BY o.order_date DESC
    """)

    rows = cursor.fetchall()
    cursor.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Order ID",
        "Customer",
        "Product",
        "Quantity",
        "Price",
        "Total",
        "Date"
    ])

    writer.writerows(rows)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=sales.csv"
        }
    )
@app.route("/export/products")
def export_products():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            category,
            price,
            stock
        FROM products
    """)

    rows = cursor.fetchall()
    cursor.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Product",
        "Category",
        "Price",
        "Stock"
    ])

    writer.writerows(rows)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=products.csv"
        }
    )

# ================= RUN =================


if __name__=="__main__":

    app.run(
        debug=True,
        port=5000
    )