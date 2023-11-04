(load "util.lisp")

(defun trees-surrounding (grid r c RR CC)
  "Neighboring trees below, above, left, and right of R C."
  (list
   (loop for i downfrom (1- r) to 0 collect (aref grid i c))
   (loop for i from (1+ r) below RR collect (aref grid i c))
   (loop for i downfrom (1- c) to 0 collect (aref grid r i))
   (loop for i from (1+ c) below CC collect (aref grid r i))))

(defun viewing-distance (cur L)
  "Viewing distance given current tree CUR and neighboring trees in one direction."
  (let ((cand (find-if #'(lambda (x) (>= x cur)) L)))
    (if cand
	(1+ (position cand L))
	(length L))))

(defun scenic-score (cur L)
  "Scenic score as a product of viewing distances along 4 directions."
  (reduce #'* (mapcar #'(lambda (x) (viewing-distance cur x))
		      L)))


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
      (let ((neigh (trees-surrounding grid r c RR CC)))
	(when (some #'(lambda (x)
			(> (aref grid r c)
			   (apply #'max (or x (list -1)))))
		    neigh)
	  (incf part1))
	(setf part2 (max part2
			 (scenic-score (aref grid r c) neigh)))))))
