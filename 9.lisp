(load "util.lisp")

(defstruct knot r c seen)

(defun update-head (k dir)
  "Increment/decrement R or C of knot K depending on DIR."
  (case dir
    (#\R (incf (knot-c k)))
    (#\L (decf (knot-c k)))
    (#\U (decf (knot-r k)))
    (#\D (incf (knot-r k)))))

(defun update-follower (k1 k2)
  "Update knot K2 based on location of knot K1."
  (cond
    ((and (<= (abs (- (knot-r k1) (knot-r k2))) 1)
	  (<= (abs (- (knot-c k1) (knot-c k2))) 1)))  ; no update
    ((= (knot-r k1) (knot-r k2))
     (incf (knot-c k2) (signum (- (knot-c k1) (knot-c k2)))))
    ((= (knot-c k1) (knot-c k2))
     (incf (knot-r k2) (signum (- (knot-r k1) (knot-r k2)))))
    (t
     (incf (knot-r k2) (signum (- (knot-r k1) (knot-r k2))))
     (incf (knot-c k2) (signum (- (knot-c k1) (knot-c k2)))))))


(let ((input (parse "data/9.txt"
		    #'lines
		    #'(lambda (x) (list (aref x 0) (parse-integer (subseq x 2))))))
      (knots (loop for i below 10 collect (make-knot :r 0 :c 0 :seen '((0 0))))))

  ;; Answers for parts 1 and 2:
  (dolist (x input (list (length (knot-seen (nth 1 knots)))
			 (length (knot-seen (nth 9 knots)))))
    (dotimes (i (second x))
      (update-head (first knots) (first x))
      (dotimes (j (1- (length knots)))  ; update all the knots following head
	(update-follower (nth j knots) (nth (1+ j) knots))
	(when (or (= j 0) (= j 8))  ; we're interested in knots at index 1 and 9
	  (pushnew (list (knot-r (nth (1+ j) knots)) (knot-c (nth (1+ j) knots)))
		   (knot-seen (nth (1+ j) knots))
		   :test 'equal))))))
