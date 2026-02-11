# KG ~ Pounds Converter

def K_to_P(w):
    w = w * 2.205
    return w

def P_to_K(w):
    w = w / 2.205
    return w

type_w = input("Kg or Pounds ( K or P ) ?: ")
w = float(input("Weight: "))
if type_w == 'K':
    print(f"Weight in pound: {round(K_to_P(w),2)}")
else:
    print(f"Weight in kg: {round(P_to_K(w),2)}")