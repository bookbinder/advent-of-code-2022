(let ((input  (string-split (string-trim (f-read-text "data/2.txt")) "\n"))
      (played '((?X . 1) (?Y . 2) (?Z . 3)))
      (lose   '("A Z" "B X" "C Y"))
      (win    '("A Y" "B Z" "C X"))
      (draw   '("A X" "B Y" "C Z"))
      (p1     0)
      (p2     0))

  (defun round-score (a b)
    (let ((val  (alist-get b played))
	  (line (concat (char-to-string a) " " (char-to-string b))))
      (cond ((member line lose) val)
	    ((member line win) (+ 6 val))
	    ((member line draw) (+ 3 val)))))

  (defun choose (a b)
    (let ((res (if (= b ?X)
		   lose
		 (if (= b ?Y)
		     draw
		   win))))
      (elt (seq-find (lambda (x) (= (elt x 0) a)) res) 2)))

  (dolist (line input)
    (setq p1 (+ p1 (round-score (elt line 0)
				(elt line 2))))
    (setq p2 (+ p2 (round-score (elt line 0)
				(choose (elt line 0) (elt line 2))))))
  (list p1 p2))
