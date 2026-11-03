"""Offline syntax coloring for the deck's short, mixed-language examples."""
from html import escape
from keyword import kwlist
import re


KEYWORDS = set(kwlist) | {'true', 'false', 'null', 'export'}
TOKENS = re.compile(
    r"""(?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')"""
    r'|(?P<comment>\#.*)'
    r'|(?P<number>\b\d+(?:\.\d+)?\b)'
    r'|(?P<word>@?[A-Za-z_]\w*)'
)
COLORS = {
    'string': '#A9DEA5',
    'comment': '#9AAFC5',
    'number': '#FFC98B',
    'keyword': '#D5B8FF',
    'name': '#91D8F7',
}


def code_text(line):
    def color(match):
        token = match[0]
        kind = match.lastgroup
        following = line[match.end():].lstrip()
        if kind == 'word':
            if token in KEYWORDS:
                kind = 'keyword'
            elif token.startswith('@') or following.startswith(('(', ':')):
                kind = 'name'
        elif kind == 'string' and following.startswith(':'):
            kind = 'name'
        escaped = escape(token)
        return f'<tspan fill="{COLORS[kind]}">{escaped}</tspan>' if kind in COLORS else escaped

    parts = []
    end = 0
    for match in TOKENS.finditer(line):
        parts.extend((escape(line[end:match.start()]), color(match)))
        end = match.end()
    parts.append(escape(line[end:]))
    return ''.join(parts)


def code_line(line, x, y, size):
    return (
        f'<text class="code-line" xml:space="preserve" x="{x}" y="{y}" '
        f'font-size="{size}" fill="#EFF4FF">{code_text(line.expandtabs(4))}</text>'
    )
