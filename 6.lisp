(require "asdf")
(asdf:load-system :uiop)
(asdf:oos 'asdf:test-op :cl-ppcre)

(defun get-file (filename)
  (with-open-file (stream filename)
    (loop for line = (read-line stream nil)
          while line
          collect line)
  )
)

(defun calc (tm d)
  (let ((cnt 0))
    (loop for x from 0 to tm
          do (if (> (* (- tm x) x) d) (incf cnt))
    )
    (return-from calc cnt)
  )
)

(defun concat-strings (list)
  (apply #'concatenate 'string list)
)

(setq f (get-file "inputs/6"))
(setq times (cdr (cl-ppcre:split "\\s+" (first f))))
(setq distances (cdr (cl-ppcre:split "\\s+" (second f))))
(setq part1 1)

(loop for x in times
      for y in distances
      do (setq part1 
           (* part1 
             (calc (parse-integer x) 
                   (parse-integer y))
           )
         )
)
(print part1)

(setq part2 (calc (parse-integer (concat-strings times)) (parse-integer (concat-strings distances))))
(print part2)
