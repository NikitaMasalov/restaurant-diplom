from mybd import get_connection
import tkinter as tk
from tkinter import messagebox
import mysql.connector

from kitchen_interface import open_kitchen_interface
from manager_interface import open_manager_interface
from kassa_interface import  open_kassa_interface


def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Ошибка", "Введите логин и пароль")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, position FROM employee WHERE name=%s AND password_cash=%s",
                       (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            user_data = {
                "id": result[0],
                "name": result[1],
                "position": result[2]
            }

            root.destroy()

            if user_data["position"] == "Кассир":
                open_kassa_interface(user_data)
            elif user_data["position"] == "Повар":
                open_kitchen_interface(user_data)
            elif user_data["position"] == "Менеджер":
                open_manager_choice(user_data)
            else:
                messagebox.showwarning("Ошибка", "Неизвестная должность")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка БД", f"Ошибка: {err}")

def open_manager_choice(user_data):
    choice_window = tk.Tk()
    choice_window.title("Выбор интерфейса")
    choice_window.geometry("400x300")

    label = tk.Label(choice_window, text="Выберите интерфейс:", font=("Arial", 16))
    label.pack(pady=20)

    btn_cashier = tk.Button(choice_window, text="Касса", font=("Arial", 14),
                            command=lambda: [choice_window.destroy(), open_kassa_interface(user_data)])
    btn_cashier.pack(pady=10, fill=tk.X, padx=50)

    btn_cook = tk.Button(choice_window, text="Повар", font=("Arial", 14),
                         command=lambda: [choice_window.destroy(), open_kitchen_interface(user_data)])
    btn_cook.pack(pady=10, fill=tk.X, padx=50)

    btn_manager = tk.Button(choice_window, text="Менеджер", font=("Arial", 14),
                            command=lambda: [choice_window.destroy(), open_manager_interface(user_data)])
    btn_manager.pack(pady=10, fill=tk.X, padx=50)

    choice_window.mainloop()

root = tk.Tk()
root.title("Вход в систему")
root.geometry("300x200")


label = tk.Label(root, text="Войдите в систему", font=("Arial", 14, "bold"))
label.pack(pady=10)

label_username = tk.Label(root, text="Логин", font=("Arial", 12))
label_username.pack()
entry_username = tk.Entry(root, width=30)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Пароль", font=("Arial", 12))
label_password.pack()
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack(pady=5)

btn_login = tk.Button(root, text="Войти", width=15, height=1, font=("Arial", 12), command=login)
btn_login.pack(pady=10)

root.mainloop()