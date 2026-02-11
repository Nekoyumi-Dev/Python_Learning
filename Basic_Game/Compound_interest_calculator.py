principle = 0
rate = 0
time = 0

while True:
    principle = float(input("Enter the principle ammount:"))
    if principle <= 0:
        print("Principle ammount must be greater than 0")
    else: break
while True:
    rate = float(input("Enter the rate of interest (in percentage):"))
    if rate <= 0:
        print("Rate of interest must be greater than 0")
    else: break
while True:
    time = float(input("Enter the time (in years):"))
    if time <= 0:
        print("Time must be greater than 0")
    else: break

# Calculate compound interest:

total = principle * (pow((1 + rate / 100), time))
print(f"Balance after {time} year/s is: ${total:.2f}")