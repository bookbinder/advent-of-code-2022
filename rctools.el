(defun ints (s)
  "Return a list of all the ints in string s."
  (with-temp-buffer
    (let (res)
      (insert s)
      (goto-char (point-min))
      (while (search-forward-regexp "[0-9]+" nil t)
	(push (string-to-number (match-string 0)) res))
      (nreverse res))))

(defun find-all (rgx str)
  "Return a list of all matches of rgx in string s."
  (with-temp-buffer
    (let (res)
      (insert str)
      (goto-char (point-min))
      (while (search-forward-regexp rgx nil t)
	(push (match-string 0) res))
      (nreverse res))))

(defun zip (list-of-lists)
  (apply #'seq-mapn #'list list-of-lists))

(provide 'rctools)
