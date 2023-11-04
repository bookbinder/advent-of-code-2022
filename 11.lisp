(load "util.lisp")

(defstruct monkey items op throw cnt)

(defun parse-monkey (m)
  (make-monkey :items (ints (second m))
	       :op #'(lambda (x)
		       (funcall (if (char= (aref (third m) 23) #\+) #'+ #'*)
			x
			(if (char= (aref (third m) 25) #\o)
			    x
			    (parse-integer (subseq (third m) 25)))))
	       :throw (mapcan #'ints (subseq m 3))
	       :cnt 0))

(defun monkey-business (L)
  "The product of number of throws of two most active monkeys."
  (reduce #'*
	  (subseq (sort (mapcar #'(lambda (x) (monkey-cnt x)) L) #'>) 0 2)))

(defun simulate (monkeys n div)
  "Run simulation N times with divisor DIV"
  (let ((prod (reduce #'* (mapcar #'(lambda (x) (first (monkey-throw x))) monkeys))))
    (dotimes (i n (monkey-business monkeys))  ; number of rounds
      (dolist (m monkeys)  ; for each monkey
	(dolist (it (monkey-items m))  ; for each item monkey is carrying
	  (let ((new-level (mod
			    (floor (funcall (monkey-op m) (pop (monkey-items m))) div)
			    prod)))
	    (incf (monkey-cnt m))
	    (if (= 0 (mod new-level (first (monkey-throw m))))
		(push new-level
		      (monkey-items (nth (second (monkey-throw m)) monkeys)))
		(push new-level
		      (monkey-items (nth (third (monkey-throw m)) monkeys))))))))))

;; Answers for parts 1 and 2:
(let ((input (parse "data/11.txt" #'pars #'lines)))
  (list (simulate (mapcar #'parse-monkey input) 20 3)
	(simulate (mapcar #'parse-monkey input) 10000 1)))
