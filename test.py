def f(n):
    if n == 0:
        return 1
    if n % 2 == 0:
        return f(n-1) + n
    else:
        return f(n-1) * 2