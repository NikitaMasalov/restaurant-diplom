import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='mydb',
            port=3306
        )
        return connection
    except Error as e:
        print("Ошибка подключения:", e)
        return None