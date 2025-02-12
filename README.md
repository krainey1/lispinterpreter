# A (small) Lisp Interpreter (in Python)

This is an adaption of Peter Norvigs lisp interpreter lis.py as outlined in his tutorial (How to Write a (Lisp) Interpreter (in Python)) - which can be found at https://norvig.com/lispy.html. This project implements the following lisp constructs:
* Variable Definition (define r 10)
* Variable Reference r
* Constant Literals
* Quotations '(the cat in the hat) will return (the cat in the hat)
* Assignment (set! r 5)
* Function Definitions/Calls
* Arithmetic operators, car, cdr, cons, sqrt, and exp
* Conditionals > < == <= >= != not or and

and can be used by cloning the repo and running the .py file. 

(this was a educational project for CSE 324 at NMT, and as such also includes the report detailing how the constructs were implmented) 
