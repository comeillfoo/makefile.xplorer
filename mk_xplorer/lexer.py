#!/usr/bin/env python3
import ply.lex as lex
from ply.lex import TOKEN


from typing import Generator


class MakefileLexer:
    reserved = {
        'include': 'INCLUDE',
        'define': 'DEFINE',
        'endef': 'ENDEF',
    }

    literals = ':=+?!$()'

    tokens = (
        'WORD',
        'NEWLINES',
        'ESCSEQ',
        'RECIPEPREFIX', # may be redefined at runtime by .RECIPEPREFIX
        'SPACES',
    ) + tuple(reserved.values())

    t_ESCSEQ = r'\\(u[A-Fa-f0-9]{4}|U[A-Fa-f0-9]{8}|.|\n)'

    t_ignore = '\r\f\v'

    def t_WORD(self, t):
        r'\w+'
        t.type = self.reserved.get(t.value, 'WORD')
        return t


    def t_COMMENT(self, t):
        r'\#.*'
        pass
        # No return value. Token discarded


    def t_NEWLINES(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t


    def t_SPACES(self, t):
        r'[ ]+'
        t.value = len(t.value)
        return t


    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    def build(self, recipeprefix: str = r'\t', **kwargs):
        @TOKEN(recipeprefix)
        def t_RECIPEPREFIX(t):
            t.value = len(t.value)
            return t
        self.t_RECIPEPREFIX = t_RECIPEPREFIX

        self.lexer = lex.lex(module=self, **kwargs)


    def tokenize(self, stream: str) -> Generator[lex.LexToken, None, None]:
        self.lexer.input(stream)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield tok
