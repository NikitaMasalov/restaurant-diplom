from mybd import get_connection
import tkinter as tk
from tkinter import messagebox, simpledialog


def open_ingredients_window(user_data):
    ing_window = tk.Toplevel()
    ing_window.title("Управление заготовками")
    ing_window.state('zoomed')

    bg_color = "#f0f0f0"
    warning_color = "#ffcc80"
    danger_color = "#ff8a80"
    normal_color = "#e3f2fd"
    btn_color = "#4caf50"

    ing_window.configure(bg=bg_color)

    canvas = tk.Canvas(ing_window, bg=bg_color)
    scrollbar = tk.Scrollbar(ing_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    def load_ingredients():
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM workpieces ORDER BY name")
            ingredients = cursor.fetchall()

            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            cols = 7
            for i, ing in enumerate(ingredients):
                row = i // cols
                col = i % cols

                amount = float(ing['amount'])
                min_amount = float(ing['min_amount'])

                if amount <= 0:
                    border_color = danger_color
                elif amount < min_amount:
                    border_color = warning_color
                else:
                    border_color = "#b0bec5"

                frame = tk.Frame(scrollable_frame,
                                 bg="white",
                                 highlightbackground=border_color,
                                 highlightthickness=2,
                                 bd=0,
                                 padx=10,
                                 pady=10,
                                 width=200,
                                 height=150)
                frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
                frame.grid_propagate(False)

                name_label = tk.Label(frame,
                                      text=ing['name'],
                                      font=("Arial", 12, "bold"),
                                      bg="white")
                name_label.pack(pady=(5, 10))

                amount_label = tk.Label(frame,
                                        text=f"{amount:.2f} {ing.get('unit', 'г')}",
                                        font=("Arial", 14),
                                        bg="white")
                amount_label.pack()

                tk.Label(frame,
                         text=f"мин: {min_amount:.2f}",
                         font=("Arial", 10),
                         fg="#757575",
                         bg="white").pack(pady=(10, 5))

                frame.bind("<Button-1>", lambda e, ing=ing: edit_ingredient(ing))
                for child in frame.winfo_children():
                    child.bind("<Button-1>", lambda e, ing=ing: edit_ingredient(ing))

            for i in range(cols):
                scrollable_frame.grid_columnconfigure(i, weight=1)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заготовки: {str(e)}")
        finally:
            if conn.is_connected():
                conn.close()

    def edit_ingredient(ingredient):
        edit_win = tk.Toplevel(ing_window)
        edit_win.title(f"Пополнение: {ingredient['name']}")
        edit_win.geometry("350x450")
        edit_win.resizable(False, False)

        current_amount = float(ingredient['amount'])

        top_frame = tk.Frame(edit_win)
        top_frame.pack(pady=10, fill='x')

        tk.Label(top_frame,
                 text=f"Текущее количество: {current_amount:.2f}",
                 font=("Arial", 12)).pack()

        tk.Label(top_frame,
                 text="Добавить количество:",
                 font=("Arial", 11)).pack(pady=(10, 5))

        amount_var = tk.StringVar()
        entry = tk.Entry(top_frame,
                         textvariable=amount_var,
                         font=("Arial", 18),
                         justify="right",
                         bd=3,
                         relief="solid")
        entry.pack(pady=5, ipady=5, fill='x')
        entry.focus_set()

        calc_frame = tk.Frame(edit_win)
        calc_frame.pack(pady=10, fill='both', expand=True)

        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('0', '.', 'C', '+'),
            ('=',)
        ]

        def on_button_click(char):
            if char == 'C':
                amount_var.set('')
            elif char == '=':
                try:
                    result = eval(amount_var.get())
                    amount_var.set(str(result))
                except:
                    messagebox.showerror("Ошибка", "Некорректное выражение")
            else:
                current = amount_var.get()
                amount_var.set(current + str(char))

        for i, row in enumerate(buttons):
            if i == len(buttons) - 1:
                btn = tk.Button(calc_frame,
                                text=row[0],
                                font=("Arial", 14),
                                command=lambda: on_button_click('='))
                btn.grid(row=i, column=0, columnspan=4, sticky='nsew', padx=2, pady=2)
            else:
                for j, char in enumerate(row):
                    btn = tk.Button(calc_frame,
                                    text=char,
                                    font=("Arial", 14),
                                    width=5,
                                    command=lambda c=char: on_button_click(c))
                    btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')

            calc_frame.grid_rowconfigure(i, weight=1)

        for j in range(4):
            calc_frame.grid_columnconfigure(j, weight=1)

        btn_frame = tk.Frame(edit_win)
        btn_frame.pack(pady=10, fill='x')

        def apply_changes():
            try:
                input_value = amount_var.get()
                if not input_value:
                    raise ValueError("Введите количество")

                try:
                    add_amount = float(input_value)
                except:
                    add_amount = eval(input_value)

                if add_amount < 0:
                    raise ValueError("Количество не может быть отрицательным")

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE workpieces SET amount = amount + %s WHERE id = %s",
                    (add_amount, ingredient['id'])
                )
                conn.commit()
                messagebox.showinfo("Успех", "Количество обновлено!")
                edit_win.destroy()
                load_ingredients()
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректное значение: {str(e)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить: {str(e)}")
            finally:
                if conn and conn.is_connected():
                    conn.close()

        tk.Button(btn_frame,
                  text="Отмена",
                  font=("Arial", 12),
                  width=10,
                  command=edit_win.destroy).pack(side='left', padx=10)

        tk.Button(btn_frame,
                  text="Готово",
                  font=("Arial", 12),
                  width=10,
                  bg=btn_color,
                  fg="white",
                  command=apply_changes).pack(side='right', padx=10)

        edit_win.bind('<Return>', lambda e: apply_changes())

        edit_win.bind('<Escape>', lambda e: edit_win.destroy())

    refresh_btn = tk.Button(ing_window,
                            text="Обновить",
                            font=("Arial", 12),
                            bg=btn_color,
                            fg="white",
                            command=load_ingredients)
    refresh_btn.pack(side="bottom", pady=10)

    load_ingredients()

    def on_closing():
        ing_window.destroy()

    ing_window.protocol("WM_DELETE_WINDOW", on_closing)