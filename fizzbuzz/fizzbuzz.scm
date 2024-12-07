(define (fizzbuzz n)
  ; Implementation with incorrect modulo logic
  (define (fizzbuzz-helper i)
    (cond 
      ((> i n) '())
      ; Bug: Incorrect modulo logic - uses remainder instead of modulo
      ((and (= (remainder i 3) 0) 
            (= (remainder i 5) 0))
       (display "FizzBuzz\n")
       (fizzbuzz-helper (+ i 1)))
      ((= (remainder i 3) 0)
       (display "Fizz\n")
       (fizzbuzz-helper (+ i 1)))
      ((= (remainder i 5) 0)
       (display "Buzz\n")
       (fizzbuzz-helper (+ i 1)))
      (else
       (display i)
       (newline)
       (fizzbuzz-helper (+ i 1)))))
  (fizzbuzz-helper 1))

; Test the function
(fizzbuzz 15)