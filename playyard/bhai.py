"""A tiny interpreter for a few words of bhai-lang.

bhai-lang (github.com/DulLabs/bhai-lang) is a toy language whose keywords are
Hindi. This covers just enough of it to run the programs in examples/:

    bhai bol "hello"        print a value
    bhai age = 21           set a variable
    age = age + 1           reassign one
    jab tak age < 3         repeat while a comparison holds
        bhai bol age
    bas

One loop may be open at a time, and a loop whose comparison is already false
never runs. Arithmetic is left to right, so 2 + 3 * 4 is 20.
"""

import re

_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\S+')
_OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}
_ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
# A guard so a loop with no progress fails loudly instead of hanging.
_MAX_STEPS = 100_000


def _tokens(line):
    found = _TOKEN.findall(line.strip())
    if found and found[0] == "bhai":
        return found[1:]
    return found


def _unescape(body):
    """Decode the few escapes a demo needs, leaving other characters alone."""
    out = []
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body):
            out.append(_ESCAPES.get(body[index + 1], body[index + 1]))
            index += 2
            continue
        out.append(char)
        index += 1
    return "".join(out)


def _value(token, env):
    if token.startswith('"') and token.endswith('"'):
        return _unescape(token[1:-1])
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    if token not in env:
        raise NameError(f"unknown name: {token}")
    return env[token]


def _expression(parts, env):
    """Evaluate left to right. Parentheses and precedence are not supported."""
    if not parts:
        raise ValueError("empty expression")
    result = _value(parts[0], env)
    index = 1
    while index < len(parts):
        op = parts[index]
        if op not in _OPS or index + 1 >= len(parts):
            raise ValueError(f"cannot evaluate: {' '.join(parts)}")
        try:
            result = _OPS[op](result, _value(parts[index + 1], env))
        except TypeError:
            raise ValueError(f"cannot combine {parts[index - 1]} {op} {parts[index + 1]}")
        index += 2
    return result


def _compare(parts, env):
    if len(parts) != 3 or parts[1] not in {"<", ">", "=="}:
        raise ValueError("comparison must look like: name < 3")
    left, op, right = _value(parts[0], env), parts[1], _value(parts[2], env)
    if op == "<":
        return left < right
    if op == ">":
        return left > right
    return left == right


def _skip_loop(lines, start):
    """Index just past the bas that closes a loop beginning at start."""
    for index in range(start, len(lines)):
        if _tokens(lines[index]) == ["bas"]:
            return index + 1
    raise SyntaxError("loop never closed with 'bas'")


def run(source, output=None):
    """Run a bhai-lang program. Returns the list of printed lines."""
    printed = output if output is not None else []
    env = {}
    lines = source.splitlines()
    index = 0
    loop = None  # (condition tokens, first body line)
    steps = 0

    while index < len(lines):
        steps += 1
        if steps > _MAX_STEPS:
            raise RuntimeError(f"stopped after {_MAX_STEPS} steps; the loop never ends")
        raw = lines[index].strip()
        if not raw or raw.startswith("#"):
            index += 1
            continue
        parts = _tokens(raw)

        if parts[:2] == ["jab", "tak"]:
            if loop is not None:
                raise SyntaxError("only one loop may be open at a time")
            condition = parts[2:]
            if not _compare(condition, env):
                index = _skip_loop(lines, index + 1)
                continue
            loop = (condition, index + 1)
            index += 1
            continue
        if parts == ["bas"]:
            if loop is None:
                raise SyntaxError("'bas' without a matching 'jab tak'")
            condition, start = loop
            if _compare(condition, env):
                index = start
            else:
                loop = None
                index += 1
            continue
        if parts and parts[0] == "bol":
            printed.append(str(_expression(parts[1:], env)))
        elif len(parts) >= 3 and parts[1] == "=":
            env[parts[0]] = _expression(parts[2:], env)
        else:
            raise SyntaxError(f"cannot read: {raw}")
        index += 1

    if loop is not None:
        raise SyntaxError("loop never closed with 'bas'")
    return printed
