from utils.database import mysql

def product_count():

    cursor=mysql.connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    total=cursor.fetchone()[0]

    cursor.close()

    return total