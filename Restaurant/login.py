from mybd import get_connection
import tkinter as tk
from tkinter import  messagebox
import  uuid
import mysql.connector
from datetime import datetime, timedelta

def cleanup_expired_codes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kitchen_codes WHERE expires_at < NOW()")
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Ошибка при удалении просроченых кодов: {err}")

def generate_session():
    cleanup_expired_codes()
    code = str(uuid.uuid4())[:4]
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=30)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kitchen_codes (code, created_at, expires_at, used) VALUES (%s, %s, %s, %s)", (code, created_at, expires_at, 0))
        conn.commit()
        cursor.close()
        return code
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка БД", f"Ошибка подключения: {err}")
        return None

def on_code_click():
    code = generate_session()
    if code:
        messagebox.showinfo("Трекер", f'Код входа: {code}')

def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Ошибка", "Введите логин или пароль")
        return
    try:
        conn =get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT level FROM account WHERE name=%s AND key_hash=%s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            level = result[0]
            messagebox.showinfo("Успешно", f"Вы вошли как: {level}")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка БД", f"Ошибка: {err}")


root = tk.Tk()
root.title("Вход в систему")
root.geometry("300x400")


label = tk.Label(root, text="Войдите в систему", font=("Arial", 14, "bold"))
label.pack(pady=20)

label_username = tk.Label(root, text="логин", font=("Arial", 14))
label_username.pack(pady=1)
entry_username = tk.Entry(root, width=30)
entry_username.pack(pady=1)

label_password = tk.Label(root, text="пароль", font=("Arial", 14))
label_password.pack(pady=1)
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack(pady=1)

btn_login = tk.Button(root, text="Войти", width=25, height=2, font=("Arial", 12), command=login)
btn_login.pack(pady=5)

btn_code= tk.Button(root, text="Вход по коду",width=15, height=2, command=on_code_click, font=("Arial", 12))
btn_code.pack(pady=10)

cleanup_expired_codes()
root.mainloop()