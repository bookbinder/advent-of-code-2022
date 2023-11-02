(load "util.lisp")

(defun get-data (file)
  "Parse the data from FILE into crates and moves"
  (destructuring-bind (crates moves) (parse file #'pars)
    (let ((crates (mapcar #'(lambda (x) (coerce x 'list)) (split crates #\Newline)))
	  (moves  (mapcar #'ints (splitlines moves))))
      (setf crates
	    (mapcar #'(lambda (x)
			(remove-if-not #'(lambda (x) (char<= #\A x #\Z)) x))
		    (remove-if-not #'(lambda (x)
				       (some #'(lambda (ch) (char<= #\A ch #\Z)) x))
				   (transpose crates))))
      (list crates moves))))

(defun part1 (crates moves)
  "Move crates one at a time."
  (dolist (move moves (map 'string #'car crates))
    (dotimes (_ (first move) crates)
      (push (pop (nth (1- (second move)) crates))
	    (nth (1- (third move)) crates)))))

(defun part2 (crates moves)
  "Move crates in groups."
  (dolist (move moves (map 'string #'car crates))
    (let ((qty  (first move))
	  (src  (1- (second move)))
	  (dest (1- (third move))))
      (setf (nth dest crates)
	    (append (subseq (nth src crates) 0 qty) (nth dest crates)))
      (setf (nth src crates)
	    (subseq (nth src crates) qty)))))

(destructuring-bind (crates moves) (get-data "data/5.txt")
  ;; Answers to parts 1 and 2
  (list (part1 (copy-list crates) moves)
	(part2 (copy-list crates) moves)))
