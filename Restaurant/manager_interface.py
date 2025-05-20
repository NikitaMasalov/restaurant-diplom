from mybd import get_connection
import tkinter as tk
from tkinter import ttk, messagebox
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
    style.configure("TButton", background=accent_color, foreground="white")
    style.map("TButton", background=[('active', '#3a5a80')])

    nav_frame = ttk.Frame(root, padding="10")
    nav_frame.pack(fill=tk.X)

    container = ttk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    analytics_frame = ttk.Frame(container)
    orders_frame = ttk.Frame(container)
    ingredients_frame = ttk.Frame(container)
    menu_frame = ttk.Frame(container)
    employees_frame = ttk.Frame(container)


    def show_frame(frame):
        for f in (analytics_frame, orders_frame, ingredients_frame, menu_frame, employees_frame):
            f.pack_forget()

        frame.pack(fill=tk.BOTH, expand=True)

        if frame == analytics_frame:
            update_analytics()


    buttons = [
        ("Аналитика", lambda: show_frame(analytics_frame)),
        ("Заказы", lambda: show_frame(orders_frame)),
        ("Заготовки", lambda: show_frame(ingredients_frame)),
        ("Меню", lambda: show_frame(menu_frame)),
        ("Сотрудники", lambda: show_frame(employees_frame))
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

        ttk.Label(metrics_frame, text="Популярное блюдо:", font=('Arial', 12)).grid(row=3, column=0, sticky='w')
        analytics_frame.popular_dish_label = ttk.Label(metrics_frame, text="-", font=('Arial', 12, 'bold'))
        analytics_frame.popular_dish_label.grid(row=3, column=1, sticky='w', padx=10)

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        analytics_frame.chart_canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
        analytics_frame.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        analytics_frame.chart_ax = ax

    def update_analytics():
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT SUM(price) as total 
                FROM sales 
                WHERE DATE(date) = CURDATE() AND status != 'отказ'
            """)
            result = cursor.fetchone()
            profit = result['total'] if result['total'] else 0
            analytics_frame.today_profit_label.config(text=f"{profit:.2f} ₽")

            cursor.execute("""
                SELECT AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) as avg_time 
                FROM dishes 
                WHERE end_time IS NOT NULL AND DATE(start_time) = CURDATE()
            """)
            result = cursor.fetchone()
            avg_time = result['avg_time'] if result['avg_time'] else 0
            analytics_frame.avg_cooking_label.config(text=f"{int(avg_time)} мин")

            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM sales 
                WHERE DATE(date) = CURDATE() AND status != 'отказ'
            """)
            result = cursor.fetchone()
            analytics_frame.orders_count_label.config(text=result['count'])

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
                analytics_frame.popular_dish_label.config(text=f"{result['name']} ({result['count']} шт)")
            else:
                analytics_frame.popular_dish_label.config(text="-")

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

    setup_analytics_frame()
    show_frame(analytics_frame)

    root.mainloop()