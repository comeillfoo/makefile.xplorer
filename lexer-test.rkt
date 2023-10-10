#lang br
(require "lexer.rkt" brag/support rackunit)

(define (lex port)
    (apply-port-proc mk-lexer port))

(define test-root "tests")
(define testfiles
    (map
        (curry build-path test-root)
        (filter
            (lambda (p) (string-suffix? (path->string p) "Makefile"))
            (directory-list test-root))))

(define test1 (open-input-file "tests/drivers_phy_tegra_Makefile"))
(display (lex test1))
(close-input-port test1)
