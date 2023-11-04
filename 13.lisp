(load "util.lisp")

(defun my-eval (L)
  "Convert a list of two strings into two proper sublists using eval."
  (mapcar #'(lambda (x)
	      (eval
	       (read-from-string
		(format nil "~A~A"
			"'"
			(substitute #\( #\[
				    (substitute #\) #\]
						(substitute #\Space #\, x)))))))
	  L))

(defun compare (a b)
  "Compare A and B for sorting."
  (labels ((rec (a b)
	     (cond ((or (null a) (null b))
		    (signum (- (length a) (length b))))
		   ((and (numberp (car a)) (numberp (car b)))
		    (if (= (car a) (car b))
			(rec (cdr a) (cdr b))
			(signum (- (car a) (car b)))))
		   (t
		    (let ((val (rec (mklist (car a)) (mklist (car b)))))
		      (if (zerop val)
			  (rec (cdr a) (cdr b))
			  (signum val)))))))
    (< (rec a b) 0)))

(let* ((input (parse "data/13.txt" #'pars #'lines #'my-eval))
       (part1 0))
  (do ((i 1 (1+ i))
       (arr input (cdr arr)))
      ((null arr))
    (when (compare (first (car arr)) (second (car arr)))
      (incf part1 i)))
  (let ((part2 (sort (apply #'append '(((2))) '(((6))) input) #'compare)))
    ;; Return answers for parts 1 and 2:
    (list part1
	  (* (1+ (position '((6)) part2 :test 'equal))
	     (1+ (position '((2)) part2 :test 'equal))))))
