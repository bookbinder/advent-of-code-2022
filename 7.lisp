(load "util.lisp")

(let ((input  (parse "data/7.txt" #'lines #'split))
      (dirs   (make-hash-table :test 'equalp))
      (part1  0)
      (curdir nil))

  (defun backfill (L amt)
    "Given the reversed path in L, fill every subdirectory with AMT."
    (dolist (subl (maplist #'reverse L))
      (incf (gethash (format nil "~{~A~^/~}" subl) dirs 0) amt)))

  ;; build hashtable of directory sizes
  (dolist (z input curdir)
    (cond
      ((string= (second z) "cd")
       (if (string= ".." (last1 z))
	   (pop curdir)
	   (push (last1 z) curdir)))
      ((char<= #\0 (aref (car z) 0) #\9)
       (backfill curdir (parse-integer (car z))))))

  ;; get answer for part 1
  (maphash #'(lambda (k v)
	       (when (<= v 100000) (incf part1 v)))
	   dirs)

  ;; get answer for part 2
  (let* ((free-space (- 70000000 (gethash "/" dirs)))
	 (to-free    (- 30000000 free-space))
	 (part2      (gethash "/" dirs)))
    (dolist (x (loop for k being the hash-keys of dirs collect k))
      (let ((val (gethash x dirs)))
	(when (and (< val part2)
		   (>= val to-free))
	  (setq part2 val))))

    ;; return answers for parts 1 and 2:
    (list part1 part2)))
