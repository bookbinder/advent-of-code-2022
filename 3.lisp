(load "util.lisp")

(defun common-letter (L)
  "A letter that both halves of list L share in common."
  (let ((N (/ (length L) 2)))
    (remove-duplicates (intersection (subseq L 0 N) (subseq L N)))))

(defun common-letter2 (L)
  "A letter shared by all sublists of L."
  (remove-duplicates (reduce #'intersection L)))

(defun priority (ch)
  "Encode letter a=1, A=27, etc."
  (cond ((char<= #\a ch #\z) (1+ (- (char-int ch) (char-int #\a))))
	((char<= #\A ch #\Z) (+ 27 (- (char-int ch) (char-int #\A))))))

(let ((input (parse "data/3.txt" #'lines #'(lambda (x) (coerce x 'list)))))
  ;; Answers to parts 1 and 2:
  (list
   (sum (mapcar #'priority (mapcan #'common-letter input)))
   (sum (mapcar #'priority (mapcan #'common-letter2 (group input 3))))))
