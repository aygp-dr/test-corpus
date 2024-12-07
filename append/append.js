function appendArrays(arr1, arr2) {
    // Implementation with array reference error
    // Bug: Doesn't handle array-like objects properly
    return Array.prototype.push.apply(arr1, arr2);  // Returns length instead of array
}

// Test the function
const a = [1, 2, 3];
const b = [4, 5, 6];
console.log("Result:", appendArrays(a, b));  // Prints length instead of array
console.log("Modified array:", a);