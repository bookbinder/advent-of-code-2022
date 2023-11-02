(load "util.lisp")

(defun trees-right (grid r c RR CC)
  "All the trees to the right of R C in GRID."
  (loop for i from (1+ c) below CC collect (aref grid r i)))

(defun trees-left (grid r c RR CC)
  "All the trees to the left of R C in GRID."
  (loop for i downfrom (1- c) to 0 collect (aref grid r i)))

(defun trees-below (grid r c RR CC)
  "All the trees below R C in GRID."
  (loop for i from (1+ r) below RR collect (aref grid i c)))

(defun trees-above (grid r c RR CC)
  "All the trees above R C in GRID."
  (loop for i downfrom (1- r) to 0 collect (aref grid i c)))

(defun viewing-distance (cur L)
  "Viewing distance given current tree CUR and neighboring trees L."
  (let ((cand (find-if #'(lambda (x) (>= x cur)) L)))
    (if cand
	(1+ (position cand L))
	(length L))))

(defun scenic-score (grid r c RR CC)
  "Scenic score as a product of viewing distances along 4 axes."
  (reduce #'*
	  (mapcar #'(lambda (x)
		      (viewing-distance (aref grid r c) (funcall x grid r c RR CC)))
		  '(trees-above trees-below trees-left trees-right))))


(let* ((input (parse "data/8.txt" #'lines))
       (RR    (length input))
       (CC    (length (first input)))
       (grid  (make-array (list RR CC)))
       (part1 0)
       (part2 0))

  ;; Create array
  (dotimes (r RR)
    (dotimes (c CC)
      (setf (aref grid r c)
	    (digit-char-p (aref (nth r input) c)))))

  ;; Find answers for parts 1 and 2
  (dotimes (r RR (list part1 part2))
    (dotimes (c CC)
      (when (some #'(lambda (x)
		      (> (aref grid r c)
			 (apply #'max (or (funcall x grid r c RR CC) (list -1)))))
		  '(trees-above trees-below trees-left trees-right))
	(incf part1))
      (setf part2 (max part2 (scenic-score grid r c RR CC))))))
