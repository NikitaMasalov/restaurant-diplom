import mysql.connector
from mysql.connector import Error
from datetime import datetime
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

def get_today_orders():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, date, status
            FROM sales
            WHERE DATE(date) = CURDATE()
            ORDER BY 
                CASE status
                    WHEN 'Готов' THEN 1
                    WHEN 'Готовится' THEN 2
                    WHEN 'Завершён' THEN 3
                    WHEN 'Отказ' THEN 4
                    ELSE 5
                END,
                date DESC
                
        """)
        orders = cursor.fetchall()
        for order in orders:
            order["date"] = order["date"] if isinstance(order["date"], datetime) else datetime.strptime(order["date"], "%Y-%m-%d %H:%M:%S")
        return orders
    except Exception as e:
        print("Ошибка при получении заказов:", e)
        return []
    finally:
        if conn.is_connected():
            conn.close()