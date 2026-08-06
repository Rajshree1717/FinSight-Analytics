from utils.database import mysql

class User:

    @staticmethod
    def login(email, password):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email=%s AND password=%s
        """, (email, password))

        user = cursor.fetchone()

        cursor.close()

        return user

    @staticmethod
    def create(name, email, password):
        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO users(name, email, password)
            VALUES(%s, %s, %s)
        """, (name, email, password))

        mysql.connection.commit()
        cursor.close()