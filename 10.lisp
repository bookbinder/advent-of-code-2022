(load "util.lisp")

(let ((input (parse "data/10.txt" #'lines #'split))
      (total 0)
      (x 1)
      vals
      display)
  (setf vals (dolist (z input (nreverse vals))
	       (push x vals)
	       (when (= 2 (length z))
		 (push x vals)
		 (incf x (parse-integer (second z))))))

  ;; Answers to parts 1 and 2:
  (do ((i 1 (1+ i))
       (L vals (cdr L)))
      ((null L) (list total
		      (mapcar #'(lambda (x)
				  (format nil "~&~{~A~}" x))
			      (group (nreverse display) 40))))
    (when (= 20 (mod i 40))
      (incf total (* i (car L))))
    (if (<= (abs (- (mod (1- i) 40) (car L))) 1)
	(push "#" display)
	(push " " display))))
