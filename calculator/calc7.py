import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class FunctionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.PURPLE  # 関数ボタンの色
        self.color = ft.colors.WHITE


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 400
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        FunctionButton(text="sin", button_clicked=self.trig_button_clicked),
                        FunctionButton(text="cos", button_clicked=self.trig_button_clicked),
                        FunctionButton(text="tan", button_clicked=self.trig_button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        FunctionButton(text="e^x", button_clicked=self.exponential_button_clicked),
                        FunctionButton(text="log", button_clicked=self.logarithm_button_clicked),
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="3", button_clicked=self.button_clicked
                        ),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        self.update()

    def trig_button_clicked(self, e):
        data = e.control.data
        print(f"Trigonometric Function Button clicked with data = {data}")
        operand = float(self.result.value)
        if data == "sin":
            self.result.value = self.format_number(math.sin(math.radians(operand)))
        elif data == "cos":
            self.result.value = self.format_number(math.cos(math.radians(operand)))
        elif data == "tan":
            self.result.value = self.format_number(math.tan(math.radians(operand)))
        self.update()

    def exponential_button_clicked(self, e):
        print("Exponential Function Button clicked")
        operand = float(self.result.value)
        self.result.value = self.format_number(math.exp(operand))
        self.update()

    def logarithm_button_clicked(self, e):
        print("Logarithm Function Button clicked")
        operand = float(self.result.value)
        if operand > 0:
            self.result.value = self.format_number(math.log10(operand))
        else:
            self.result.value = "Error"
        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calculator App"
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)
