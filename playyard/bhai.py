"""A tiny interpreter for a few words of bhai-lang.

bhai-lang (github.com/DulLabs/bhai-lang) is a toy language whose keywords are
Hindi. This covers just enough of it to run the programs in examples/:

    bhai bol "hello"        print a value
    bhai age = 21           set a variable
    age = age + 1           reassign one
    jab tak age < 3         repeat while a comparison holds
        bhai bol age
    bas

Only one loop may be open at a time, which keeps the control flow obvious.
"""

import re

_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\S+')
_OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}


def _tokens(line):
    found = _TOKEN.findall(line.strip())
    if found and found[0] == "bhai":
        return found[1:]
    return found


def _value(token, env):
    if token.startswith('"') and token.endswith('"'):
        return bytes(token[1:-1], "utf-8").decode("unicode_escape")
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    if token not in env:
        raise NameError(f"unknown name: {token}")
    return env[token]


def _expression(parts, env):
    """Evaluate a flat sum or product. Parentheses are not supported."""
    if not parts:
        raise ValueError("empty expression")
    result = _value(parts[0], env)
    index = 1
    while index < len(parts):
        op = parts[index]
        if op not in _OPS:
            raise ValueError(f"unknown operator: {op}")
        result = _OPS[op](result, _value(parts[index + 1], env))
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


def run(source, output=None):
    """Run a bhai-lang program. Returns the list of printed lines."""
    printed = output if output is not None else []
    env = {}
    lines = source.splitlines()
    index = 0
    loop = None  # (condition tokens, first body line)

    while index < len(lines):
        raw = lines[index].strip()
        if not raw or raw.startswith("#"):
            index += 1
            continue
        parts = _tokens(raw)

        if parts[:2] == ["jab", "tak"]:
            loop = (parts[2:], index + 1)
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
