from mybd import get_connection
import tkinter as tk
from tkinter import messagebox, simpledialog



def open_new_order_window(user_data):
    order_window = tk.Toplevel()
    order_window.title(f"Новый заказ - Кассир: {user_data['name']}")
    order_window.state('zoomed')

    bg_main = "#e6f2ff"
    panel_color = "#d9eaff"
    text_color = "#003366"
    btn_color = "#3399ff"
    btn_text_color = "#ffffff"

    order_window.configure(bg=panel_color)
    container = tk.Frame(order_window, bg=panel_color)
    container.pack(fill=tk.BOTH, expand=True)

    client_data = {"id": None, "name": "", "points": 0}
    cart = []
    categories = []
    menu_items = []

    #Вывод категорий
    def load_categories():
        nonlocal categories
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu WHERE stop_list = 0")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        categories.insert(0, "Все")
        update_category_buttons()

    #Вывод меню
    def load_menu_items(category=None):
        nonlocal menu_items
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if category and category != "Все":
            cursor.execute("SELECT * FROM menu WHERE stop_list = 0 AND category = %s", (category,))
        else:
            cursor.execute("SELECT * FROM menu WHERE stop_list = 0")
        menu_items = cursor.fetchall()
        cursor.close()
        conn.close()
        update_menu_display()

    def update_category_buttons():
        for widget in categories_frame.winfo_children():
            widget.destroy()

        for category in categories:
            btn = tk.Button(categories_frame, text=category, font=("Arial", 12),
                            bg=btn_color, fg=btn_text_color, relief="flat",
                            command=lambda c=category: load_menu_items(c))
            btn.pack(side=tk.TOP, fill=tk.X, pady=2)

    def update_menu_display():
        for widget in menu_frame.winfo_children():
            widget.destroy()

        columns = 5
        for i, item in enumerate(menu_items):
            row = i // columns
            col = i % columns

            frame = tk.Frame(menu_frame, bg="white", bd=2, relief="ridge", padx=10, pady=10)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            tk.Label(frame, text=item['name'], font=("Arial", 12), bg="white").pack()
            tk.Label(frame, text=f"{item['price']:.2f} ₽", font=("Arial", 11), bg="white").pack()

            tk.Button(frame, text="Добавить", font=("Arial", 10), bg="#e6ffe6",
                      command=lambda i=item: add_to_cart(i)).pack()

    def add_to_cart(item):
        for cart_item in cart:
            if cart_item['id'] == item['id']:
                cart_item['quantity'] += 1
                update_cart_display()
                return

        cart.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': 1
        })
        update_cart_display()

    def update_cart_display():
        for widget in cart_frame.winfo_children():
            widget.destroy()

        total = 0
        for i, item in enumerate(cart):
            item_frame = tk.Frame(cart_frame, bg="white", bd=1, relief="ridge")
            item_frame.pack(fill=tk.X, pady=2)

            tk.Label(item_frame, text=f"{item['name']}", font=("Arial", 11), bg="white").pack(side=tk.LEFT)

            tk.Button(item_frame, text="-", font=("Arial", 10), bg="#ffcccc",
                      command=lambda idx=i: update_quantity(idx, -1)).pack(side=tk.LEFT, padx=5)

            tk.Label(item_frame, text=str(item['quantity']), font=("Arial", 11), bg="white").pack(side=tk.LEFT)

            tk.Button(item_frame, text="+", font=("Arial", 10), bg="#ccffcc",
                      command=lambda idx=i: update_quantity(idx, 1)).pack(side=tk.LEFT, padx=5)

            tk.Label(item_frame, text=f"{item['price'] * item['quantity']:.2f} ₽",
                     font=("Arial", 11), bg="white").pack(side=tk.RIGHT)

            total += item['price'] * item['quantity']

        if cart:
            total_frame = tk.Frame(cart_frame, bg="white")
            total_frame.pack(fill=tk.X, pady=10)
            tk.Label(total_frame, text=f"Итого: {total:.2f} ₽", font=("Arial", 14, "bold"), bg="white").pack()

            if client_data['id']:
                points_frame = tk.Frame(cart_frame, bg="white")
                points_frame.pack(fill=tk.X)
                tk.Label(points_frame, text=f"Баллы клиента: {client_data['points']}",
                         font=("Arial", 12), bg="white").pack()

                use_points = tk.BooleanVar()
                tk.Checkbutton(points_frame, text="Списать баллы", variable=use_points,
                               font=("Arial", 11), bg="white").pack()

            btn_pay = tk.Button(cart_frame, text="Оплатить", font=("Arial", 14),
                                bg="#66cc66", fg="white", command=lambda: process_payment(total, use_points.get() if
                client_data['id'] else False))
            btn_pay.pack(fill=tk.X, pady=5)

            btn_cancel = tk.Button(cart_frame, text="Отменить", font=("Arial", 14),
                                   bg="#ff6666", fg="white", command=order_window.destroy)
            btn_cancel.pack(fill=tk.X)

    def update_quantity(index, delta):
        cart[index]['quantity'] += delta
        if cart[index]['quantity'] <= 0:
            cart.pop(index)
        update_cart_display()

    #Вход и регестрация клиента (для баллов)
    def ask_client_number():
        phone = simpledialog.askstring("Клиент", "Введите номер телефона клиента (необязательно):")
        if phone:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM client WHERE phone = %s", (phone,))
            client = cursor.fetchone()

            if client:
                client_data.update({
                    'id': client['id'],
                    'name': client['name'],
                    'points': client['points']
                })
            else:
                name = simpledialog.askstring("Новый клиент", "Введите имя нового клиента:")
                if name:
                    cursor.execute("INSERT INTO client (name, phone, points) VALUES (%s, %s, 0)", (name, phone))
                    client_id = cursor.lastrowid
                    conn.commit()
                    client_data.update({
                        'id': client_id,
                        'name': name,
                        'points': 0
                    })

            cursor.close()
            conn.close()
            update_client_display()

    def update_client_display():
        for widget in client_frame.winfo_children():
            widget.destroy()

        if client_data['id']:
            tk.Label(client_frame, text=f"Клиент: {client_data['name']}",
                     font=("Arial", 14), bg=panel_color, fg=text_color).pack(anchor="w", padx=10, pady=(20, 5))
            tk.Label(client_frame, text=f"Баллы: {client_data['points']}",
                     font=("Arial", 12), bg=panel_color, fg=text_color).pack(anchor="w", padx=10)
        else:
            tk.Label(client_frame, text="Клиент не выбран",
                     font=("Arial", 14), bg=panel_color, fg=text_color).pack(anchor="w", padx=10, pady=(20, 5))

        tk.Button(client_frame, text="Выбрать клиента", font=("Arial", 12),
                  bg=btn_color, fg=btn_text_color, command=ask_client_number).pack(anchor="w", padx=10, pady=10)

    #Основная логика покупки
    def process_payment(total, use_points=False):
        if not cart:
            messagebox.showerror("Ошибка", "Корзина пуста!")
            return

        if messagebox.askyesno("Оплата", "Подтвердите оплату"):
            conn = get_connection()
            cursor = conn.cursor()

            try:
                points_to_add = int(float(total) * 0.15)
                points_to_use = min(float(client_data['points']), float(total)) if use_points and client_data[
                    'id'] else 0
                final_amount = float(total) - float(points_to_use)

                cursor.execute(
                    "INSERT INTO sales (date, status, client_id, employee_id, price) "
                    "VALUES (NOW(), 'в ожидании', %s, %s, %s)",
                    (client_data['id'] if client_data['id'] else None, user_data['id'], final_amount)
                )
                sale_id = cursor.lastrowid

                for item in cart:
                    cursor.execute("SELECT recipe_id FROM menu WHERE id = %s", (item['id'],))
                    recipe_result = cursor.fetchone()

                    if not recipe_result or not recipe_result[0]:
                        raise Exception(f"Для блюда {item['name']} не указан рецепт в меню")

                    recipe_id = recipe_result[0]

                    for _ in range(item['quantity']):
                        cursor.execute(
                            "INSERT INTO dishes (menu_id, recipe_id, name, status, start_time, price) "
                            "VALUES (%s, %s, %s, 'в ожидании', NOW(), %s)",
                            (item['id'], recipe_id, item['name'], item['price'])
                        )
                        dish_id = cursor.lastrowid

                        cursor.execute(
                            "INSERT INTO sales_has_dishes (sales_id, dishes_id) VALUES (%s, %s)",
                            (sale_id, dish_id)
                        )

                    cursor.execute(
                        "SELECT workpieces_id, amount FROM recipe_has_workpieces WHERE recipe_id = %s",
                        (recipe_id,)
                    )
                    ingredients = cursor.fetchall()

                    if not ingredients:
                        messagebox.showwarning("Предупреждение",
                                               f"Для рецепта блюда {item['name']} не указаны ингредиенты")
                    else:
                        for wp_id, amount in ingredients:
                            used_amount = amount * item['quantity']
                            cursor.execute(
                                "UPDATE workpieces SET amount = amount - %s WHERE id = %s",
                                (used_amount, wp_id)
                            )

                if client_data['id']:
                    new_points = float(client_data['points']) - float(points_to_use) + float(points_to_add)
                    cursor.execute(
                        "UPDATE client SET points = %s WHERE id = %s",
                        (int(new_points), client_data['id'])
                    )

                conn.commit()
                messagebox.showinfo("Успех", "Заказ успешно оформлен!")
                order_window.destroy()

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Ошибка", f"Ошибка при оформлении заказа: {str(e)}")

            finally:
                cursor.close()
                conn.close()

    left_panel = tk.Frame(container, bg=panel_color, width=250)
    left_panel.pack(side=tk.LEFT, fill=tk.Y)

    center_panel = tk.Frame(container, bg=bg_main)
    center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_panel = tk.Frame(container, bg=panel_color, width=350)
    right_panel.pack(side=tk.RIGHT, fill=tk.Y)

    client_frame = tk.Frame(left_panel, bg=panel_color)
    client_frame.pack(fill=tk.X, pady=10)
    update_client_display()

    categories_frame = tk.Frame(left_panel, bg=panel_color)
    categories_frame.pack(fill=tk.BOTH, expand=True)

    menu_canvas = tk.Canvas(center_panel, bg=bg_main, highlightthickness=0)
    menu_scroll = tk.Scrollbar(center_panel, orient="vertical", command=menu_canvas.yview)
    menu_frame = tk.Frame(menu_canvas, bg=bg_main)

    menu_canvas.create_window((0, 0), window=menu_frame, anchor="nw")
    menu_canvas.configure(yscrollcommand=menu_scroll.set)
    menu_frame.bind("<Configure>", lambda e: menu_canvas.configure(scrollregion=menu_canvas.bbox("all")))

    menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    menu_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    cart_canvas = tk.Canvas(right_panel, bg="white", highlightthickness=0)
    cart_scroll = tk.Scrollbar(right_panel, orient="vertical", command=cart_canvas.yview)
    cart_frame = tk.Frame(cart_canvas, bg="white")

    cart_canvas.create_window((0, 0), window=cart_frame, anchor="nw")
    cart_canvas.configure(yscrollcommand=cart_scroll.set)
    cart_frame.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))

    cart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    cart_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    load_categories()
    load_menu_items()