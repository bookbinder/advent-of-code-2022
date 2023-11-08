;;;; currently takes about 8s

(load "util.lisp")

(defun matches (line)
  "Find valve names and flow rates in LINE and convert them to symbols and ints."
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
  "Return whether VALVE is in the NUM representing seen."
  (logtest (expt 2 (get valve :pos)) num))

(defun add-valve (valve num)
  "Add valve to NUM representing SEEN."
  (logior (expt 2 (get valve :pos)) num))

(defun dfs (current time total opened &aux cache)
  "Search all paths and save results in CACHE: (valves-opened pressure-released)"
  (labels ((rec (current time total opened)
	     (let ((new-total (+ total (* (get-flow opened) (- 30 time)))))
	       (push (list opened new-total) cache)
	       (dolist (x *candidates*)
		 (unless (valve-in-seen x opened)
		   (let ((time-delta (1+ (get current x))))
		     (when (< (+ time time-delta) 30)
		       (rec x
			    (+ time time-delta)
			    (+ total (* time-delta (get-flow opened)))
			    (add-valve x opened)))))))))
    (rec current time total opened))
  (remove-duplicates cache :test 'equal))

(let ((input (parse "data/16.txt" #'lines #'matches)))
  (defparameter *valves*     (mapcar #'car input))
  (defparameter *candidates* (filter #'(lambda (x)
					 (when (plusp (second x)) (car x)))
				     input))
  ;; In the property list of each symbol, list the flow-rate (:rate),
  ;; immediate neighbors (:nei), bit position lookup (:pos); and the
  ;; shortest distance to every other symbol, e.g. (get 'aa 'jj) = 2.
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
   (apply #'max (mapcar #'second (dfs 'aa 0 0 0)))
   ;; part 2 (get the max of disjoint pair sums)
   (do ((x (dfs 'aa 4 0 0) (cdr x))
	(best 0))
       ((null (cdr x)) best)
     (do ((y (cdr x) (cdr y)))
	 ((null y))
       (when (zerop (logand (first (first x)) (first (first y))))
	 (setf best (max best (+ (second (first x)) (second (first y))))))))))))
