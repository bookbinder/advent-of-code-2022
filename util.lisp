(ql:quickload 'cl-ppcre)

(proclaim '(inline last1 single append1 conc1 mklist))

(defconstant inf (truncate 9e15))

(defun last1 (lst)
  "Return last elt as an atom, not a list."
  (car (last lst)))

(defun single (lst)
  "Return whether the list contains a single item."
  (and (consp lst) (not (cdr lst))))

(defun append1 (lst obj)
  "Append an atom to a list."
  (append lst (list obj)))

(defun conc1 (obj lst)
  "Conc an atom to a list. Like 'push' but put at end."
  (nconc lst (list obj)))

(defun mklist (obj)
  "Turn an item into a list if it isn't one already."
  (if (listp obj) obj (list obj)))

(defun longer (x y)
  "Return whether the first arg is longer than the second."
  (labels ((compare (x y)
	     (and (consp x)
		  (or (null y)
		      (compare (cdr x) (cdr y))))))
    (if (and (listp x) (listp y))
	(compare x y)
	(> (length x) (length y)))))

(defun filter (fn lst &aux acc)
  "Like mapcar except that it doesn't add NIL to the final list of results."
  (dolist (x lst (nreverse acc))
    (let ((val (funcall fn x)))
      (when val (push val acc)))))

(defun group (source n)
  "Tail-recursive. Eg: (group '(1 2 3) 2) -> '((1 2) (3))"
  (if (zerop n) (error "zero length")) ; otherwise infinite loop when n is 0
  (labels ((rec (source acc)
	     (let ((rest (nthcdr n source)))
	       (if (consp rest)
		   (rec rest (cons (subseq source 0 n) acc))
		   (nreverse (cons source acc))))))
    (if source (rec source nil) nil)))

(defun transpose (L)
  "Transpose a list of lists."
  (apply #'mapcar #'list L))

(defun flatten (x)
  "Flatten a list."
  (labels ((rec (x acc)
	     (cond ((null x) acc)
		   ((atom x) (cons x acc))
		   (t (rec (car x) (rec (cdr x) acc))))))
    (rec x nil)))

(defun prune (test tree)
  "Remove elements even when nested if they pass test."
  (labels ((rec (tree acc)
	     (cond ((null tree) (nreverse acc))
		   ((consp (car tree))
		    (rec (cdr tree)
			 (cons (rec (car tree) nil) acc)))
		   (t (rec (cdr tree)
			   (if (funcall test (car tree))
			       acc
			       (cons (car tree) acc)))))))
    (rec tree nil)))

(defun find2 (fn lst)
  "Find first elt of LST that satisfies FN, then return elt
and result of FN call on that elt."
  (if (null lst)
      nil
      (let ((val (funcall fn (car lst))))
	(if val
	    (values (car lst) val)
	    (find2 fn (cdr lst))))))

(defun before (x y lst &key (test #'eql))
  "Return the sublist starting at X if we encounter an X before a (possible) Y."
  (and lst
       (let ((first (car lst)))
	 (cond ((funcall test y first) nil)
	       ((funcall test x first) lst)
	       (t (before x y (cdr lst) :test test))))))

(defun after (x y lst &key (test #'eql))
  "Return the sublist starting at X if a Y occurred before the first X. Note that
both args must occur in list, otherwise returns nil."
  (let ((rest (before y x lst :test test)))
    (and rest (member x rest :test test))))

(defun duplicate (obj lst &key (test #'eql))
  "Return sublist starting at second occurrence of obj -- or Nil if no
second occurrence."
  (member obj (cdr (member obj lst :test test))
	  :test test))

(defun split-if (fn lst)
  "Split LST into 2 sublists at first elt where FN returns true."
  (let ((acc nil))
    (do ((src lst (cdr src)))
	((or (null src) (funcall fn (car src)))
	 (values (nreverse acc) src))
      (push (car src) acc))))

(defun most (fn lst)
  "Return elt and score of (fn elt) for that elt that has highest score."
  (if (null lst)
      (values nil nil)
      (let* ((wins (car lst))
	     (max (funcall fn wins)))
	(dolist (obj (cdr lst))
	  (let ((score (funcall fn obj)))
	    (when (> score max)
	      (setq wins obj
		    max  score))))
	(values wins max))))

(defun mostn (fn lst)
  "Return a list of all elts in LST that have highest score according to FN,
along with the highest score."
  (if (null lst)
      (values nil nil)
      (let ((result (list (car lst)))
	    (max (funcall fn (car lst))))
	(dolist (obj (cdr lst))
	  (let ((score (funcall fn obj)))
	    (cond ((> score max)
		   (setq max score
			 result (list obj)))
		  ((= score max)
		   (push obj result)))))
	(values (nreverse result) max))))

(defun best (fn lst)
  "Where FN is a predicate of two args, return elt that beats all others. Like
the car of sort, but more efficient, like finding max or min with a key."
  (if (null lst)
      nil
      (let ((wins (car lst)))
	(dolist (obj (cdr lst))
	  (if (funcall fn obj wins)
	      (setq wins obj)))
	wins)))

(defun mapa-b (fn a b &optional (step 1))
  "Map a function onto each number in the range given by a and b
with optional step."
  (do ((i a (+ i step))
       (result nil))
      ((> i b) (nreverse result))
    (push (funcall fn i) result)))

(defun map0-n (fn n)
  "Map a function on integers from 0 to n."
  (mapa-b fn 0 n))

(defun map1-n (fn n)
  "Map a function on integers from 1 to n."
  (mapa-b fn 1 n))

(defun map-> (fn start test-fn succ-fn)
  "Works for any kind of sequence of objects. Stops when TEST-FN succeeds,
then returns the list. Gets successors each iteration through SCC-FN."
  (do ((i start (funcall succ-fn i))
       (result nil))
      ((funcall test-fn i) (nreverse result))
    (push (funcall fn i) result)))

(defun mappend (fn &rest lsts)
  "A non-destructive alternative to mapcan."
  (apply #'append (apply #'mapcar fn lsts)))

(defun mapcars (fn &rest lsts)
  "Run mapcar on multiple lists without concatenating them first."
  (let ((result nil))
    (dolist (lst lsts)
      (dolist (obj lst)
	(push (funcall fn obj) result)))
    (nreverse result)))

(defun rmapcar (fn &rest args)
  "Recursive mapcar on all elements of nested lists."
  (if (some #'atom args)
      (apply fn args)
      (apply #'mapcar
             (lambda (&rest args)
               (apply #'rmapcar fn args))
             args)))

(defun mkstr (&rest args)
  "Convert each arg from ARGS to a string and concatenate into one string."
  (with-output-to-string (s)
    (dolist (a args) (princ a s))))

(defun memoize (fn)
  "After creating FN, say, fib, then run (setf (fdefinition 'fib) (memoize #'fib))"
  (let ((cache (make-hash-table :test #'equal)))
    #'(lambda (&rest args)
	(multiple-value-bind (val win) (gethash args cache)
	  (if win
	      val
	      (setf (gethash args cache)
		    (apply fn args)))))))

(defun compose (&rest fns)
  "E.g. (funcall (compose #'1+ #'length) '(1 2 3)) = 4"
  (if fns
      (let ((fn1 (car (last fns)))
	    (fns (butlast fns)))
	#'(lambda (&rest args)
	    (reduce #'funcall fns
		    :from-end t
		    :initial-value (apply fn1 args))))
      #'identity))

(defun fif (_if _then &optional _else)
  "E.g. (mapcar (fif #'slave #'owner #'employer) people)
So if #'slave passes on elt, then run #'owner on it, otherwise #'employer"
  #'(lambda (x)
      (if (funcall _if x)
	  (funcall _then x)
	  (if _else (funcall _else x)))))

(defun fint (fn &rest fns)
  "Intersection of given functions... i.e., do they all pass? Works well
with find-if."
  (if (null fns)
      fn
      (let ((chain (apply #'fint fns)))
	#'(lambda (x)
	    (and (funcall fn x) (funcall chain x))))))

(defun fun (fn &rest fns)
  "Union of given functions... i.e., do any of them pass? Works well
with find-if."
  (if (null fns)
      fn
      (let ((chain (apply #'fint fns)))
	#'(lambda (x)
	    (or (funcall fn x) (funcall chain x))))))

(defun lrec (rec &optional base)
  "Create a function that operates recursively on successive cdrs of a list.
This tends to lead away from tail recursion, however. The first arg to lrec,
rec, is a function of two arguments: the current car and a function to continue
the recursion. For example:
(setq mylen (lrec #'(lambda (x f) (1+ (funcall f))) 0))
(funcall mylen '(1 2 3))"
  (labels ((self (lst)
	     (if (null lst)
		 (if (functionp base)
		     (funcall base)
		     base)
		 (funcall rec (car lst)
			  #'(lambda ()
			      (self (cdr lst)))))))
    #'self))

(defun ttrav (rec &optional (base #'identity))
  "Create a tree-traversal function. (Macros might be better for this).
E.g. (setq our-copy-tree (ttrav #'cons)) and then (funcall our-copy-tree (tree...))"
  (labels ((self (tree)
	     (if (atom tree)
		 (if (functionp base)
		     (funcall base tree)
		     base)
		 (funcall rec (self (car tree))
			  (if (cdr tree)
			      (self (cdr tree)))))))
    #'self))

(defun ints (s)
  "Return a list of all the integers in string S including negatives
unless it's \d-\d which would indicate two separate ints."
  (mapcar #'parse-integer (cl-ppcre:all-matches-as-strings "(?<!\\d)(-)*\\d+" s)))

(defmacro ppmx (form)
  "Pretty-prints the macro expansion of FORM."
  `(let* ((exp1 (macroexpand-1 ',form))
	  (exp (macroexpand exp1))
	  (*print-circle* nil))
     (cond ((equal exp exp1)
	    (format t "~&Macro expansion:")
	    (pprint exp))
	   (t (format t "~&First step of expansion:")
	      (pprint exp1)
	      (format t "~%~%Final expansion:")
	      (pprint exp)))
     (format t "~%~%")
     (values)))

(defmacro while (test &rest body)
  "Somewhat unneccessary macro when we can just use do."
  `(do () ((not ,test)) ,@body))

(defun cross-product (fn alist blist)
  "Return a list of all (fn a b) values.
E.g. (cross-product #'list '(a b) '(1 2))
-> ((A 1) (B 1) (A 2) (B 2)
E.g. (cross-product #'+ '(1 2) '(20 30))
-> (21 22 31 32)"
  (mappend #'(lambda (y)
	       (mapcar #'(lambda (x) (funcall fn x y)) alist))
	   blist))

(defun prefixp (a b)
  "Returns whether string A is a prefix of string B."
  (and (<= (length a) (length b))
       (string= a (subseq b 0 (length a)))))

(defun split (s &optional (ch #\Space) acc)
  "Split string S on character CH (default is a space)."
  (if (string= s "")
      (nreverse acc)
      (let ((i (position ch s)))
	(if i
	    (split (subseq s (1+ i)) ch (cons (subseq s 0 i) acc))
	    (nreverse (cons s acc))))))

(defun find-all (item sequence &rest keyword-args
		 &key (test #'eql) test-not &allow-other-keys)
  "Find all those elements of sequence that match item,
according to the keywords. Doesn't alter sequence. (From PAIP)"
  (if test-not
      (apply #'remove item sequence
	     :test-not (complement test-not) keyword-args)
      (apply #'remove item sequence
	     :test (complement test) keyword-args)))

(defun counter (seq)
  "Return a dictionary of counts for elements in SEQ, where
SEQ can be a string, list, or vector."
  (let ((counts (make-hash-table)))
    (typecase seq
      (string (dotimes (i (length seq) counts)
		(incf (gethash (char seq i) counts 0))))
      (list   (dolist (z seq counts)
		(incf (gethash z counts 0))))
      (vector (dotimes (i (length seq) counts)
		(incf (gethash (aref seq i) counts 0)))))))

(defun lines (str) (cl-ppcre:split "\\n" str))

(defun pars (str) (cl-ppcre:split "\\n\\n+" str))

(defun sum (L) (reduce #'+ L))

(defun parse (file &rest commands)
  "Get a file-string and then run the functions
listed in COMMANDS on it. For example,
(parse \"test.txt\" #'pars #'ints #'sum)
will split the string by paragraph, then get all the ints in that
paragraph, then sum the ints--resulting in a list where each element
is the sum of the ints in that paragraph. If no functions are given,
then just return a string-copy of the file contents.
Helpful functions: #'lines splits the text by line,
#'pars by paragraphs, #'ints gets all the integers in
integer format."
  (let ((contents (uiop:read-file-string file)))
    (dolist (fn commands contents)
      (if (stringp contents)
	  (setq contents (funcall fn contents))
	  (setq contents (funcall #'mapcar fn contents))))))

(defun 2d-list-to-2d-array (L)
  "Convert a 2d list to a 2d array."
  (make-array (list (length L) (length (first L)))
	      :initial-contents L))
