;;;; currently takes about 20s

(load "util.lisp")

(defun matches (line)
  "Find valve names and flow rates and convert them to symbols and ints."
  (destructuring-bind (a b . c)
      (cl-ppcre:all-matches-as-strings "([A-Z]{2}|\\d+)" line)
    (append (list (intern a) (parse-integer b)) (mapcar #'intern c))))

(defun get-flow (opened)
  "Get total flow of all OPENED valves in a given instant."
  (let ((total 0))
    (dotimes (i (integer-length opened) total)
      (when (logbitp i opened)
	(incf total (get (nth i *valves*) :rate))))))

(defun valve-in-seen (valve num)
  "Return whether valve is in the num representing seen."
  (logtest (expt 2 (get valve :pos)) num))

(defun add-valve (valve num)
  "Add valve to num representing seen."
  (logior (expt 2 (get valve :pos)) num))

(let ((cache (make-hash-table :test 'equal))
      cache2)
  (defun dfs (current time total opened)
    "Search all paths and return max."
    (when-bind (val (gethash (list current time total opened) cache))
      (return-from dfs val))
    (let ((mx (+ total (* (get-flow opened) (- 30 time)))))
      (push (list opened mx) cache2)
      (dolist (x *candidates*)
	(unless (valve-in-seen x opened)
	  (let (value time-delta)
	    (setf time-delta (1+ (get current x)))
	    (when (< (+ time time-delta) 30)
	      (setf value (dfs x
			       (+ time time-delta)
			       (+ total (* time-delta (get-flow opened)))
			       (add-valve x opened)))
	      (when (> value mx)
		(setf mx value))))))
      (setf (gethash (list current time total opened) cache) mx)))
  (defun clear-cache ()
    (setf cache (make-hash-table :test 'equal))
    (setf cache2 nil))
  (defun get-cache () cache)
  (defun get-cache2 () cache2))

(let* ((input (parse "data/16.txt" #'lines #'matches)))
  (defparameter *valves*     (mapcar #'car input))
  (defparameter *candidates* (filter #'(lambda (x)
					 (when (plusp (second x)) (car x)))
				     input))
  ;; In the property list of each symbol, list the flow-rate (:rate),
  ;; immediate neighbors (:nei), bit position lookup (:pos); and the
  ;; shortest distance to every other symbol (get 'aa 'jj) = 2.
  (do ((arr input (cdr arr))
       (i 0 (1+ i)))
      ((null arr))
    (let ((x (first arr)))
      (setf (get (first x) :pos)  i)
      (setf (get (first x) :rate) (second x))
      (setf (get (first x) :nei)  (subseq x 2))))

  ;; Floyd-Marshall shortest distances
  (dolist (x input)
    (dolist (y input)
      (if (member (car y) (get (car x) :nei))
	  (setf (get (car x) (car y)) 1)
	  (setf (get (car x) (car y)) inf))))
  (dolist (k *valves*)
    (dolist (i *valves*)
      (dolist (j *valves*)
	(setf (get i j)
	      (min (get i j) (+ (get i k) (get k j)))))))

  (list
   ;; part 1
   (progn (clear-cache)
	  (dfs 'aa 0 0 0)
	  (apply #'max (mapcar #'second (get-cache2))))
   ;; part 2
   (progn
     (let* ((best 0) res)
       (clear-cache)
       (dfs 'aa 4 0 0)
       (setf res (get-cache2))
       (dolist (x res best)
	 (dolist (y res)
	   (when (zerop (logand (car x) (car y)))
	     (setf best (max best (+ (second x) (second y)))))))))))
