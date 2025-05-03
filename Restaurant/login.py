
from mybd import get_connection

def test_connection():
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print(f"Успешное подключение к базе данных: {db_name[0]}")
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            conn.close()
    else:
        print("Подключение не удалось.")

if __name__ == "__main__":
    test_connection()