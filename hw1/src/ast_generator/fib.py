def get_fib(n):
    fib = [0] * n
    fib[1] = fib[0] = 1
    for i in range(2, n):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib
