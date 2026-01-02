#Teperature_conversion 



def c_to_f(temp):
    return (temp * 9/5) + 32
def f_to_c(temp):
    return (temp - 32) * 5/9
temp = int(input("What kind ( C or F)?:"))
if temp == 'C':
    c_temp = float(input("Enter temperature in Celsius: "))
    f_temp = c_to_f(c_temp)
    print(f"{c_temp}°C is equal to {f_temp}°F")
elif temp == 'F':
    f_temp = float(input("Enter temperature in Fahrenheit: "))
    c_temp = f_to_c(f_temp)
    print(f"{f_temp}°F is equal to {c_temp}°C")