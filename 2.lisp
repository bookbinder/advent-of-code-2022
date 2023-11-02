(load "util.lisp")

(defun letter->num (L)
  "Convert ABC and XYZ to 123 in the first and second of L."
  (list (1+ (- (char-int (coerce (first L) 'character)) (char-int #\A)))
	(1+ (- (char-int (coerce (second L) 'character)) (char-int #\X)))))

(defun points (L)
  "Return the number of points given the hand played L."
  (cond ((= (first L) (second L))
	 (+ 3 (second L)))
	((= (mod (first L) 3) (1- (second L)))
	 (+ 6 (second L)))
	(t
	 (second L))))

(defun choose (L)
  "Return the hand that will achieve the results in the second of L."
  (list (first L)
	(case (second L)
	  (1 (1+ (mod (1+ (first L)) 3)))
	  (2 (first L))
	  (3 (1+ (mod (first L) 3))))))

(let ((input (parse "data/2.txt" #'lines #'split #'letter->num)))
  ;; Answers for parts 1 and 2:
  (list (sum (mapcar #'points input))
	(sum (mapcar (compose #'points #'choose) input))))
