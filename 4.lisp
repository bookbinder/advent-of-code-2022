(defun total-overlap (L)
  "First two numbers of list L indicate first range, second 2 indicate second range.
Is there total overlap?"
  (or (<= (first L) (third L) (fourth L) (second L))
      (<= (third L) (first L) (second L) (fourth L))))

(defun partial-overlap (L)
  "First two numbers of list L indicate first range, second 2 indicate second range.
Is there partial overlap?"
  (or (<= (third L) (first L) (fourth L))
      (<= (first L) (third L) (second L))))

(let ((input (parse "data/4.txt" #'lines #'ints)))
  ;; Answers to parts 1 and 2:
  (list (count-if #'total-overlap input)
	(count-if #'partial-overlap input)))