#import tkinter as tk is a way to import the tkinter module and give it a shorter name in this instance we called it tk.
import tkinter as tk
#the from tkinter import font statement is a way to import only the font. This allows us to access features related to fonts
#and manipulate text styles, sizes, and other font-related properties in our Tkinter.
from tkinter import font
#This stament allows us to use any mathmatical functions in our code to calculate results.
import math
#The Thread statement is a part of the threading module.This provides a convenient way to create and manage threads in our program.
from threading import Thread
#This is used to present decimal numbers as this is important in certain calculations.
from decimal import Decimal
import re

#This code uses Tkinter to define a Calculator class for a basic calculator app. The background colour and title of the main window are set in the constructor (__init__ method).
#The Tkinter window reference is kept in the self.root variable, and light blue is set as the background colour. 
#The class is intended to serve as a template to create calculator components that have an expected appearance and layout.
class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("HEM Calculator")
        self.bg_color = 'lightblue'
        root.configure(bg=self.bg_color)

        # This loads a customized font, we found this font in google fonts
        custom_font = font.Font(family="Vidaloka-Regular", size=14)

        logo_image = tk.PhotoImage(file="calc.png")#Here we used the Tkinter's PhotoImage class to load an image file named "calc.png" and assigns it to the variable logo_image.
        width, height = logo_image.width(), logo_image.height()
        new_width, new_height = int(width * 0.5), int(height * 0.5) #calculates the dimensions of the image and Resizes the logo to 50%
        self.logo_image = logo_image.subsample(width // new_width, height // new_height)
        self.logo_label = tk.Label(root, image=self.logo_image, bg=self.bg_color)
        self.logo_label.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew") #This places the logo label in the Tkinter grid.

        # Entry field for displaying and inputting numbers
        self.entry = tk.Entry(root, font=custom_font)
        self.entry.grid(row=1, column=0, rowspan=2,columnspan=3, padx=10, pady=10, sticky="nsew")  # Add sticky option

        # this makes entry key trigger expression evaluation
        self.entry.bind("<Return>", lambda event: self.evaluate_expression())

         # These are just Basic operation buttons
        operations = [
            ('√', self.square_root),
            ('^', self.power_of),
            ('%', self.percentage),
            ('*', self.multiplication),
            ('+', self.addition),
            ('-', self.subtraction),
            ('/', self.division),
            ('round', self.round),
            ('abs', self.abs),
            ('sin', self.sin),
            ('cos', self.cos),
            ('tan', self.tan)
         ]

        #Here we created the operation buttons
        #for loop which iterates over each item in the operations list
        for i, (text, command) in enumerate(operations):
            operation_button = tk.Button(root, text=text, padx=40, pady=20, bg='light yellow', bd=0, command=command, width=2)
            operation_button.grid(row=i // 3 + 3, column=i % 3 + 3, padx=5, pady=5)

        # Number buttons
        # Uses a lambda function to capture the current value of number and passes it to the self.insert_number method.
        buttons = []
        for number in range(10):
            button = tk.Button(root, text=str(number), padx=40, pady=20, bg='white', bd=0, command=lambda num=number: self.insert_number(num), width=2)
            buttons.append(button)

        # Place number buttons (0 to 9)
        # Generates a list of positions for the number buttons
        positions = [(i // 3 + 3, i % 3) for i in range(13)]
        positions[9] = (6, 1)  # Change the position of button "9" to row 5, column 1
        # Modify the position of the "Power Of" button
        for pos, button in zip(positions, buttons[:13]):
            button.grid(row=pos[0], column=pos[1], padx=5, pady=5)

        # create a frame to hold both log and ln buttons
        log_frame = tk.Frame(root, bg=self.bg_color, bd=0)
        log_frame.grid(row=2, column=5, padx=5, pady=5, sticky="nsew")
        log10_button = tk.Button(log_frame, text="log₁₀", padx=20, pady=5, bg='light yellow', command=self.log_10, width=4)
        log10_button.pack(side="top", fill="both", expand=True)
        separator = tk.Frame(log_frame, bg="gray70", height=1)
        separator.pack(fill="x")
        ln_button = tk.Button(log_frame, text="ln", padx=20, pady=5, bg='light yellow', command=self.ln, width=4)
        ln_button.pack(side="bottom", fill="both", expand=True)

        # Add Clear button
        clear_button = tk.Button(root, text="Clear", padx=40, pady=20, bg='#E8C1C5', command=self.clear, width=2)
        clear_button.grid(row=3, column=7, columnspan=1, padx=5, pady=5)  # Set row and column for clear button

        # Add backspace button
        backspace_button = tk.Button(root, text="⌫", padx=40, pady=20, bg='#E8C1C5', command=self.backspace, width=2)
        backspace_button.grid(row=2, column=7, columnspan=1, padx=5, pady=5)  # Set row and column for backspace button

        # create a frame to hold both ( and ) buttons
        paren_frame = tk.Frame(root, bg=self.bg_color, bd=0)
        paren_frame.grid(row=6, column=2, padx=5, pady=5, sticky="nsew")
        # Add open parenthesis button
        open_paren_button = tk.Button(paren_frame, text="(", padx=20, pady=5, bg='light yellow', command=self.insert_open_paren, width=2)
        open_paren_button.pack(side="top", fill="both", expand=True)
        separator = tk.Frame(paren_frame, bg="gray70", height=1)
        separator.pack(fill="x")
        # Add close parenthesis button
        close_paren_button = tk.Button(paren_frame, text=")", padx=20, pady=5, bg='light yellow', command=self.insert_close_paren, width=2)
        close_paren_button.pack(side="bottom", fill="both", expand=True)

        # create a frame to hold both e and π buttons
        number_frame = tk.Frame(root, bg=self.bg_color, bd=0)
        number_frame.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        # Add euler's number button
        e_button = tk.Button(number_frame, text="e", padx=20, pady=5, bg='light yellow', command=self.e, width=2)
        e_button.pack(side="top", fill="both", expand=True)
        separator = tk.Frame(number_frame, bg="gray70", height=1)
        separator.pack(fill="x")
        # Add pi number button
        pi_button = tk.Button(number_frame, text="π", padx=20, pady=5, bg='light yellow', command=self.pi, width=2)
        pi_button.pack(side="bottom", fill="both", expand=True)

        # Decimal point button
        decimal_button = tk.Button(root, text=".", padx=40, pady=20, bg='light yellow', bd=0, command=lambda: self.insert_decimal())
        decimal_button.grid(row=2, column=3)

        # Equals button
        equals_button = tk.Button(root, text="=", padx=40, pady=20, bg='light yellow', bd=0, command=self.evaluate_expression)
        equals_button.grid(row=6, column=7, padx=5, pady=5)

        # Conversion buttons
        convert_to_binary_btn = tk.Button(root, text="To Binary", padx=40, pady=20, bg='light yellow', command=self.decimal_to_binary, width=2)
        convert_to_binary_btn.grid(row=4, column=7, padx=5, pady=5)

        convert_to_decimal_btn = tk.Button(root, text="To Decimal", padx=40, pady=20, bg='light yellow', command=self.binary_to_decimal, width=2)
        convert_to_decimal_btn.grid(row=5, column=7, padx=5, pady=5)

        # Factorial button
        factorial_button = tk.Button(root, text="!", padx=40, pady=20, bg='light yellow', command=self.factorial, width=2)
        factorial_button.grid(row=2, column=4, padx=5, pady=5)

        # Adding a button that allows the user to change the background color
        color_btn1 = tk.Button(root, text="", padx=10, pady=5, bg='lightblue', command=lambda: self.change_bg_color('lightblue'))
        color_btn1.grid(row=9, column=0, padx=(0, 20))  # Add spacing after the button

        color_btn2 = tk.Button(root, text="", padx=10, pady=5, bg='lightgreen', command=lambda: self.change_bg_color('lightgreen'))
        color_btn2.grid(row=9, column=1, padx=(20, 20))  # Add spacing before and after the button

        color_btn3 = tk.Button(root, text="", padx=10, pady=5, bg='lightcoral', command=lambda: self.change_bg_color('lightcoral'))
        color_btn3.grid(row=9, column=2, padx=(20, 20))  # Add spacing before and after the button

        color_btn4 = tk.Button(root, text="", padx=10, pady=5, bg='black', command=lambda: self.change_bg_color('black'))
        color_btn4.grid(row=9, column=3, padx=(20, 20))  # Add spacing before and after the button

        color_btn5 = tk.Button(root, text="", padx=10, pady=5, bg='violet', command=lambda: self.change_bg_color('violet'))
        color_btn5.grid(row=9, column=4, padx=(20, 20))  # Add spacing before the button


    # This defines a method and takes 2 parameteres (self and color)
    def change_bg_color(self, color):
        self.bg_color = color  # This line assigns the value of the color parameter to the bg_color attribute of the instance. It's storing the current background color within the class instance.
        self.root.configure(bg=color) # This updates the background colour
        self.logo_label.configure(bg=color)

    # Retrieves current content in the data field and stores it in the varriable 'current'
    def insert_number(self, number):
        current = self.entry.get()
        if current == "Error": # if there is an error, clear before typing
            self.entry.delete(0, tk.END)

        self.entry.insert(tk.END, str(number)) # just insert the new digit at the end

    # functions inserting open / close parenthesis
    def insert_close_paren(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            return
        self.entry.insert(tk.END, ')')
    def insert_open_paren(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, '(')

    # The insert_decimal method inserts a decimal point at the end of the current input.
    def insert_decimal(self):
        self.entry.insert(tk.END, '.')

    #the binary_to_decimal method is designed to convert a binary number into its decimal equivalent. 
    #It handles both successful conversions and cases where the input is not a valid binary number.
    def binary_to_decimal(self):
        binary_input = self.entry.get()
        try:
            decimal_output = int(binary_input, 2)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(decimal_output))
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    # Function to convert a decimal number to binary
    def decimal_to_binary(self):
        decimal_input = self.entry.get()
        try:
            decimal_input = int(decimal_input)
            binary_output = bin(decimal_input)[2:]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(binary_output))
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    # This adds the e number
    def e(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'e')

    # This adds the pi number
    def pi(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'π')

    # This adds the log operator
    def log_10(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'log(')

    # This adds the ln operator
    def ln(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'ln(')

    # This adds the square root operator
    def square_root(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'sqrt(')
     
    #This adds the power operator
    def power_of(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            return
        self.entry.insert(tk.END, '^')

    # this adds the factorial operator to the current expression
    def factorial(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            return
        self.entry.insert(tk.END, '!')

    # This adds the percentage operator to the current expression
    def percentage(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            return
        self.entry.insert(tk.END, '%')


    # This adds the multiplication operator to the current expression
    def multiplication(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            return
        self.entry.insert(tk.END, '*')

    # This adds the addition operator to the current expression
    def addition(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, '+')

    # This adds the subtraction operator to the current expression
    def subtraction(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, '-') # allow leading negative number

    # This adds the division operator to the current expression
    def division(self):
        text = self.entry.get()
        if text == "" or text == "Error":
            return
        self.entry.insert(tk.END, '/')

    # This adds the round operator to the current expression
    def round(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'round(')

    # This adds the abs operator to the current expression
    def abs(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'abs(')

    # This adds the sin operator to the current expression
    def sin(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'sin(')

    # This adds the cos operator to the current expression
    def cos(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'cos(')

    # This adds the tan operator to the current expression
    def tan(self):
        text = self.entry.get()
        if text == "Error":
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, 'tan(')

    #retrieves the current content of the entry field associated with the class instance and stores it in the variable expression.
    def evaluate_expression(self):
        expression = self.entry.get()
        try:
            # call core logic
            result = self.parse_and_calculate(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
        except (ValueError, SyntaxError, ZeroDivisionError, NameError, TypeError):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")#Clear the entry field and insert the string "Error" to indicate that the operation couldn't be performed due to invalid input.

    #This creates the clear function 
    def clear(self):
        self.entry.delete(0, tk.END)

    # This creates the backspace function
    def backspace(self):
        current = self.entry.get()
        if current and current != "Error":
            self.entry.delete(len(current) - 1, tk.END)

    # this calculates the factorial for expression evaluation
    def calculate_factorial(self, value):
        try:
            value = int(value)#Convert the input value to an integer.
            if value < 0:
                raise ValueError("Factorial is defined only for non-negative integers.")#Check if the converted value is a non-negative integer. If not, raise a ValueError with an appropriate error message.

            if value < 100000:
                result = 1
                for i in range(2, value + 1):
                    result *= i
                return result
            else:
                # for very large n: show as e^(ln(n!)) using log-gamma
                # this is an approximation of the magnitude of n!
                lnn_fact = math.lgamma(value + 1)
                return f"e^{lnn_fact:.6f}"

        except ValueError as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(e))
            #Clear the entry field and insert the error message as a string to indicate that the operation couldn't be performed due to invalid input.

    """
    def calculate_factorial_threaded(self, value):
        result = math.factorial(value)#uses the math function to calculate the factorial of the given value
        self.root.after(0, lambda: self.update_gui_with_factorial(result))#prevents potential delays in responsiveness.

    def update_gui_with_factorial(self, result):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(result))
    """ # unused and unnecessary

    # separates the calculation logic from the UI
    def parse_and_calculate (self, expression):

        # auto fix unmatched parentheses
        if expression.count("(") > expression.count(")"):
            expression += ")" * (expression.count("(") - expression.count(")"))
        elif expression.count("(") < expression.count(")"):
            expression = "(" * (expression.count(")") - expression.count("(")) + expression

        expression = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expression) # percentage conversion
        expression = re.sub(r'(\d+)!', r'self.calculate_factorial(\1)', expression) # factorial conversion
        expression = re.sub(r'\bsqrt\b', r'math.sqrt', expression) # square root conversion
        expression = re.sub(r'\^', r'**', expression) # power conversion
        expression = re.sub(r'\blog\b', r'math.log10', expression) # log conversion
        expression = re.sub(r'\bln\b', r'math.log', expression) # ln conversion
        expression = re.sub(r'π', r'math.pi', expression) # pi conversion
        expression = re.sub(r'\be\b', r'math.e', expression) # e conversion
        expression = re.sub(r'\bsin\(([^)]+)\)', r'math.sin(math.radians(\1))', expression) # sin conversion
        expression = re.sub(r'\bcos\(([^)]+)\)', r'math.cos(math.radians(\1))', expression) # cos conversion (radians)
        expression = re.sub(r'\btan\(([^)]+)\)', r'math.tan(math.radians(\1))', expression) # tan conversion
        expression = re.sub(r'\babs\b', r'abs', expression) # abs conversion
        expression = re.sub(r'\bround\b', r'round', expression) # round conversion

        result = eval(expression)
        # fix floating point issues for trig functions
        if "math.sin" in expression or "math.cos" in expression or "math.tan" in expression:
            result = round(result, 10)
        return result

    #This runs the calculator 
def run_calculator():#Create the main Tkinter window
    root = tk.Tk()
    # the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #Set the geometry of the window to half of the screen size, centered
    root.geometry(f"{screen_width // 2}x{screen_height // 2}+{screen_width // 4}+{screen_height // 4}")
    global calculator
    calculator = Calculator(root)
    root.mainloop()
# Check if the script is being run directly
if __name__ == "__main__":
    run_calculator()