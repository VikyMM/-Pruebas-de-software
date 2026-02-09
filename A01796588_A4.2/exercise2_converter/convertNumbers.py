#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Convert numbers from a text file to binary and hexadecimal (basic algorithms).

Usage:
    python convertNumbers.py path/to/file.txt

Outputs:
    - Prints results to console
    - Writes results to ConvertionResults.txt

Notes:
    - Uses basic algorithms (no bin(), hex(), format()).
    - Invalid lines are reported and execution continues.
"""

from __future__ import annotations

import sys
import time
from typing import List

HEX_DIGITS = "0123456789ABCDEF"


def parse_int(text: str) -> int | None:
    """Parse an integer from a line. Returns None if invalid."""
    s = text.strip()

    if not s:
        return None

    sign = 1
    if s[0] in "+-":
        if s[0] == "-":
            sign = -1
        s = s[1:].strip()

    if not s:
        return None

    # Only digits allowed (integers only)
    for ch in s:
        if ch < "0" or ch > "9":
            return None

    value = 0
    for ch in s:
        value = value * 10 + (ord(ch) - ord("0"))

    return sign * value


def to_binary(n: int) -> str:
    """Convert integer to base-2 string using a basic algorithm.

    Negative numbers use 10-bit two's complement representation.
    """
    if n == 0:
        return "0"

    if n < 0:
        n = (2 ** 10) + n

    digits: List[str] = []
    while n > 0:
        digits.append("1" if (n % 2) == 1 else "0")
        n //= 2

    digits.reverse()
    return "".join(digits)


def to_hex(n: int) -> str:
    """Convert integer to base-16 string using a basic algorithm.

    Negative numbers use 40-bit two's complement representation.
    """
    if n == 0:
        return "0"

    if n < 0:
        n = (2 ** 40) + n

    digits: List[str] = []
    while n > 0:
        digits.append(HEX_DIGITS[n % 16])
        n //= 16

    digits.reverse()
    return "".join(digits)


def build_report(source_file: str, lines: List[str]) -> str:
    """Build the output report text."""
    output: List[str] = []
    output.append(f"FILE: {source_file}")
    output.append("ITEM\tDECIMAL\tBINARY\tHEXADECIMAL")

    item = 0
    for idx, raw in enumerate(lines, start=1):
        value = parse_int(raw)
        if value is None:
            output.append(f"[ERROR] Line {idx}: invalid data -> {raw.rstrip()!r}")
            continue

        item += 1
        output.append(f"{item}\t{value}\t{to_binary(value)}\t{to_hex(value)}")

    return "\n".join(output) + "\n"


def main(argv: List[str]) -> int:
    """Program entry point."""
    start = time.perf_counter()

    if len(argv) != 2:
        print("Usage: python convertNumbers.py path/to/file.txt")
        return 1

    input_path = argv[1]

    try:
        with open(input_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_path}")
        return 1

    report = build_report(input_path, lines)

    elapsed = time.perf_counter() - start
    report += f"ELAPSED_TIME_SECONDS: {elapsed}\n"

    # Console output
    print(report)

    # File output (same folder where you run the command)
    with open("ConvertionResults.txt", "w", encoding="utf-8") as out:
        out.write(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
