#!/usr/bin/env python3
import re
from enum import IntEnum, auto


class ParserContext(IntEnum):
    BASE_CTX = 0
    RULE_CTX = auto()

class Filenames:
    def __init__(self, filenames: str):
        self.filenames = filenames.strip().split(' ')

    def __str__(self) -> str:
        return ' '.join(self.filenames)


FILENAME_STX = '[a-zA-Z0-9](?:[a-zA-Z0-9 ._-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+'

class Rule:
    RECIPE_PREFIX='\t'
    TARGETS_PREREQS_STX = f'({FILENAME_STX} )*({FILENAME_STX})'
    RECIPE_STX = re.compile(f'(?P<targets>{TARGETS_PREREQS_STX})(?P<grouped>\&)?: *(?P<prereqs>{TARGETS_PREREQS_STX}) *(?P<recipe>;.*)?')

    def __init__(self, targets: Filenames, prerequisittes: Filenames,
                 is_default: bool = False, is_grouped: bool = False,
                 recipe: list[str] = []):
        self.is_default = is_default
        self.targets = targets
        self.is_grouped_or_independent = is_grouped # targets grouped or independent
        self.prerequisites = prerequisittes
        self.recipe: list[str] = recipe


    def __str__(self) -> str:
        return str(self.targets) \
            + ' ' + ('&:' if self.is_grouped_or_independent else ':') \
            + ' ' + str(self.prerequisites) + '\n' \
            + '\n'.join(map(lambda s: Rule.RECIPE_PREFIX + s, self.recipe))


class MakefileParser():

    def __init__(self):
        self.parser_ctx = ParserContext.BASE_CTX
        self.rules: list[Rule] = []


    def _parse_base(self, mk_line: str):
        match_rule = Rule.RECIPE_STX.match(mk_line)
        if match_rule: # has match
            recipe = match_rule.group('recipe')
            [] if not recipe else [ recipe ]
            self.rules.append(Rule(
                Filenames(match_rule.group('targets').strip()),
                Filenames(match_rule.group('prereqs').strip()),
                not self.rules, match_rule.group('grouped') is not None,
                [] if not recipe else [ recipe ]))

            # switch to parse recipe in rule context
            self.parser_ctx = ParserContext.RULE_CTX

        # TODO: parse variables
        # TODO: parse directives


    def _parse_rule(self, mk_line: str):
        if not mk_line.startswith(Rule.RECIPE_PREFIX):
            return self._parse_base(mk_line)
        self.rules[-1].recipe \
            .append(mk_line.lstrip(Rule.RECIPE_PREFIX).strip())


    _line_handlers = {
        ParserContext.BASE_CTX: _parse_base,
        ParserContext.RULE_CTX: _parse_rule,
    }


    def parse_line(self, mk_line: str):
        try:
            return self._line_handlers[self.parser_ctx](self, mk_line)
        except IndexError:
            raise ValueError


    def parse(self, makefile: str):
        for line in makefile.split('\n'):
            self.parse_line(line)
