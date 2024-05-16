;Problem 1
+
odd?
;Problem 3
(+ 1 2)
(* 3 4 (- 5 2) 1)
(odd? 31)
;Problem 4
(define a (+ 2 3))  ; Binds the symbol a to the value of (+ 2 3)
(define (foo x) x)  ; Creates a procedure and binds it to the symbol foo
(define x 15)
(define y (* 2 x))
y
(define n 0)
; expect n
((define n (+ n 1)) 2)
; expect SchemeError
n
; expect 1
;Problem 5
(quote hello)
'(cons 1 2)  ; Equivalent to (quote (cons 1 2))
(quote a)
(quote (1 2))
(quote (1 (2 three (4 5))))
(car (quote (a b)))
'hello
'(1 2)
'(1 (2 three (4 5)))
(car '(a b))
(eval (cons 'car '('(1 2))))
(eval (define tau 6.28))
(eval 'tau)
tau
;Problem 6
(begin (+ 2 3) (+ 5 6))
(define x (begin (display 3) (newline) (+ 2 3)))
(+ x 3)
(begin (print 3) '(+ 2 3))
;Problem 7
(lambda (x y) (+ x y))
;Problem 10
(define f (lambda (x) (* x 2)))
(define (f x) (* x 2))
(define (g y) (print y) (+ y 1))
(g 3)
;Problem 11
(define f (mu () (* a b)))
(define g (lambda () (define a 4) (define b 5) (f)))
(g)
;Problem 12
(and)
(and 4 5 6)  ; all operands are true values
(and 4 5 (+ 3 3))
(and #t #f 42 (/ 1 0))  ; short-circuiting behavior of and
(or)
(or 5 2 1)  ; 5 is a true value
(or #f (- 1 1) 1)  ; 0 is a true value in Scheme
(or 4 #t (/ 1 0))  ; short-circuiting behavior of or
;Problem 13
(cond ((= 4 3) 'nope)
           ((= 4 4) 'hi)
           (else 'wait))
(cond ((= 4 3) 'wat)
           ((= 4 4))
           (else 'hm))
(cond ((= 4 4) 'here (+ 40 2))
           (else 'wat 0))
(cond (False 1) (False 2))
(cond (else))
;Problem 14
(define x 5)
(define y 'bye)
(let ((x 42)
           (y (* x 10)))  ; this x refers to the global value of x, not 42
       (list x y))
(list x y)

