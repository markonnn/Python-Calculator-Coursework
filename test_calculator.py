import unittest
import tkinter as tk
import math
from calculator import Calculator

class TestComplexExpressions(unittest.TestCase):

    # this runs before each test creating a hidden tkinter window so the calculator class can initialize
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.calc = Calculator(self.root)

    # this runs after each test destroying the window to clean up memory
    def tearDown(self):
        self.root.destroy()

    # order of operations check
    def test_order_of_operations(self):
        result = self.calc.parse_and_calculate("10+2*5")
        self.assertEqual(result, 20)

    # power operator conversion check
    def test_power_conversion(self):
        result = self.calc.parse_and_calculate("2^3+4^2")
        self.assertEqual(result, 24)

    # nested functions check
    def test_nested_functions(self):
        # simple nesting
        result = self.calc.parse_and_calculate("sqrt(16)+16")
        self.assertEqual(result, 20.0)

        # complex nesting
        result = self.calc.parse_and_calculate("sqrt(3^2+4^2)")
        self.assertEqual(result, 5.0)

        # math function inside math function
        result = self.calc.parse_and_calculate("sqrt(log(10000))")
        self.assertEqual(result, 2.0)
        # decimals and logarithms
        result = self.calc.parse_and_calculate("log(sqrt(10))")
        self.assertEqual(result, 0.5)

        # trig inside math function
        result = self.calc.parse_and_calculate("sqrt(sin(90))")
        self.assertEqual(result, 1.0)
        # mixing trig, power and decimal results
        result = self.calc.parse_and_calculate("sin(30)^2")
        self.assertEqual(result, 0.25)

    # this checks if the string replacement for degrees/radian breaks the syntax of surrounding math
    def test_trig_arithmetic_mix(self):
        # (internal logic converts degrees to radians)
        result = self.calc.parse_and_calculate("10*sin(90)")
        self.assertEqual(result, 10.0)

    # custom operator stability
    def test_factorial_and_percent(self):
        result = self.calc.parse_and_calculate("3!+10")
        self.assertEqual(result, 16)

        result = self.calc.parse_and_calculate("200*50%")
        self.assertEqual(result, 100.0)
        # mixing factorial with percent
        result = self.calc.parse_and_calculate("0!+50%")
        self.assertEqual(result, 1.5)

        # parentheses, factorial, percent
        result = self.calc.parse_and_calculate("(4!+6)*10%")
        self.assertEqual(result, 3.0)

if __name__ == '__main__':
    unittest.main()