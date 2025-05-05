from mybd import get_today_orders
import tkinter as tk
from tkinter import  messagebox
import mysql.connector

root = tk.Tk()
root.title("Касса")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

bg_main = "#e6f2ff"
panel_color = "#d9eaff"
card_bg = "#ffffff"
text_color = "#003366"
btn_color = "#3399ff"
btn_text_color = "#ffffff"

root.configure(bg=panel_color)

container = tk.Frame(root, bg=panel_color)
container.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(container, bg=panel_color, width=250)
left_panel.place(x=0, y=0, relheight=1)

right_panel = tk.Frame(container, bg=panel_color, width=250)
right_panel.place(relx=1.0, x=-250, y=0, relheight=1)

center_panel = tk.Frame(container, bg=bg_main)
center_panel.place(x=250, y=0, relwidth=1.0, relheight=0.93, anchor="nw", width=-500)

def setup_left_panel():
    tk.Label(left_panel, text="Кассир: Иванов И.И.",
             font=("Arial", 14), bg=panel_color, fg=text_color).pack(anchor="w", padx=10, pady=(20, 10))
    tk.Label(left_panel, text="Среднее время продажи: 2 мин",
             font=("Arial", 12), bg=panel_color, fg=text_color).pack(anchor="w", padx=10)
    tk.Label(left_panel, text="Цели: (пока пусто)",
             font=("Arial", 12), bg=panel_color, fg=text_color).pack(anchor="w", padx=10, pady=(10, 0))

def setup_right_panel():
    tk.Label(right_panel, text="Правая панель (пока пусто)",
             font=("Arial", 12), bg=panel_color, fg=text_color).pack(anchor="n", pady=20, padx=10)

def setup_center_panel():
    tk.Label(center_panel, text="Текущие заказы за сегодня",
             font=("Arial", 14), bg=bg_main, fg=text_color).pack(anchor="w", pady=(10, 10), padx=20)

    orders_frame = tk.Frame(center_panel, bg=bg_main)
    orders_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    orders = get_today_orders()
    columns = 4

    for i, order in enumerate(orders):
        row = i // columns
        col = i % columns

        order_id = order["id"]
        status = order["status"]
        canceled = order["canceled"]
        created_at = order["date"].strftime("%H:%M")

        if canceled:
            status = "отказ"

        bg_color = "#ffffff"
        if status == "готов":
            bg_color = "#ccffcc"
        elif status == "завершён":
            bg_color = "#cccccc"
        elif status == "отказ":
            bg_color = "#cccccc"

        card = tk.Frame(orders_frame, bg=bg_color, bd=2, relief="ridge", padx=10, pady=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        if status == "отказ":
            tk.Label(card, text="ОТКАЗ", font=("Arial", 10, "bold"),
                     bg=bg_color, fg="red").pack(anchor="w")

        tk.Label(card, text=f"Заказ #{order_id}", font=("Arial", 12, "bold"),
                 bg=bg_color, fg=text_color).pack(anchor="w")

        tk.Label(card, text=f"Статус: {status}", font=("Arial", 11),
                 bg=bg_color, fg=text_color).pack(anchor="w", pady=2)

        tk.Label(card, text=f"Создан: {created_at}", font=("Arial", 10, "italic"),
                 bg=bg_color, fg="#666666").pack(anchor="w", pady=(0, 5))

        btn_frame = tk.Frame(card, bg=bg_color)
        btn_frame.pack(anchor="e", pady=(5, 0))

        tk.Button(btn_frame, text="Подробнее", font=("Arial", 9),
                  bg="#cce6ff", fg="#003366", relief="flat",
                  command=lambda oid=order_id: show_details(oid)).pack(side=tk.LEFT, padx=5)

        if status == "готов":
            tk.Button(btn_frame, text="Отдать", font=("Arial", 9),
                      bg="#66cc66", fg="#003300", relief="flat",
                      activebackground="#99cc99", activeforeground="#003300",
                      bd=2, highlightthickness=1,
                      command=lambda oid=order_id: complete_order(oid)).pack(side=tk.LEFT, padx=5)

    for i in range((len(orders) // columns) + 1):
        orders_frame.rowconfigure(i, weight=1)
    for j in range(columns):
        orders_frame.columnconfigure(j, weight=1)
def create_order():
    print("Создание нового заказа...")

def show_details(order_id):
    print(f"Показать детали заказа #{order_id}")

def complete_order(order_id):
    print(f"Заказ #{order_id} завершён (отдан клиенту)")

setup_left_panel()
setup_center_panel()
setup_right_panel()

bottom_panel = tk.Frame(root, bg=bg_main)
bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

create_order_button = tk.Button(
    bottom_panel, text="Создать заказ",
    font=("Arial", 16), bg=btn_color, fg=btn_text_color,
    height=2, width=25, command=create_order
)
create_order_button.pack(pady=10)

root.mainloop()
