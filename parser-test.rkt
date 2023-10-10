#lang br
(require "parser.rkt" "tokenizer.rkt" brag/support)

(define (parse port)
    (apply-port-proc
        (curry apply-tokenizer make-tokenizer)
        port))

(define test1 (open-input-file "tests/drivers_phy_tegra_Makefile"))
(parse-to-datum (parse test1))
(close-input-port test1)