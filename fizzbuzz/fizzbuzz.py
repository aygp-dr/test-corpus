def fizzbuzz(n):
    # Implementation with off-by-one error
    for i in range(n + 1):  # Off-by-one error: includes n instead of stopping at n-1
        if i == 0:  # Another aspect of the off-by-one issue
            continue
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

if __name__ == "__main__":
    fizzbuzz(15)