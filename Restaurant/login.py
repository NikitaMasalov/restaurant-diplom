from mybd import get_connection
import tkinter as tk
from tkinter import  messagebox
import mysql.connector


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

root.mainloop()