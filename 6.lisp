(defun som-marker (str som)
  (dotimes (i (1+ (- (length str) som)) nil)
    (when (= som (length (remove-duplicates (subseq str i (+ i som)))))
      (return-from som-marker (+ i som)))))

(let ((input (parse "data/6.txt")))
  ;; Answers to parts 1 and 2:
  (list (som-marker input 4)
	(som-marker input 14)))
