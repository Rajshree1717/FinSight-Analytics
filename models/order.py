from utils.database import mysql

class Order:

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT
                o.order_id,
                c.customer_name,
                o.order_date,
                o.total_amount
            FROM orders o
            JOIN customers c
            ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
        """)

        orders = cursor.fetchall()

        cursor.close()

        return orders

    @staticmethod
    def total_revenue():
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT IFNULL(SUM(total_amount),0)
            FROM orders
        """)

        revenue = cursor.fetchone()[0]

        cursor.close()

        return revenue

    @staticmethod
    def total_orders():
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM orders")

        total = cursor.fetchone()[0]

        cursor.close()

        return total