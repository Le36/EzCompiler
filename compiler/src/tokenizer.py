import re
from dataclasses import dataclass


@dataclass
class SourceLocation:
    file: str
    line: int
    column: int

    def __eq__(self, other):
        return isinstance(other, SourceLocation) or other is L


L = SourceLocation(file='any', line=-1, column=-1)


@dataclass
class Token:
    text: str
    type: str
    location: SourceLocation

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.type, self.text) == (other.type, other.text) and (
                    self.location == other.location or self.location is L or other.location is L)
        return False


def tokenize(source_code: str, file_name: str = 'editor') -> list[Token]:
    token_patterns = {
        'COMMENT': r'//.*|/\*[\s\S]*?\*/|#.*',
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z_0-9]*',
        'INTEGER': r'\d+',
        'OPERATOR': r'==|!=|<=|>=|\+|-|\*|/|=|<|>',
        'PUNCTUATION': r'[(),;{}]',
        'WHITESPACE': r'\s+',
    }

    combined_pattern = '|'.join(f'(?P<{token_type}>{pattern})' for token_type, pattern in token_patterns.items())

    regex = re.compile(combined_pattern)

    line = 1
    column = 1

    tokens = []
    for match in regex.finditer(source_code):
        token_type = match.lastgroup
        token = match.group(token_type)
        start, end = match.span(token_type)

        line_increment = token.count('\n')
        if line_increment > 0:
            line += line_increment
            column = end - source_code.rfind('\n', 0, end)
        else:
            if token_type not in ['WHITESPACE', 'COMMENT']:
                location = SourceLocation(file_name, line, column)
                tokens.append(Token(text=token, type=token_type, location=location))
            column += end - start

    return tokens
