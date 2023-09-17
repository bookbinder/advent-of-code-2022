<<<<<<< HEAD
(let ((input (string-split (f-read-text "data/1.txt") "\n\n")))
  (setq input (mapcar '-sum
		      (-tree-map 'string-to-number (mapcar 'string-split input))))

  ;; Parts 1 and 2 answers:
  (list (seq-max input)
	(-sum (seq-subseq (sort input '>) 0 3))))
=======
(defun aoc-2022-1 ()
  (let ((input (string-split (f-read-text "data/1.txt") "\n\n")))
    (setq input (mapcar '-sum
			(-tree-map 'string-to-number (mapcar 'string-split input))))

    ;; Parts 1 and 2 answers:
    (list (seq-max input)
	  (-sum (seq-subseq (sort input '>) 0 3)))))

(aoc-2022-1)
>>>>>>> 766d637 (added elisp 1 and 3)
