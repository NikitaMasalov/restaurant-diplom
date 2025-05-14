import tkinter as tk


def open_cook_interface(user_data):
    cook_window = tk.Tk()
    cook_window.title(f"Повар - {user_data['name']}")
    cook_window.geometry("800x600")

    label = tk.Label(cook_window, text=f"Интерфейс повара: {user_data['name']}", font=("Arial", 20))
    label.pack(pady=50)

    cook_window.mainloop()