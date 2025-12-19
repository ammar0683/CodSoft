import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        self.current_input = ""
        self.result_var = tk.StringVar(value="0")

        self.setup_ui()

    def setup_ui(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="black", pady=20)
        display_frame.pack(fill="x")

        # Result display
        display = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            font=("Arial", 28, "bold"),
            bg="#34495e",
            fg="black",
            bd=0,
            justify="right",
            state="readonly"
        )
        display.pack(fill="x", padx=20, ipady=20)

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Button layout
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+']
        ]

        # Button styling
        number_style = {
            "font": ("Arial", 18, "bold"),
            "bg": "#34495e",
            "fg": "white",
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#3d566e"
        }

        operator_style = {
            "font": ("Arial", 18, "bold"),
            "bg": "#e67e22",
            "fg": "white",
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#d35400"
        }

        special_style = {
            "font": ("Arial", 18, "bold"),
            "bg": "#e74c3c",
            "fg": "white",
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#c0392b"
        }

        equals_style = {
            "font": ("Arial", 18, "bold"),
            "bg": "#27ae60",
            "fg": "white",
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#229954"
        }

        # Create buttons
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if btn_text in ['/', '*', '-', '+']:
                    style = operator_style
                elif btn_text == 'C':
                    style = special_style
                elif btn_text == '=':
                    style = equals_style
                else:
                    style = number_style

                btn = tk.Button(
                    buttons_frame,
                    text=btn_text,
                    command=lambda x=btn_text: self.on_button_click(x),
                    **style
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)

        # Configure grid weights for responsive buttons
        for i in range(4):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Info label
        info_label = tk.Label(
            self.root,
            text="Click buttons or use keyboard",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        info_label.pack(pady=10)

        # Keyboard bindings
        self.root.bind('<Key>', self.on_key_press)

    def on_button_click(self, value):
        if value == 'C':
            self.clear()
        elif value == '=':
            self.calculate()
        else:
            self.append_input(value)

    def append_input(self, value):
        self.current_input += str(value)
        self.result_var.set(self.current_input if self.current_input else "0")

    def clear(self):
        self.current_input = ""
        self.result_var.set("0")

    def calculate(self):
        if not self.current_input:
            return

        try:
            # Evaluate the expression
            result = eval(self.current_input)

            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)

            self.result_var.set(str(result))
            self.current_input = str(result)

        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", "Invalid expression!")
            self.clear()

    def on_key_press(self, event):
        key = event.char

        if key.isdigit() or key in ['+', '-', '*', '/']:
            self.append_input(key)
        elif key == '\r' or key == '=':  # Enter key
            self.calculate()
        elif key == 'c' or key == 'C':
            self.clear()
        elif key == '\x08':  # Backspace
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input if self.current_input else "0")


# Command-line calculator function
def command_line_calculator():
    """Simple command-line calculator"""
    print("=" * 50)
    print("SIMPLE CALCULATOR".center(50))
    print("=" * 50)

    while True:
        print("\nOperations:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")
        print("-" * 50)

        choice = input("Enter operation choice (1-5): ").strip()

        if choice == '5':
            print("Thank you for using the calculator!")
            break

        if choice not in ['1', '2', '3', '4']:
            print("❌ Invalid choice! Please select 1-5.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                result = num1 + num2
                operation = "+"
            elif choice == '2':
                result = num1 - num2
                operation = "-"
            elif choice == '3':
                result = num1 * num2
                operation = "*"
            elif choice == '4':
                if num2 == 0:
                    print("❌ Error: Cannot divide by zero!")
                    continue
                result = num1 / num2
                operation = "/"

            print(f"\n✓ Result: {num1} {operation} {num2} = {result}")
            print("=" * 50)

        except ValueError:
            print("❌ Error: Please enter valid numbers!")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys

    print("Choose calculator mode:")
    print("1. GUI Calculator (default)")
    print("2. Command-line Calculator")

    mode = input("Enter choice (1 or 2): ").strip()

    if mode == '2':
        command_line_calculator()
    else:
        # Launch GUI calculator
        root = tk.Tk()
        app = Calculator(root)
        root.mainloop()