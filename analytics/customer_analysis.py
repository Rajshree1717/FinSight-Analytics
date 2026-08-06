from utils.database import mysql

def customer_count():

    cursor=mysql.connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    total=cursor.fetchone()[0]

    cursor.close()

    return total