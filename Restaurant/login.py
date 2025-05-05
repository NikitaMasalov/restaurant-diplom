from mybd import get_connection
import tkinter as tk
from tkinter import  messagebox
import  uuid
import mysql.connector
from datetime import datetime, timedelta


def generate_session():
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

def on_tracker_click():
    code = generate_session()
    if code:
        messagebox.showinfo("Трекер", f'Код сеанса: {code}')

root = tk.Tk()
root.title("Вход в систему")
root.geometry("300x200")

label = tk.Label(root, text="Войдите в систему")
label.pack(pady=20)

btn_traker= tk.Button(root, text="Вход в трекер", command=on_tracker_click)
btn_traker.pack(pady=5)

root.mainloop()