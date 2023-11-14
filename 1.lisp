(load "util.lisp")

(let ((input (sort (parse "data/1.txt" #'pars #'ints #'sum) #'>)))
  (list (first input)
	(sum (subseq input 0 3))))
