(load "util.lisp")

(defun md (x1 y1 x2 y2)
  "Manhattan distance."
  (+ (abs (- x1 x2)) (abs (- y1 y2))))

(defun nei (x y dist row)
  "Range of columns in ROW that can't hold a beacon, assuming no beacons
within Manhattan DIST of X Y."
  (let* ((diff  (abs (- y row)))
	 (width (- dist diff)))
    (when (<= diff dist)
      (list (- x width) (+ x width)))))

(defun combine-ranges (L &aux res)
  "Combine a sorted list of ranges L in case any overlap."
  (dolist (z L (nreverse res))
    (if (or (null res) (> (first z) (second (car res))))
	(push z res)
	(setf (second (car res)) (max (second (car res)) (second z))))))

(defun sum-ranges (L)
  "Total space occupied by all the ranges in L."
  (sum (mapcar #'(lambda (x) (+ 1 (- (second x) (first x)))) L)))

(defun beacons-in-range (beacons L row)
  "How many beacons are in one of the ranges of L at ROW?"
  (count-if #'(lambda (x)
		(and (= (second x) row)
		     (some #'(lambda (y)
			       (<= (first y) (first x) (second y)))
			   L)))
	    beacons))

(defun ranges-in-row (input row &aux res)
  "Return a list of ranges in ROW where no beacon is possible."
  (dolist (z input (combine-ranges (sort res #'< :key 'car)))
    (destructuring-bind (a b c d) z
      (let ((range (nei a b (md a b c d) row)))
	(when range (push range res))))))

(defun gaps (L mx)
  "Given a list of ranges in L, determine if there are any gaps
between 0 and MX."
  (cond ((> (first (first L)) 0) 1)
	((< (second (last1 L)) mx) (1+ (second (last1 L))))
	(t (do ((arr L (cdr arr)))
	       ((null (cdr arr)))
	     (when (> (- (first (second arr)) (second (first arr))) 1)
	       (return-from gaps (1+ (second (first arr)))))))))

(let* ((input   (parse "data/15.txt" #'lines #'ints))
       (beacons (remove-duplicates
		 (mapcar #'(lambda (x) (list (third x) (fourth x))) input)
		 :test 'equal))
       (row     (if (> (length input) 14) 2000000 10))
       (mx      (if (> (length input) 14) 4000000 20)))

  (list
   ;; part 1
   (let ((ranges (ranges-in-row input row)))
     (- (sum-ranges ranges)
	(beacons-in-range beacons ranges row)))
   
   ;; part 2 (Currently takes a few seconds. Can it be sped up?)
   (dotimes (i mx)
     (let ((res (gaps (ranges-in-row input i) mx)))
       (when res (return (+ (* res 4000000) i)))))))
