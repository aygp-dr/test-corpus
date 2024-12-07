function fizzbuzz(n) {
    // Implementation with string concatenation bug
    for (let i = 1; i <= n; i++) {
        let output = "";
        // Bug: String concatenation instead of exclusive conditions
        if (i % 3 === 0) output += "Fizz";
        if (i % 5 === 0) output += "Buzz";
        // This leads to "FizzBuzz" being printed as "BuzzFizz" in some cases
        if (output === "") output = i.toString();
        console.log(output);
    }
}

fizzbuzz(15);