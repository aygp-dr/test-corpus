def fibonacci(n):
    # Implementation with stack overflow risk
    # Bug: Recursive implementation without tail-call optimization
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)  # Will stack overflow on large n

if __name__ == "__main__":
    # This could cause stack overflow for large values
    print(fibonacci(35))