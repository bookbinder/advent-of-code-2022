(defun aoc-2022-3 ()
  (let ((input (mapcar 'string-to-list (string-split (f-read-text "data/3.txt")))))

    (defun score (ch)
      "Given a character, return its score."
      (+ 1 (- (downcase ch) ?a) (if (<= ch ?Z) 26 0)))

    (defun common-elt (L)
      "Find the common element among sublists of L and return its score."
      (score (car (seq-reduce 'seq-intersection L (car L)))))

    ;; Parts 1 and 2 answers:
    (list (-sum (mapcar 'common-elt
			(mapcar (lambda (x) (seq-partition x (/ (length x) 2)))
				input)))
	  (-sum (mapcar 'common-elt (seq-partition input 3))))))

(aoc-2022-3)
