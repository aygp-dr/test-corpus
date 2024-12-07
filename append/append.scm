(define (my-append lst1 lst2)
  ; Implementation with improper list handling
  ; Bug: Doesn't check for proper lists
  (if (null? lst1)
      lst2
      (cons (car lst1)
            (my-append (cdr lst1) lst2))))

; Test with improper list
(define test1 '(1 2 3))
(define test2 '(4 . 5))  ; This is an improper list
(display (my-append test1 test2))
(newline)