(load "util.lisp")

(defun expand-rocks (line)
  "Update *grid* with rock ranges in a line of input."
  (do ((arr line (cddr arr)))
      ((null (cddr arr)))
    (destructuring-bind (x1 y1 x2 y2) (subseq arr 0 4)
      (do ((x x1 (incf x (signum (- x2 x1))))
	   (y y1 (incf y (signum (- y2 y1)))))
	  ((and (= x x2) (= y y2)) (setf (aref *grid* y x) t))
	(setf (aref *grid* y x) t)))))

(defun maxes (input axis)
  "Return max value along axis."
  (let ((op (if (eq axis 'x) #'identity #'not)))
    (apply #'max (mapcan #'(lambda (x)
			     (loop for z in x and idx from 0
				   if (funcall op (zerop (mod idx 2)))
				     collect z))
			 input))))

(defun drop (rr &optional (r 0) (c 500))
  "Drop a piece of sand and let it fall until it rests or passes RR, the
lowest obstacle."
  (do ((r r (1+ r)))
      ;; return nil if it passes RR or is blocked
      ((or (>= r rr) (aref *grid* 0 500)))  
    ;; return non-nil when sand comes to rest
    (when (and (aref *grid* (1+ r) (1- c))
	       (aref *grid* (1+ r) c)
	       (aref *grid* (1+ r) (1+ c)))
      (return-from drop (setf (aref *grid* r c) t)))
    ;; change column if necessary
    (if (aref *grid* (1+ r) c)
	(if (null (aref *grid* (1+ r) (1- c)))
	    (decf c)
	    (incf c)))))


(let* ((input (parse "data/14.txt" #'lines #'ints))
       (rr (maxes input 'y))
       (cc (maxes input 'x))
       (part1 0)
       (part2 0))
  ;; set up *grid* for part 1
  (defparameter *grid* (make-array (list (+ 2 rr) (+ 2 cc)) :initial-element nil))
  (mapc #'expand-rocks input)
  (setf part1 (do ((i 0 (1+ i)))
		  ((null (drop rr)) i)))
  ;; set up *grid* for part 2
  (defparameter *grid* (make-array (list (+ 3 rr) (+ 20 cc rr)) :initial-element nil))
  (mapc #'expand-rocks input)
  (dotimes (i (+ 20 cc rr))  ; create floor
    (setf (aref *grid* (+ rr 2) i) t))
  (setf part2 (do ((i 0 (1+ i)))
		  ((null (drop inf)) i)))
  (list part1 part2))
