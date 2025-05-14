from mybd import get_today_orders, get_connection
import tkinter as tk
from datetime import datetime


def open_kassa_interface(user_data):
    root = tk.Tk()
    root.title(f"Касса - {user_data['name']}")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width - 100
    window_height = screen_height - 100
    root.geometry(f"{window_width}x{window_height}+50+50")

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

    bottom_panel = tk.Frame(root, bg=bg_main)
    bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_left_panel():
        tk.Label(left_panel, text=f"Кассир: {user_data['name']}",
                 font=("Arial", 14), bg=panel_color, fg=text_color).pack(anchor="w", padx=10, pady=(20, 10))
        tk.Label(left_panel, text="Среднее время: 2 мин",
                 font=("Arial", 12), bg=panel_color, fg=text_color).pack(anchor="w", padx=10)
        tk.Button(left_panel, text="Выход", font=("Arial", 12),
                  bg="#ff6666", fg=btn_text_color, command=root.destroy).pack(anchor="w", padx=10, pady=(10, 0))

    def setup_right_panel():
        tk.Label(right_panel, text="Правая панель (пока пусто)", font=("Arial", 12), bg=panel_color,
                 fg=text_color).pack(
            anchor="n", pady=20, padx=10)

    def show_details(sales_id):
        detail_window = tk.Toplevel()
        detail_window.title(f"Детали заказа #{sales_id}")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.name, d.status 
            FROM dishes d
            JOIN sales_has_dishes sd ON d.id = sd.dishes_id
            WHERE sd.sales_id = %s
        """, (sales_id,))
        dishes = cursor.fetchall()
        cursor.close()
        conn.close()

        for i, dish in enumerate(dishes):
            frame = tk.Frame(detail_window, width=200, height=120, bg='lightblue', relief='raised', borderwidth=2)
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            tk.Label(frame, text=dish['name'], font=("Arial", 11, "bold"), bg='lightblue').pack(pady=5)
            tk.Label(frame, text=dish['status'], font=("Arial", 10), bg='lightblue').pack()

    def complete_order(order_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE sales SET status = 'завершён' WHERE id = %s", (order_id,))
        conn.commit()
        cursor.close()
        refresh_orders()

    def refresh_orders():
        try:
            for widget in orders_frame.winfo_children():
                widget.destroy()

            orders = get_today_orders()
            columns = 4

            for i, order in enumerate(orders):
                row = i // columns
                col = i % columns

                bg_color = "#ffffff"
                if order['status'] == "готов":
                    bg_color = "#ccffcc"
                elif order['status'] == "завершён":
                    bg_color = "#cccccc"
                elif order['status'] == "отказ":
                    bg_color = "#ffcccc"

                card = tk.Frame(orders_frame, bg=bg_color, bd=2, relief="ridge", padx=15, pady=15, width=300,
                                height=150)
                card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
                card.grid_propagate(False)

                if order['status'] == "отказ":
                    tk.Label(card, text="ОТКАЗ", font=("Arial", 10, "bold"), bg=bg_color, fg="red").pack(anchor="w")

                tk.Label(card, text=f"Заказ #{order['id']}", font=("Arial", 14, "bold"), bg=bg_color,
                         fg=text_color).pack(anchor="w")
                tk.Label(card, text=f"Статус: {order['status']}", font=("Arial", 12), bg=bg_color, fg=text_color).pack(
                    anchor="w", pady=5)
                tk.Label(card, text=f"Создан: {order['date'].strftime('%H:%M')}", font=("Arial", 10), bg=bg_color,
                         fg="#666666").pack(anchor="w")

                btn_frame = tk.Frame(card, bg=bg_color)
                btn_frame.pack(anchor="e", pady=(5, 0))

                tk.Button(btn_frame, text="Подробнее", font=("Arial", 10), bg="#cce6ff", fg="#003366", relief="flat",
                          command=lambda oid=order['id']: show_details(oid)).pack(side=tk.LEFT, padx=5)

                if order['status'] == "готов":
                    tk.Button(btn_frame, text="Отдать", font=("Arial", 10), bg="#66cc66", fg="#003300", relief="flat",
                              command=lambda oid=order['id']: complete_order(oid)).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка обновления: {str(e)}")

    def auto_refresh():
        refresh_orders()
        root.after(60000, auto_refresh)

    def create_order():
        print("Создание нового заказа...")

    setup_left_panel()

    tk.Label(center_panel, text="Текущие заказы за сегодня",
             font=("Arial", 14), bg=bg_main, fg=text_color).pack(anchor="w", pady=(10, 10), padx=20)

    canvas = tk.Canvas(center_panel, bg=bg_main, highlightthickness=0)
    scrollbar = tk.Scrollbar(center_panel, orient="vertical", command=canvas.yview)
    orders_frame = tk.Frame(canvas, bg=bg_main)

    canvas.create_window((0, 0), window=orders_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    orders_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side="left", fill="both", expand=True, padx=20)
    scrollbar.pack(side="right", fill="y")

    btn_frame = tk.Frame(bottom_panel, bg=bg_main)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Обновить", font=("Arial", 12),
              bg=btn_color, fg=btn_text_color, command=refresh_orders).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Создать заказ", font=("Arial", 16),
              bg=btn_color, fg=btn_text_color, height=2, width=25, command=create_order).pack(side=tk.LEFT, padx=10)

    refresh_orders()
    auto_refresh()
    root.mainloop()