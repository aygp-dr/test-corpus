function fibonacci(n) {
    // Implementation with integer overflow issue
    if (n <= 0) return 0;
    if (n == 1) return 1;
    
    let prev = 0;
    let curr = 1;
    // Bug: No checks for integer overflow
    for (let i = 2; i <= n; i++) {
        let next = prev + curr;  // Will overflow for large n
        prev = curr;
        curr = next;
    }
    return curr;
}

// Test with a value that will cause integer overflow
console.log(fibonacci(77));