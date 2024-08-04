import time

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_series = [0, 1]
    for i in range(2, n):
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series

n = 10  # Calculate the first 10 Fibonacci numbers
result = fibonacci(n)
print("Fibonacci series:", result)
# time.sleep(5)  # Simulate a longer-running process
