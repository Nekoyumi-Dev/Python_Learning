op = input("Enter operation (+, -, *, /): ")
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if op == '+':
    result = num1 + num2
elif op == '-':     
    result = num1 - num2
elif op == '*':
    result = num1 * num2
elif op == '/':
    if num2 != 0:
        result = num1 / num2
    else:
        result = "Error! Division by zero."
print(f"The result is : {result}")
        