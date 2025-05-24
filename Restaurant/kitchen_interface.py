from mybd import get_connection
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


def open_kitchen_interface(user_data):
    cook_window = tk.Tk()
    cook_window.title(f"Повар - {user_data['name']}")
    cook_window.state('zoomed')

    bg_main = "#e6f2ff"
    panel_color = "#d9eaff"
    text_color = "#003366"
    btn_color = "#3399ff"
    btn_text_color = "#ffffff"

    cook_window.configure(bg=panel_color)
    container = tk.Frame(cook_window, bg=panel_color)
    container.pack(fill=tk.BOTH, expand=True)

    #Вывод заказов
    def refresh_orders():
        for widget in orders_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                   SELECT d.id, d.name, d.status, s.id as sale_id, d.start_time
                   FROM dishes d
                   JOIN sales_has_dishes sd ON d.id = sd.dishes_id
                   JOIN sales s ON sd.sales_id = s.id
                   WHERE d.status = 'в ожидании'
                   ORDER BY d.start_time
               """)
        pending_dishes = cursor.fetchall()
        cursor.execute("""
                   SELECT d.id, d.name, d.status, s.id as sale_id, d.start_time
                   FROM dishes d
                   JOIN sales_has_dishes sd ON d.id = sd.dishes_id
                   JOIN sales s ON sd.sales_id = s.id
                   WHERE d.status = 'готовиться'
                   ORDER BY d.start_time
               """)
        cooking_dishes = cursor.fetchall()

        cursor.close()
        conn.close()


        dishes =  cooking_dishes + pending_dishes

        columns = 6
        for i, dish in enumerate(dishes):
            row = i // columns
            col = i % columns

            bg_color = "#ffffff"
            if dish['status'] == "готовиться":
                bg_color = "#fff3cd"
            elif dish['status'] == "в ожидании":
                bg_color = "#d4edda"

            dish_frame = tk.Frame(orders_frame, bg=bg_color, bd=2, relief="ridge", padx=10, pady=10, width=300,
                                  height=150)
            dish_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            dish_frame.grid_propagate(False)

            tk.Label(dish_frame,
                     text=f"Заказ #{dish['sale_id']}",
                     font=("Arial", 12, "bold"), bg=bg_color).pack(anchor="w")
            tk.Label(dish_frame,
                     text=f"Блюдо: {dish['name']}",
                     font=("Arial", 11), bg=bg_color).pack(anchor="w")
            tk.Label(dish_frame,
                     text=f"Статус: {dish['status']}",
                     font=("Arial", 10), bg=bg_color).pack(anchor="w")
            tk.Label(dish_frame,
                     text=f"Начато: {dish['start_time'].strftime('%H:%M:%S')}",
                     font=("Arial", 9), bg=bg_color).pack(anchor="w")

            btn_frame = tk.Frame(dish_frame, bg=bg_color)
            btn_frame.pack(fill=tk.X, pady=(5, 0))

            if dish['status'] == "в ожидании":
                tk.Button(btn_frame, text="Начать готовить",
                          bg="#ffc107", fg=text_color, width=15,
                          command=lambda d=dish: start_cooking(d)).pack()
            else:
                tk.Button(btn_frame, text="Готово",
                          bg="#28a745", fg="white", width=15,
                          command=lambda d=dish: finish_cooking(d)).pack()


        for i in range((len(dishes) // columns) + 1):
            orders_frame.rowconfigure(i, weight=1)
        for j in range(columns):
            orders_frame.columnconfigure(j, weight=1)

        last_update_label.config(text=f"Обновлено: {datetime.now().strftime('%H:%M:%S')}")

    def start_cooking(dish):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE dishes SET status = 'готовиться' WHERE id = %s", (dish['id'],))
            conn.commit()
            refresh_orders()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Ошибка", f"Не удалось изменить статус: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    #Перевод в готово (завершение готовки)
    def finish_cooking(dish):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE dishes SET status = 'готово', end_time = NOW() WHERE id = %s", (dish['id'],))

            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM dishes d
                JOIN sales_has_dishes sd ON d.id = sd.dishes_id
                WHERE sd.sales_id = %s AND d.status != 'готово'
            """, (dish['sale_id'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                cursor.execute("UPDATE sales SET status = 'готов' WHERE id = %s", (dish['sale_id'],))

            conn.commit()
            refresh_orders()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Ошибка", f"Не удалось изменить статус: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def auto_refresh():
        refresh_orders()
        cook_window.after(30000, auto_refresh)

    header_frame = tk.Frame(container, bg=panel_color)
    header_frame.pack(fill=tk.X, pady=10)

    tk.Label(header_frame, text="Текущие заказы",
             font=("Arial", 16), bg=panel_color).pack(side=tk.LEFT, padx=20)

    last_update_label = tk.Label(header_frame, text="",
                                 font=("Arial", 10), bg=panel_color)
    last_update_label.pack(side=tk.RIGHT, padx=20)

    btn_refresh = tk.Button(header_frame, text="Обновить",
                            bg=btn_color, fg=btn_text_color,
                            command=refresh_orders)
    btn_refresh.pack(side=tk.RIGHT, padx=10)

    canvas = tk.Canvas(container, bg=bg_main, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    orders_frame = tk.Frame(canvas, bg=bg_main)

    canvas.create_window((0, 0), window=orders_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    orders_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    refresh_orders()
    auto_refresh()
    cook_window.mainloop()