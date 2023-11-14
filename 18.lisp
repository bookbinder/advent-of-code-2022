(load "util.lisp")

(defun normalize-input (input)
  "Normalize coordinates so that (0 0 0) is just outside
the bottome left front, and then return normalized coordinates
and a 3d array."
  (let* ((ranges (loop for i in input
		       minimizing (first i) into x-min
		       maximizing (first i) into x-max
		       minimizing (second i) into y-min
		       maximizing (second i) into y-max
		       minimizing (third i) into z-min
		       maximizing (third i) into z-max
		       finally (return (list x-min x-max
					     y-min y-max
					     z-min z-max))))
	 (grid   (make-array (list (+ 3 (- (second ranges) (first ranges)))
				   (+ 3 (- (fourth ranges) (third ranges)))
				   (+ 3 (- (sixth ranges) (fifth ranges))))
			     :initial-element 0)))
    (dolist (x input input)
      (incf (first x) (- 1 (first ranges)))
      (incf (second x) (- 1 (third ranges)))
      (incf (third x) (- 1 (fifth ranges))))
    (dolist (x input (values input grid))
      (setf (aref grid (first x) (second x) (third x)) 1))))

(defun neighbors (pt)
  "Orthogonal neighbors in 3d grid."
  (let ((x (first pt)) (y (second pt)) (z (third pt)))
    `((,(1+ x) ,y ,z) (,(1- x) ,y ,z)
      (,x ,(1+ y) ,z) (,x ,(1- y) ,z)
      (,x ,y ,(1+ z)) (,x ,y ,(1- z)))))

(defun dfs (grid x y z)
  "DFS search of area between bounding box and shape.
Return the number of times the search makes contact with the shape."
  (let ((edges 0))
    (labels ((rec (x y z)
	       (setf (aref grid x y z) 2)
	       (dolist (nei (neighbors (list x y z)))
		 (destructuring-bind (nx ny nz) nei
		   (cond ((or (not (array-in-bounds-p grid nx ny nz))
			      (= 2 (aref grid nx ny nz)))) ; do nothing
			 ((= 1 (aref grid nx ny nz))
			  (incf edges))
			 (t (rec nx ny nz)))))))
      (rec x y z))
    edges))


(multiple-value-bind (input grid)
    (normalize-input (parse "data/18.txt" #'lines #'ints))
  ;; answers to parts 1 and 2
  (list
   (sum (mapcar #'(lambda (x)
		    (count-if #'(lambda (y)
				  (zerop (aref grid (first y) (second y) (third y))))
			      (neighbors x)))
		input))
   (dfs grid 0 0 0)))
