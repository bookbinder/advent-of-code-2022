(load "util.lisp")

(defun shift (grid shape dir)
  "Shift piece one unit in direction DIR if possible. Return new coords or nil."
  (let* ((dr (if (zerop dir) 1 0))
	 (dc dir)
	 (new-shape (mapcar #'(lambda (x)
				(list (+ dr (first x)) (+ dc (second x))))
			    shape)))
    (unless (or (some #'(lambda (x)
		      (or (not (<= 0 (second x) 6))
			  (>= (first x) (first (array-dimensions grid)))))
		  new-shape)
	    (some #'(lambda (x)
		      (= 1 (aref grid (first x) (second x))))
		  new-shape))
      new-shape)))

(defun drop (grid i j mx cycle &optional (sig nil sig-p))
  "Drop a shape until it rests. I is rock count, J is wind count, MX is
max height so far, and CYCLE is whether a cycle has been found. SIG
checks for a signature for repetition. Derive shape from I and position
of shape from MX, and return new grid, J, MX, and cycle."
  (let* ((is    (mod i *ns*))
	 (r     (- mx (+ 4 (- (nth is *shape-heights*) 1))))
	 (shape (mapcar #'(lambda (x)
			    (list (+ r (first x)) (+ 2 (second x))))
			(nth is *shapes*))))
    (while t
      (when-bind (val (shift grid shape (aref *wind* (mod j *nw*))))
	(setf shape val))
      (incf j)
      (let ((newshape (shift grid shape 0))) 
	(if newshape
	    (setf shape newshape)
	    (progn
	      (dolist (z shape)
		(setf (aref grid (first z) (second z)) 1))
	      (let ((new-mx (min mx (apply #'min (mapcar #'car shape)))))
		(when (and sig-p (null cycle))
		  (when-bind (val (funcall sig grid mx i j))
		    (setf cycle val)))
		(return-from drop (list grid j new-mx cycle)))))))))

(defun signature (&optional (n 20))
  "Return a function that converts last N rows of grid into a number.
Store results in MEMO with
key= (current-shape-index current-wind-index last-n-rows-number), and
value= (current-rock-num mx). When the inner function finds a
repetition, return values at the 2 indices, otherwise nil."
  (let ((memo (make-hash-table :test 'equal)))
    #'(lambda (grid mx i j)
	(let* ((rows (parse-integer
		      (format nil "~{~A~}"
			      (loop for x from (max (- mx n) 0) below mx
				    append (loop for y below 7
						 collect (aref grid x y))))
		      :radix 2))
	       (val (gethash (list (mod i *ns*) (mod j *nw*) rows) memo)))
	  (if val
	      (list val (list i mx))
	      (progn
		(setf (gethash (list (mod i *ns*) (mod j *nw*) rows) memo)
		      (list i mx))
		nil))))))

;;;; Global constants
(defparameter *input*
  (map 'list #'(lambda (x) (case x (#\> 1) (#\< -1)))
       (parse "data/17.txt")))
(defparameter *wind* (make-array (length *input*) :initial-contents *input*))
(defparameter *nw* (length *wind*))
(defparameter *shapes* '(((0 0) (0 1) (0 2) (0 3))
			 ((0 1) (1 0) (1 1) (1 2) (2 1))
			 ((0 2) (1 2) (2 0) (2 1) (2 2))
			 ((0 0) (1 0) (2 0) (3 0))
			 ((0 0) (0 1) (1 0) (1 1))))
(defparameter *ns* (length *shapes*))
(defparameter *shape-heights*
  (mapcar #'(lambda (x) (1+ (apply #'max (mapcar #'first x)))) *shapes*))
(defparameter *max-rocks* 1000000000000)


(let* ((n     2022)  ; max number of rocks to drop
       (grid  (make-array (list (+ 10 (* n 4)) 7) :initial-element 0))
       (mx    (first (array-dimensions grid)))
       (j     0)     ; wind count
       (cycle nil)   ; have we encountered a repition of the signature yet?
       (part1 nil)
       (sig   (signature))
       rock-heights)
  (dotimes (i n (list part1 "cycle not found"))
    (let ((val (drop grid i j mx cycle sig)))
      (setf grid  (first val)
	    j     (second val)
	    mx    (third val)
	    cycle (fourth val))
      (push mx rock-heights))
    (when (= i 2021)
      (setf part1 (- (first (array-dimensions grid)) mx)))
    (when (and part1 cycle)
      (destructuring-bind ((rockstart mxstart) (rockend mxend)) cycle
	  (let* ((htstart (- (first (array-dimensions grid)) mxstart))
		 (htend (- (first (array-dimensions grid)) mxend))
		 (cycle-height (- htend htstart))
		 (cycle-length (- rockend rockstart)))
	    (multiple-value-bind (num-cycles remainder)
		(floor (- *max-rocks* rockstart) cycle-length)
	      (return (list part1
			    (+ (* num-cycles cycle-height)
			       (- (first (array-dimensions grid))
				  (nth (1- (+ remainder rockstart))
				       (reverse rock-heights))))))))))))
