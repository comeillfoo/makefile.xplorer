#lang br
(require brag/support)

(define-lex-abbrevs
    (target-common (:or (char-set "_-") alphabetic)))

(define-lex-abbrevs
    (target (:seq (:or target-common numeric) (:* target-common))))

(define-lex-abbrevs
    (file-name (:seq target "." target)))

(define-lex-abbrevs
    (dir-name (:or "/" (:seq target "/"))))

(define mk-lexer
    (lexer-srcloc
        [ (from/stop-before "#" "\n") (token lexeme #:skip? #t)]
        [ (:or whitespace blank) (token lexeme #:skip? #t)]
        [ "\\\n" (token lexeme #:skip? #t)]
        [ dir-name (token 'DIR (string->path lexeme))]
        [ file-name (token 'FILE (string->path lexeme))]
        [ (:or "+=" "=" "$" "(" ")"
            "ifdef" "ifndef" "endif" "else") (token lexeme lexeme)]
        [ target (token 'TARGET lexeme)]))

(provide mk-lexer)
