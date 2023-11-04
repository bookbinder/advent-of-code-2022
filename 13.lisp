(load "util.lisp")

(defun my-eval (s)
  "Parse string S into a quoted list data structure."
  (eval (read-from-string (format nil "~A~A" "'" s))))

(defun repl (s)
  "Make string S look like a Lisp list data structure."
  (substitute #\( #\[
	      (substitute #\) #\]
			  (substitute #\Space #\,
				      s))))

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

(let* ((input (mapcar #'lines (pars (repl (parse "data/13.txt")))))
       (input (mapcar #'(lambda (x) (mapcar #'my-eval x)) input))
       (part1 0))
  (do ((i 1 (1+ i))
       (arr input (cdr arr)))
      ((null arr))
    (when (compare (first (car arr)) (second (car arr)))
      (incf part1 i)))
  (let ((p2-input (sort (apply #'append '(((2))) '(((6))) input) #'compare)))
    ;; Return answers for parts 1 and 2:
    (list part1
	  (* (1+ (position '((6)) p2-input :test 'equalp))
	     (1+ (position '((2)) p2-input :test 'equalp))))))
