import tkinter as tk


def open_manager_interface(user_data):
    manager_window = tk.Tk()
    manager_window.title(f"Менеджер - {user_data['name']}")
    manager_window.geometry("800x600")

    label = tk.Label(manager_window, text=f"Интерфейс менеджера: {user_data['name']}", font=("Arial", 20))
    label.pack(pady=50)

    manager_window.mainloop()