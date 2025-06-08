from mybd import get_connection
import hashlib
from tkcalendar import Calendar
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_manager_interface(user_data):
    root = tk.Tk()
    root.title(f"Менеджер - {user_data['name']}")
    root.state('zoomed')


    bg_color = "#f0f0f0"
    panel_color = "#e1e1e1"
    accent_color = "#4a6fa5"
    text_color = "#333333"

    root.configure(bg=bg_color)

    style = ttk.Style()
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=text_color)
    style.configure("TButton", background=accent_color, foreground="black")
    style.map("TButton", background=[('active', '#3a5a80')])

    nav_frame = ttk.Frame(root, padding="10")
    nav_frame.pack(fill=tk.X)

    container = ttk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    analytics_frame = ttk.Frame(container)
    orders_frame = ttk.Frame(container)
    employees_frame = ttk.Frame(container)
    workpieces_frame = ttk.Frame(container)
    workpieces_frame.entries = {}

    def update_employees():
        for item in employees_frame.tree.get_children():
            employees_frame.tree.delete(item)

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, phone, position FROM employee WHERE is_active = TRUE ORDER BY name")

            for row in cursor.fetchall():
                employees_frame.tree.insert("", "end", values=(
                    row['id'],
                    row['name'],
                    row['phone'],
                    row['position']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def show_frame(frame):
        for f in (analytics_frame, orders_frame, employees_frame, workpieces_frame):
            f.pack_forget()

        frame.pack(fill=tk.BOTH, expand=True)

        if frame == analytics_frame:
            update_analytics()
        elif frame == orders_frame:
            update_orders()
        elif frame == employees_frame:
            update_employees()
        elif frame == workpieces_frame:
            load_workpieces()

    buttons = [
        ("Аналитика", lambda: show_frame(analytics_frame)),
        ("Заказы", lambda: show_frame(orders_frame)),
        ("Персонал", lambda: show_frame(employees_frame)),
        ("Остатки", lambda: show_frame(workpieces_frame))

    ]

    for text, command in buttons:
        btn = ttk.Button(nav_frame, text=text, command=command)
        btn.pack(side=tk.LEFT, padx=5)


    def setup_analytics_frame():
        ttk.Label(analytics_frame, text="Аналитика", font=('Arial', 16, 'bold')).pack(pady=20)

        metrics_frame = ttk.Frame(analytics_frame)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(metrics_frame, text="Прибыль за сегодня:", font=('Arial', 12)).grid(row=0, column=0, sticky='w')
        analytics_frame.today_profit_label = ttk.Label(metrics_frame, text="0 ₽", font=('Arial', 12, 'bold'))
        analytics_frame.today_profit_label.grid(row=0, column=1, sticky='w', padx=10)

        ttk.Label(metrics_frame, text="Среднее время готовки:", font=('Arial', 12)).grid(row=1, column=0, sticky='w')
        analytics_frame.avg_cooking_label = ttk.Label(metrics_frame, text="0 мин", font=('Arial', 12, 'bold'))
        analytics_frame.avg_cooking_label.grid(row=1, column=1, sticky='w', padx=10)

        ttk.Label(metrics_frame, text="Количество заказов:", font=('Arial', 12)).grid(row=2, column=0, sticky='w')
        analytics_frame.orders_count_label = ttk.Label(metrics_frame, text="0", font=('Arial', 12, 'bold'))
        analytics_frame.orders_count_label.grid(row=2, column=1, sticky='w', padx=10)

        ttk.Label(metrics_frame, text="Популярное блюдо сегодня:", font=('Arial', 12)).grid(row=3, column=0, sticky='w')
        analytics_frame.popular_dish_day_label = ttk.Label(metrics_frame, text="-", font=('Arial', 12, 'bold'))
        analytics_frame.popular_dish_day_label.grid(row=3, column=1, sticky='w', padx=10)

        ttk.Label(metrics_frame, text="Популярное блюдо:", font=('Arial', 12)).grid(row=4, column=0, sticky='w')
        analytics_frame.popular_dish_label = ttk.Label(metrics_frame, text="-", font=('Arial', 12, 'bold'))
        analytics_frame.popular_dish_label.grid(row=4, column=1, sticky='w', padx=10)

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        analytics_frame.chart_canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
        analytics_frame.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        analytics_frame.chart_ax = ax

    #Данные для аналитики
    def update_analytics():
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            #Прибыль за сегодня
            cursor.execute("""
                SELECT SUM(price) as total 
                FROM sales 
                WHERE DATE(date) = CURDATE() AND status != 'отказ'
            """)
            result = cursor.fetchone()
            profit = result['total'] if result['total'] else 0
            analytics_frame.today_profit_label.config(text=f"{profit:.2f} ₽")

            #Среднее время готовки
            cursor.execute("""
                SELECT AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) as avg_time 
                FROM dishes 
                WHERE end_time IS NOT NULL AND DATE(start_time) = CURDATE()
            """)
            result = cursor.fetchone()
            avg_time = result['avg_time'] if result['avg_time'] else 0
            analytics_frame.avg_cooking_label.config(text=f"{int(avg_time)} мин")

            #Колличество заказов за сегодня
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM sales 
                WHERE DATE(date) = CURDATE() AND status != 'отказ'
            """)
            result = cursor.fetchone()
            analytics_frame.orders_count_label.config(text=result['count'])

            #Популярное блюдо сегодня
            cursor.execute("""
                SELECT m.name, COUNT(*) as count 
                FROM dishes d
                JOIN menu m ON d.menu_id = m.id
                JOIN sales_has_dishes sd ON d.id = sd.dishes_id
                JOIN sales s ON sd.sales_id = s.id
                WHERE DATE(s.date) = CURDATE()
                GROUP BY m.name
                ORDER BY count DESC
                LIMIT 1
            """)
            result = cursor.fetchone()
            if result:
                analytics_frame.popular_dish_day_label.config(text=f"{result['name']} ({result['count']} шт)")
            else:
                analytics_frame.popular_dish_day_label.config(text="-")

                # Популярное блюдо за все время
            cursor.execute("""
                SELECT m.name, COUNT(*) as count 
                FROM dishes d
                JOIN menu m ON d.menu_id = m.id
                JOIN sales_has_dishes sd ON d.id = sd.dishes_id
                JOIN sales s ON sd.sales_id = s.id
                GROUP BY m.name
                ORDER BY count DESC
                LIMIT 1
                        """)
            result = cursor.fetchone()
            if result:
                analytics_frame.popular_dish_label.config(text=f"{result['name']} ({result['count']} шт)")
            else:
                analytics_frame.popular_dish_label.config(text="-")

            #Вывод прибыли в график (7 дней)
            cursor.execute("""
                SELECT DATE(date) as day, SUM(price) as total
                FROM sales
                WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND status != 'отказ'
                GROUP BY DATE(date)
                ORDER BY day
            """)
            sales_data = cursor.fetchall()

            dates = [row['day'].strftime('%d.%m') for row in sales_data]
            amounts = [float(row['total']) if row['total'] else 0 for row in sales_data]

            analytics_frame.chart_ax.clear()
            analytics_frame.chart_ax.bar(dates, amounts, color=accent_color)
            analytics_frame.chart_ax.set_title('Продажи за последние 7 дней')
            analytics_frame.chart_ax.set_ylabel('Сумма (₽)')
            analytics_frame.chart_canvas.draw()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
        finally:
            if conn.is_connected():
                conn.close()

    def setup_orders_frame():
        # Фрейм для фильтров
        filter_frame = ttk.Frame(orders_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        # Выбор типа поиска
        ttk.Label(filter_frame, text="Поиск по:").pack(side=tk.LEFT, padx=5)
        search_field = ttk.Combobox(filter_frame, values=["№", "Дата", "Клиент", "Статус"], state="readonly")
        search_field.set("№")
        search_field.pack(side=tk.LEFT, padx=5)
        search_field.bind("<<ComboboxSelected>>", lambda e: update_search_widgets())

        # Виджеты для разных типов поиска
        # 1. Поиск по тексту (по умолчанию)
        search_entry = ttk.Entry(filter_frame)

        # 2. Поиск по дате
        date_frame = ttk.Frame(filter_frame)
        date_picker_btn = ttk.Button(date_frame, text="Выбрать дату", command=lambda: show_calendar())
        date_picker_btn.pack(side=tk.LEFT)
        date_label = ttk.Label(date_frame, text="")
        date_label.pack(side=tk.LEFT, padx=5)

        # 3. Поиск по периоду
        period_frame = ttk.Frame(filter_frame)
        ttk.Label(period_frame, text="С:").pack(side=tk.LEFT)
        start_date_btn = ttk.Button(period_frame, text="Выбрать", command=lambda: show_calendar(is_start_date=True))
        start_date_btn.pack(side=tk.LEFT, padx=5)
        ttk.Label(period_frame, text="По:").pack(side=tk.LEFT, padx=5)
        end_date_btn = ttk.Button(period_frame, text="Выбрать", command=lambda: show_calendar(is_start_date=False))
        end_date_btn.pack(side=tk.LEFT)

        # Определим perform_search до использования
        def perform_search():
            search_type = search_field.get()
            if search_type == "Дата":
                if orders_frame.selected_date:
                    update_orders(search_by="Дата", search_text=orders_frame.selected_date)
                else:
                    messagebox.showwarning("Ошибка", "Выберите дату")
            elif search_type == "Статус":
                status = status_combobox.get()
                if status:
                    update_orders(search_by="Статус", search_text=status)
                else:
                    messagebox.showwarning("Ошибка", "Выберите статус")
            elif search_type in ["№", "Клиент"]:
                update_orders(search_by=search_type, search_text=search_entry.get())

        # 4. Выпадающий список для статуса
        status_combobox = ttk.Combobox(filter_frame, values=["в ожидании", "готов", "завершён", "отказ"],
                                           state="readonly")

        # Кнопки управления
        search_btn = ttk.Button(filter_frame, text="Поиск", command=perform_search)
        search_btn.pack(side=tk.LEFT, padx=5)
        reset_btn = ttk.Button(filter_frame, text="Сброс", command=lambda: update_orders())
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Переменные для хранения дат
        orders_frame.selected_date = None
        orders_frame.start_date = None
        orders_frame.end_date = None

        # Таблица заказов
        tree_frame = ttk.Frame(orders_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        orders_frame.tree = ttk.Treeview(tree_frame, columns=("id", "date", "client", "status", "price"),
                                         show="headings")
        orders_frame.tree.heading("id", text="№")
        orders_frame.tree.heading("date", text="Дата")
        orders_frame.tree.heading("client", text="Клиент")
        orders_frame.tree.heading("status", text="Статус")
        orders_frame.tree.heading("price", text="Сумма")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=orders_frame.tree.yview)
        orders_frame.tree.configure(yscrollcommand=scrollbar.set)

        orders_frame.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Панель с общей суммой
        right_frame = ttk.Frame(orders_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        orders_frame.total_label = ttk.Label(right_frame, text="Общая сумма: 0 ₽", font=('Arial', 12, 'bold'))
        orders_frame.total_label.pack(pady=10)

        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Обновить", command=update_orders).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Подробнее", command=show_order_details).pack(fill=tk.X, pady=5)

        def update_search_widgets():
            # Скрываем все виджеты поиска
            search_entry.pack_forget()
            date_frame.pack_forget()
            period_frame.pack_forget()
            status_combobox.pack_forget()

            # Показываем нужный виджет
            if search_field.get() == "Дата":
                date_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            elif search_field.get() == "Статус":
                status_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            else:
                search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        def show_calendar(is_start_date=None):
            top = tk.Toplevel(root)
            top.title("Выберите дату")

            cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
            cal.pack(pady=10)

            def set_date():
                selected = cal.get_date()
                if is_start_date is None:
                    orders_frame.selected_date = selected
                    date_label.config(text=selected)
                elif is_start_date:
                    orders_frame.start_date = selected
                    start_date_btn.config(text=selected)
                else:
                    orders_frame.end_date = selected
                    end_date_btn.config(text=selected)
                top.destroy()

            ttk.Button(top, text="Выбрать", command=set_date).pack(pady=5)

        def perform_search():
            search_type = search_field.get()
            if search_type == "Дата":
                if orders_frame.selected_date:
                    update_orders(search_by="Дата", search_text=orders_frame.selected_date)
                else:
                    messagebox.showwarning("Ошибка", "Выберите дату")
            elif search_type in ["№", "Клиент", "Статус"]:
                update_orders(search_by=search_type, search_text=search_entry.get())

        update_search_widgets()  # Инициализация виджетов

    def update_orders(search_by=None, search_text=None):
        for item in orders_frame.tree.get_children():
            orders_frame.tree.delete(item)

        total_amount = 0
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT s.id, s.date, s.status, s.price, c.name as client_name
                FROM sales s
                LEFT JOIN client c ON s.client_id = c.id
            """

            params = []

            if search_by == "№":
                query += " WHERE s.id = %s"
                params.append(int(search_text))
            elif search_by == "Дата":
                query += " WHERE DATE(s.date) = %s"
                params.append(search_text)
            elif search_by == "Клиент":
                query += " WHERE c.name LIKE %s"
                params.append(f"%{search_text}%")
            elif search_by == "Статус":
                query += " WHERE s.status = %s"
                params.append(search_text)

            query += " ORDER BY s.date DESC"

            cursor.execute(query, params)

            for row in cursor.fetchall():
                orders_frame.tree.insert("", "end", values=(
                    row['id'],
                    row['date'].strftime('%d.%m.%Y %H:%M'),
                    row['client_name'] if row['client_name'] else "Гость",
                    row['status'],
                    f"{row['price']:.2f} ₽"
                ))
                total_amount += float(row['price'])

            orders_frame.total_label.config(text=f"Общая сумма: {total_amount:.2f} ₽")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def show_order_details():
        selected = orders_frame.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите заказ")
            return

        order_id = orders_frame.tree.item(selected[0])['values'][0]

        detail_window = tk.Toplevel(root)
        detail_window.title(f"Детали заказа #{order_id}")

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Информация о заказе
            cursor.execute("""
                SELECT s.date, s.status, s.price, e.name as employee_name, c.name as client_name,
                       (SELECT MAX(end_time) FROM dishes d 
                        JOIN sales_has_dishes sd ON d.id = sd.dishes_id 
                        WHERE sd.sales_id = s.id) as end_time
                FROM sales s
                JOIN employee e ON s.employee_id = e.id
                LEFT JOIN client c ON s.client_id = c.id
                WHERE s.id = %s
            """, (order_id,))
            order_info = cursor.fetchone()

            info_frame = ttk.Frame(detail_window)
            info_frame.pack(fill=tk.X, padx=10, pady=10)

            ttk.Label(info_frame, text=f"Номер заказа: #{order_id}").pack(anchor="w")
            ttk.Label(info_frame, text=f"Дата: {order_info['date'].strftime('%d.%m.%Y %H:%M')}").pack(anchor="w")
            ttk.Label(info_frame, text=f"Статус: {order_info['status']}").pack(anchor="w")

            if order_info['end_time']:
                ttk.Label(info_frame, text=f"Завершен: {order_info['end_time'].strftime('%d.%m.%Y %H:%M')}").pack(
                    anchor="w")

            ttk.Label(info_frame, text=f"Сумма: {order_info['price']:.2f} ₽").pack(anchor="w")
            ttk.Label(info_frame, text=f"Кассир: {order_info['employee_name']}").pack(anchor="w")
            if order_info['client_name']:
                ttk.Label(info_frame, text=f"Клиент: {order_info['client_name']}").pack(anchor="w")

            # Блюда в заказе
            cursor.execute("""
                SELECT d.name, d.status, d.price, d.start_time, d.end_time
                FROM dishes d
                JOIN sales_has_dishes sd ON d.id = sd.dishes_id
                WHERE sd.sales_id = %s
            """, (order_id,))

            dishes_frame = ttk.Frame(detail_window)
            dishes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            ttk.Label(dishes_frame, text="Блюда в заказе:", font=('Arial', 12, 'bold')).pack(anchor="w")

            for dish in cursor.fetchall():
                dish_frame = ttk.Frame(dishes_frame, borderwidth=1, relief="solid", padding=5)
                dish_frame.pack(fill=tk.X, pady=2)

                ttk.Label(dish_frame, text=f"{dish['name']} - {dish['price']:.2f} ₽").pack(anchor="w")
                ttk.Label(dish_frame, text=f"Статус: {dish['status']}").pack(anchor="w")
                ttk.Label(dish_frame, text=f"Начато: {dish['start_time'].strftime('%H:%M:%S')}").pack(anchor="w")
                if dish['end_time']:
                    ttk.Label(dish_frame, text=f"Завершено: {dish['end_time'].strftime('%H:%M:%S')}").pack(anchor="w")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # Фрейм управления персоналом
    def setup_employees_frame():
        search_frame = ttk.Frame(employees_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(search_frame, text="Поиск по:").pack(side=tk.LEFT, padx=5)
        employees_frame.search_field = ttk.Combobox(search_frame, values=["Имя", "Телефон"], state="readonly")
        employees_frame.search_field.set("Имя")
        employees_frame.search_field.pack(side=tk.LEFT, padx=5)

        employees_frame.search_entry = ttk.Entry(search_frame)
        employees_frame.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        def perform_search():
            search_type = employees_frame.search_field.get()
            search_text = employees_frame.search_entry.get()

            if not search_text:
                messagebox.showwarning("Ошибка", "Введите данные для поиска")
                return

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)

                if search_type == "Имя":
                    cursor.execute("SELECT * FROM employee WHERE name LIKE %s AND is_active = TRUE",
                                   (f"%{search_text}%",))
                elif search_type == "Телефон":
                    cursor.execute("SELECT * FROM employee WHERE phone LIKE %s AND is_active = TRUE",
                                   (f"%{search_text}%",))

                employees = cursor.fetchall()

                for item in employees_frame.tree.get_children():
                    employees_frame.tree.delete(item)

                for employee in employees:
                    employees_frame.tree.insert("", "end", values=(
                        employee['id'],
                        employee['name'],
                        employee['phone'],
                        employee['position']
                    ))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось выполнить поиск: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        search_btn = ttk.Button(search_frame, text="Поиск", command=perform_search)
        search_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(search_frame, text="Сброс", command=lambda: update_employees())
        reset_btn.pack(side=tk.LEFT, padx=5)

        tree_frame = ttk.Frame(employees_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        employees_frame.tree = ttk.Treeview(tree_frame, columns=("id", "name", "phone", "position"), show="headings")
        employees_frame.tree.heading("id", text="ID")
        employees_frame.tree.heading("name", text="Имя")
        employees_frame.tree.heading("phone", text="Телефон")
        employees_frame.tree.heading("position", text="Должность")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=employees_frame.tree.yview)
        employees_frame.tree.configure(yscrollcommand=scrollbar.set)

        employees_frame.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        employees_frame.search_field.bind("<<ComboboxSelected>>", lambda e: update_search_widgets())

        def update_search_widgets():
            employees_frame.search_entry.delete(0, tk.END)

        def delete_employee():
            selected = employees_frame.tree.selection()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберите сотрудника для удаления")
                return

            employee_id = employees_frame.tree.item(selected[0])['values'][0]

            password = simpledialog.askstring("Подтверждение", "Введите пароль для подтверждения изменения:", show='*')
            if not password:
                return

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Проверка пароля текущего пользователя
                cursor.execute("SELECT password_cash FROM employee WHERE id = %s", (user_data['id'],))
                result = cursor.fetchone()

                if not result:
                    messagebox.showerror("Ошибка", "Пользователь не найден")
                    return

                stored_password = result[0]  # Первый элемент кортежа
                input_password = hashlib.md5(password.encode('utf-8')).hexdigest()

                if input_password != stored_password:
                    messagebox.showerror("Ошибка", "Неверный пароль")
                    return

                # Устанавливаем is_active = FALSE вместо удаления
                cursor.execute("UPDATE employee SET is_active = FALSE WHERE id = %s", (employee_id,))
                conn.commit()
                messagebox.showinfo("Успех", "Сотрудник деактивирован")
                update_employees()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось деактивировать сотрудника: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        # Функция для изменения сотрудника
        def edit_employee():
            selected = employees_frame.tree.selection()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберите сотрудника для редактирования")
                return

            employee_id = employees_frame.tree.item(selected[0])['values'][0]

            password = simpledialog.askstring("Подтверждение", "Введите пароль для подтверждения изменения:", show='*')
            if not password:
                return

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)

                cursor.execute("SELECT password_cash FROM employee WHERE id = %s", (user_data['id'],))
                result = cursor.fetchone()

                if not result:
                    messagebox.showerror("Ошибка", "Пользователь не найден")
                    return

                stored_password = result['password_cash']
                input_password = hashlib.md5(password.encode('utf-8')).hexdigest()

                if input_password != stored_password:
                    messagebox.showerror("Ошибка", "Неверный пароль")
                    return

                cursor.execute("SELECT * FROM employee WHERE id = %s", (employee_id,))
                employee = cursor.fetchone()

                edit_window = tk.Toplevel(root)
                edit_window.title("Редактировать сотрудника")

                ttk.Label(edit_window, text="Имя:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
                name_entry = ttk.Entry(edit_window)
                name_entry.insert(0, employee['name'])
                name_entry.grid(row=0, column=1, padx=5, pady=5)

                ttk.Label(edit_window, text="Телефон:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
                phone_entry = ttk.Entry(edit_window)
                phone_entry.insert(0, employee['phone'])
                phone_entry.grid(row=1, column=1, padx=5, pady=5)

                ttk.Label(edit_window, text="Должность:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
                position_entry = ttk.Entry(edit_window)
                position_entry.insert(0, employee['position'])
                position_entry.grid(row=2, column=1, padx=5, pady=5)

                ttk.Label(edit_window, text="Новый пароль:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
                password_entry = ttk.Entry(edit_window, show="*")
                password_entry.grid(row=3, column=1, padx=5, pady=5)

                def save_changes():
                    name = name_entry.get()
                    phone = phone_entry.get()
                    position = position_entry.get()
                    password = password_entry.get()

                    if not name or not phone or not position:
                        messagebox.showwarning("Ошибка", "Все поля обязательны для заполнения")
                        return

                    conn = None
                    cursor = None
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        if password:
                            hashed_password = hashlib.md5(password.encode()).hexdigest()
                            cursor.execute(
                                "UPDATE employee SET name = %s, phone = %s, position = %s, password_cash = %s WHERE id = %s",
                                (name, phone, position, hashed_password, employee_id)
                            )
                        else:
                            cursor.execute(
                                "UPDATE employee SET name = %s, phone = %s, position = %s WHERE id = %s",
                                (name, phone, position, employee_id)
                            )

                        conn.commit()
                        messagebox.showinfo("Успех", "Изменения сохранены")
                        edit_window.destroy()
                        update_employees()
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Не удалось сохранить изменения: {str(e)}")
                    finally:
                        if cursor:
                            cursor.close()
                        if conn and conn.is_connected():
                            conn.close()

                ttk.Button(edit_window, text="Сохранить", command=save_changes).grid(row=4, column=1, pady=10)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
                edit_window.destroy()
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        # Определение функции добавления сотрудника
        def add_employee():
            add_window = tk.Toplevel(root)
            add_window.title("Добавить сотрудника")

            ttk.Label(add_window, text="Имя:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            name_entry = ttk.Entry(add_window)
            name_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(add_window, text="Телефон:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            phone_entry = ttk.Entry(add_window)
            phone_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(add_window, text="Должность:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            position_entry = ttk.Entry(add_window)
            position_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(add_window, text="Пароль:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
            password_entry = ttk.Entry(add_window, show="*")
            password_entry.grid(row=3, column=1, padx=5, pady=5)

            def save_employee():
                name = name_entry.get()
                phone = phone_entry.get()
                position = position_entry.get()
                password = password_entry.get()

                if not name or not phone or not position or not password:
                    messagebox.showwarning("Ошибка", "Все поля обязательны для заполнения")
                    return

                hashed_password = hashlib.md5(password.encode()).hexdigest()

                conn = None
                cursor = None
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO employee (name, phone, position, password_cash) VALUES (%s, %s, %s, %s)",
                        (name, phone, position, hashed_password)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Сотрудник добавлен")
                    add_window.destroy()
                    update_employees()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {str(e)}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn and conn.is_connected():
                        conn.close()

            ttk.Button(add_window, text="Сохранить", command=save_employee).grid(row=4, column=1, pady=10)

        btn_frame = ttk.Frame(employees_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Добавить", command=add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Изменить", command=edit_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=delete_employee).pack(side=tk.LEFT, padx=5)

        update_employees()

    #Фрейм остатков
    def setup_workpieces_frame():
        ttk.Label(workpieces_frame, text="Управление остатками", font=('Arial', 16, 'bold')).pack(pady=20)

        workpieces_frame.list_frame = ttk.Frame(workpieces_frame)  # Инициализация list_frame как атрибута
        workpieces_frame.list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        headers = ["Название", "Текущий остаток", "Фактический остаток", "Разница"]
        for i, header in enumerate(headers):
            ttk.Label(workpieces_frame.list_frame, text=header, font=('Arial', 12, 'bold')).grid(row=0, column=i,
                                                                                                 padx=5, pady=5)

        btn_frame = ttk.Frame(workpieces_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Проверить", command=check_workpieces).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сохранить", command=save_workpieces).pack(side=tk.LEFT, padx=5)

        load_workpieces()

    def load_workpieces():
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM workpieces")
            workpieces = cursor.fetchall()

            for widget in workpieces_frame.list_frame.winfo_children():
                if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Label):
                    widget.destroy()

            for i, wp in enumerate(workpieces):
                ttk.Label(workpieces_frame.list_frame, text=wp['name']).grid(row=i + 1, column=0, padx=5, pady=5)
                ttk.Label(workpieces_frame.list_frame, text=f"{wp['amount']:.2f}").grid(row=i + 1, column=1, padx=5,
                                                                                        pady=5)
                workpieces_frame.entries[wp['id']] = ttk.Entry(workpieces_frame.list_frame)
                workpieces_frame.entries[wp['id']].grid(row=i + 1, column=2, padx=5, pady=5)
                ttk.Label(workpieces_frame.list_frame, text="").grid(row=i + 1, column=3, padx=5, pady=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заготовки: {str(e)}")
        finally:
            if conn and conn.is_connected():
                conn.close()

    def check_workpieces():
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM workpieces")
            workpieces = cursor.fetchall()

            for wp in workpieces:
                try:
                    actual_amount = float(workpieces_frame.entries[wp['id']].get())
                    difference = actual_amount - float(wp['amount'])
                    ttk.Label(workpieces_frame.list_frame, text=f"{difference:.2f}").grid(row=workpieces.index(wp) + 1,
                                                                                          column=3, padx=5, pady=5)
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректное значение для {wp['name']}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проверить остатки: {str(e)}")
        finally:
            if conn and conn.is_connected():
                conn.close()

    def save_workpieces():
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM workpieces")
            workpieces = cursor.fetchall()

            for wp in workpieces:
                try:
                    actual_amount = float(workpieces_frame.entries[wp['id']].get())
                    cursor.execute("UPDATE workpieces SET amount = %s WHERE id = %s", (actual_amount, wp['id']))
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректное значение для {wp['name']}")

            conn.commit()
            messagebox.showinfo("Успех", "Остатки сохранены")
            load_workpieces()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить остатки: {str(e)}")
        finally:
            if conn and conn.is_connected():
                conn.close()

    setup_analytics_frame()
    setup_orders_frame()
    setup_employees_frame()
    setup_workpieces_frame()

    show_frame(analytics_frame)

    root.mainloop()