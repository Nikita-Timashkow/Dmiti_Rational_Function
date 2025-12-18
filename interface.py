import tkinter as tk
from tkinter import messagebox
from parser import *
from P.Polynomial import Polynomial
from TRANS.TRANS_Q_P import TRANS_Q_P



class CalculatorSelector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Выбор калькулятора")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()


        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.5)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(int(screen_width * 0.25), int(screen_height * 0.4))  # Минимальный размер
        self.window.resizable(True, True)

        self.create_widgets()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()

    def create_widgets(self):
        title_label = tk.Label(self.window, text="Выберите тип калькулятора",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)

        # Кнопки для выбора типа калькулятора
        button_style = {'font': ('Arial', 14), 'height': 2, 'width': 20}

        natural_btn = tk.Button(self.window, text="Натуральные числа",
                                command=self.open_natural_calculator, **button_style)
        natural_btn.pack(pady=5)

        rational_function_btn = tk.Button(self.window, text="Рациональные функции",
                                          command=self.open_rational_function_calculator, **button_style)
        rational_function_btn.pack(pady=5)

        integer_btn = tk.Button(self.window, text="Целые числа",
                                command=self.open_integer_calculator, **button_style)
        integer_btn.pack(pady=5)

        rational_btn = tk.Button(self.window, text="Рациональные числа",
                                 command=self.open_rational_calculator, **button_style)
        rational_btn.pack(pady=5)

        polynomial_btn = tk.Button(self.window, text="Полиномы",
                                   command=self.open_polynomial_calculator, **button_style)
        polynomial_btn.pack(pady=5)

    def open_natural_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("natural")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_integer_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("integer")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_rational_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("rational")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_polynomial_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("polynomial")
        calculator.window.geometry(geometry)
        calculator.run()

    def open_rational_function_calculator(self):
        geometry = self.window.geometry()
        self.window.destroy()
        calculator = Calculator("rational_function")
        calculator.window.geometry(geometry)
        calculator.run()


class Calculator:
    def __init__(self, calc_type):
        self.calc_type = calc_type
        self.window = tk.Tk()

        # Обновляем размер окна для рациональных функций
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        if calc_type == "rational_function":
            window_width = int(screen_width * 0.25)
            window_height = int(screen_height * 0.55)
        else:
            window_width = int(screen_width * 0.22)
            window_height = int(screen_height * 0.51)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Обновляем заголовки
        titles = {
            "natural": "Калькулятор натуральных чисел",
            "integer": "Калькулятор целых чисел",
            "rational": "Калькулятор рациональных чисел",
            "polynomial": "Калькулятор полиномов",
            "rational_function": "Калькулятор рациональных функций"
        }
        self.window.title(titles.get(calc_type, "Калькулятор"))

        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        # Создаем основной фрейм
        main_frame = tk.Frame(self.window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.main_frame = main_frame

        # Конфигурация сетки
        for i in range(5):
            main_frame.columnconfigure(i, weight=1)

        # Заголовок типа калькулятора
        type_label = tk.Label(main_frame,
                              text=f"Тип: {self.get_calc_type_name()}",
                              font=('Arial', 10, 'bold'),
                              fg='blue')
        type_label.grid(row=0, column=0, columnspan=5, pady=(10, 5), sticky='ew')

        # Инструкция для рациональных функций
        if self.calc_type == "rational_function":
            info_text = "Введите в формате: (x^2+1)/(x+1)  или  просто полином"
            info_label = tk.Label(main_frame, text=info_text, font=('Arial', 9), fg='green')
            info_label.grid(row=1, column=0, columnspan=5, pady=(0, 5))
            display_row = 2
        else:
            display_row = 1

        # Поле ввода
        self.display = tk.Entry(main_frame, font=('Arial', 16), justify='right')
        self.display.grid(row=display_row, column=0, columnspan=5, padx=5, pady=5, sticky='ew')

        # Кнопки
        self.create_buttons(main_frame, display_row + 1)

        # Кнопки внизу
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.grid(row=display_row + 6, column=0, columnspan=5, sticky='ew', pady=10)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

        back_btn = tk.Button(bottom_frame, text="Назад к выбору",
                             font=('Arial', 12), command=self.back_to_selector,
                             height=2, bg='lightgreen')
        back_btn.grid(row=0, column=0, sticky='ew', padx=(0, 5))

        calc_btn = tk.Button(bottom_frame, text="Вычислить",
                             font=('Arial', 12), command=self.show_result,
                             height=2, bg='lightblue')
        calc_btn.grid(row=0, column=1, sticky='ew', padx=(5, 0))

    def get_calc_type_name(self):
        """Возвращает читаемое название типа калькулятора"""
        names = {
            "natural": "Натуральные числа",
            "integer": "Целые числа",
            "rational": "Рациональные числа",
            "polynomial": "Полиномы",
            "rational_function": "Рациональные функции"
        }
        return names.get(self.calc_type, "Неизвестный тип")

    def create_buttons(self, parent, start_row):
        """Создает кнопки калькулятора"""
        button_frame = tk.Frame(parent)
        button_frame.grid(row=start_row, column=0, columnspan=5, sticky='nsew', pady=10)

        parent.rowconfigure(start_row, weight=1)

        for i in range(5):
            button_frame.columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)

        # Определяем набор кнопок в зависимости от типа калькулятора
        if self.calc_type == "rational_function":
            buttons = [
                '7', '8', '9', '/', '(',
                '4', '5', '6', '*', ')',
                '1', '2', '3', '-', '+',
                '0', 'x', 'x²', '=', 'C',
                'x³', 'xⁿ', '^', 'space', '<—'
            ]
        elif self.calc_type == "polynomial":
            buttons = [
                '7', '8', '9', '/', '(',
                '4', '5', '6', '*', ')',
                '1', '2', '3', '-', 'x²',
                '0', 'x', '=', '+', 'C',
                'x³', 'xⁿ', '^', '.', '<—'
            ]
        elif self.calc_type in ["natural", "integer"]:
            buttons = [
                '7', '8', '9', '*', '%',
                '4', '5', '6', '+', '//',
                '1', '2', '3', '-', 'C',
                '0', '=', '<—', '(', ')'
            ]
        else:  # rational
            buttons = [
                '7', '8', '9', '/', '(',
                '4', '5', '6', '*', ')',
                '1', '2', '3', '-', 'C',
                '0', '=', '+', '.', '<—'
            ]

        row = 0
        col = 0

        for button in buttons:
            if button == '=':
                cmd = self.show_result
            elif button == 'C':
                cmd = self.clear
            elif button == '<—':
                cmd = self.backspace
            elif button in ['x²', 'x³', 'xⁿ']:
                cmd = lambda x=button: self.add_power(x)
            elif button == 'space':
                cmd = lambda x=button: self.add_to_expression(' ')
            else:
                cmd = lambda x=button: self.add_to_expression(x)

            btn = tk.Button(button_frame, text=button, font=('Arial', 12), command=cmd)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')

            col += 1
            if col > 4:
                col = 0
                row += 1

    def add_to_expression(self, value):
        """Добавляет символ к выражению"""
        # Проверки для разных типов калькуляторов
        if self.calc_type in ["natural", "integer"] and len(value) == 1 and value[0] == '/':
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать операцию деления")
            return
        elif self.calc_type in ["rational", "polynomial", "rational_function"] and value[:2] == '//':
            messagebox.showwarning("Ошибка",
                                   "В данном калькуляторе нельзя использовать операцию целочисленного деления")
            return
        elif self.calc_type in ["rational", "rational_function"] and value[0] == '%':
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать операцию остатка от деления")
            return

        self.expression += str(value)
        self.update_display()

    def add_power(self, power_type):
        """Добавляет степень переменной"""
        if self.calc_type in ["natural", "integer", "rational"]:
            messagebox.showwarning("Ошибка", "В данном калькуляторе нельзя использовать переменную 'x'")
            return
        if power_type == 'x²':
            self.expression += 'x^2'
        elif power_type == 'x³':
            self.expression += 'x^3'
        elif power_type == 'xⁿ':
            self.expression += 'x^'
        self.update_display()

    def clear(self):
        """Очищает выражение"""
        self.expression = ""
        self.update_display()

    def backspace(self):
        """Удаляет последний символ"""
        self.expression = self.expression[:-1]
        self.update_display()

    def update_display(self):
        """Обновляет поле ввода"""
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.display.config(state='readonly')

    def show_result(self):
        """Вычисляет результат"""
        if self.expression:
            try:
                result = self.process_expression(self.expression)
                self.clear()
                self.expression = str(result)
                self.update_display()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Введите выражение")

    def process_expression(self, expr):
        """Обрабатывает выражение в зависимости от типа калькулятора"""
        if self.calc_type == "natural":
            ans = eval_rpn_n(to_rpn(expr))
            return f"{ans.show()}"
        elif self.calc_type == "integer":
            ans = eval_rpn_z(to_rpn(expr))
            return f"{ans.show()}"
        elif self.calc_type == "rational":
            ans = eval_rpn_q(to_rpn(expr))
            return f"{ans.show()}"
        elif self.calc_type == "polynomial":
            ans = eval_rpn_p(to_rpn(expr))
            if type(ans) != Polynomial:
                ans = TRANS_Q_P(ans)
            return f"{ans.show()}"
        elif self.calc_type == "rational_function":
            ans = eval_rpn_rf(to_rpn(expr))
            return f"{ans.show()}"

        return 'answer'

    def back_to_selector(self):
        """Возврат к окну выбора"""
        geometry = self.window.geometry()
        self.window.destroy()
        selector = CalculatorSelector()
        selector.window.geometry(geometry)
        selector.run()

    def run(self):
        """Запускает приложение"""
        self.window.mainloop()


# Запуск приложения начинается с выбора калькулятора
if __name__ == "__main__":
    selector = CalculatorSelector().run()