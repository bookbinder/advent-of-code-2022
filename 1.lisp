(load "~/scripts/lisp/util.lisp")

(let ((input (sort (parse "~/scripts/aoc/2022/data/1.txt" #'pars #'ints #'sum) #'>)))
  (list (first input)
	(sum (subseq input 0 3))))
