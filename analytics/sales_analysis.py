from utils.database import mysql

def total_revenue():

    cursor=mysql.connection.cursor()

    cursor.execute(
        "SELECT IFNULL(SUM(total_amount),0) FROM orders"
    )

    revenue=cursor.fetchone()[0]

    cursor.close()

    return revenue


def total_orders():

    cursor=mysql.connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )

    count=cursor.fetchone()[0]

    cursor.close()

    return count