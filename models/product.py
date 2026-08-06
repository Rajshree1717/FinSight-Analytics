from utils.database import mysql

class Product:

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()

        cursor.close()

        return products


    @staticmethod
    def create(name, category, price, stock):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO products
            (product_name, category, price, stock)
            VALUES (%s, %s, %s, %s)
        """, (name, category, price, stock))

        mysql.connection.commit()
        cursor.close()


    @staticmethod
    def get_by_id(product_id):
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM products WHERE product_id=%s",
            (product_id,)
        )

        product = cursor.fetchone()

        cursor.close()

        return product


    @staticmethod
    def update(product_id, name, category, price, stock):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            UPDATE products
            SET
                product_name=%s,
                category=%s,
                price=%s,
                stock=%s
            WHERE product_id=%s
        """, (name, category, price, stock, product_id))

        mysql.connection.commit()
        cursor.close()


    @staticmethod
    def delete(product_id):
        cursor = mysql.connection.cursor()

        cursor.execute(
            "DELETE FROM products WHERE product_id=%s",
            (product_id,)
        )

        mysql.connection.commit()
        cursor.close()