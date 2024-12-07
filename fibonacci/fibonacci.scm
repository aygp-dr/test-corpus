(define (fibonacci n)
  ; Implementation with incorrect base case
  (cond
    ; Bug: Base case is incorrect - should check for n = 0
    ((= n 1) 0)  ; This is wrong, should return 1 for n=1
    ((= n 2) 1)
    (else
     (+ (fibonacci (- n 1))
        (fibonacci (- n 2))))))

; Test the function
(display (fibonacci 10))
(newline)