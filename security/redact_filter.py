#!/usr/bin/env python3
import re
import sys

PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}['\"]?"),
    re.compile(r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9/_+=-]{16,}['\"]?"),
    re.compile(r"(?i)password\s*[:=]\s*['\"]?.{6,}['\"]?"),
    re.compile(r"-----BEGIN (?:RSA|EC|PRIVATE) KEY-----[\s\S]*?-----END (?:RSA|EC|PRIVATE) KEY-----"),
]

REPLACEMENT = "<REDACTED>"

def redact(text: str) -> str:
    out = text
    for pat in PATTERNS:
        out = pat.sub(REPLACEMENT, out)
    return out

def main() -> None:
    data = sys.stdin.read()
    redacted = redact(data)
    sys.stdout.write(redacted)

if __name__ == "__main__":
    main()

