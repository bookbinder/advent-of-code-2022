(let ((input (mapcar 'ints (string-split (f-read-text "data/4.txt")))))

  (defun ints (s)
    "Return a list of all the ints in string s."
    (with-temp-buffer
      (let (res)
	(insert s)
	(goto-char (point-min))
	(while (search-forward-regexp "[0-9]+" nil t)
	  (push (string-to-number (match-string 0)) res))
	(nreverse res))))
  
  (defun total-overlap (x)
    "Check if range of first two elements and range of second two elements
totally overlap."
    (cl-multiple-value-bind (a b c d) x
      (if (or (<= a c d b)
	      (<= c a b d))
	  1
	0)))

  (defun partial-overlap (x)
    "Check if range of first two elements and range of second two elements
partially overlap."
    (cl-multiple-value-bind (a b c d) x
      (if (or (<= a c b)
	      (<= c a d))
	  1
	0)))

  ;; Answers to parts 1 and 2:
  (list (-sum (mapcar 'total-overlap input))
	(-sum (mapcar 'partial-overlap input))))
