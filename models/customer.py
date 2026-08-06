from utils.database import mysql

class Customer:

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        cursor.close()
        return customers

    @staticmethod
    def get_by_id(customer_id):
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM customers WHERE customer_id=%s",
            (customer_id,)
        )

        customer = cursor.fetchone()

        cursor.close()

        return customer

    @staticmethod
    def create(name, email, city, state):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO customers
            (customer_name,email,city,state)
            VALUES(%s,%s,%s,%s)
        """, (name, email, city, state))

        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete(customer_id):
        cursor = mysql.connection.cursor()

        cursor.execute(
            "DELETE FROM customers WHERE customer_id=%s",
            (customer_id,)
        )

        mysql.connection.commit()
        cursor.close()