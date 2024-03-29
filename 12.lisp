(load "util.lisp")

(defun transform-list (L)
  "Return 3 values: a 2d array with numbers substituted for letters; start coords;
end coords."
  (do ((r 0 (1+ r))
       (arr L (cdr arr))
       res start end)
      ((null arr) (values (2d-list-to-2d-array (nreverse res)) start end))
    (let ((S (position #\S (car arr)))
	  (E (position #\E (car arr))))
      (when S (setf start (list r S)))
      (when E (setf end (list r E)))
      (push (map 'list #'(lambda (x)
			   (- (char-code x) (char-code #\a)))
		 (substitute #\a #\S (substitute #\z #\E (car arr))))
	    res))))

(defun neighbors (grid pt &aux res)
  "Orthogonal cells to PT whose values are no more than one higher than
the value at PT."
  (dolist (x '((0 1) (1 0) (0 -1) (-1 0)) res)
    (let ((cur (mapcar #'+ pt x)))
      (when (and (array-in-bounds-p grid (first cur) (second cur))
		 (<= (aref grid (first cur) (second cur))
		     (1+ (aref grid (first pt) (second pt)))))
	(push cur res)))))

(defun bfs (grid start end)
  "Shortest distance from START to END points in GRID."
  (let ((seen (make-array (array-dimensions grid) :initial-element nil)))
    (setf (aref seen (first start) (second start)) t)
    (do ((level 0 (1+ level))
	 (q (list start))
	 tmp)
	((null q) inf)
      (dotimes (_ (length q))
	(let ((cur (pop q)))
	  (when (equalp cur end) (return-from bfs level))
	  (dolist (z (neighbors grid cur))
	    (unless (aref seen (first z) (second z))
	      (setf (aref seen (first z) (second z)) t)
	      (push z tmp)))))
      (setf q tmp)
      (setf tmp nil))))

(defun a-coords (grid &aux res)
  "All `a` coordinates (with a value of 0)."
  (destructuring-bind (rr cc) (array-dimensions grid)
    (dotimes (r rr res)
      (dotimes (c cc)
	(when (zerop (aref grid r c)) (push (list r c) res))))))

(multiple-value-bind (grid start end) (transform-list (parse "data/12.txt" #'lines))
  (list (bfs grid start end)
	(apply #'min (mapcar #'(lambda (x) (bfs grid x end))
			     (a-coords grid)))))
