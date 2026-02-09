#!/usr/bin/env python3
"""
Compute descriptive statistics from a text file.

Statistics:
- Count
- Mean
- Median
- Mode
- Standard deviation (population)
- Variance (population)
pyth
Usage:
    python computeStatistics.py path/to/file.txt
"""
# pylint: disable=invalid-name

from __future__ import annotations

import sys
import time
from typing import List, Optional


def is_number(text: str) -> bool:
    """Return True if text can be parsed as float; False otherwise."""
    try:
        float(text)
        return True
    except ValueError:
        return False


def read_numbers(file_path: str) -> List[float]:
    """
    Read numbers from file. Invalid lines are reported and skipped.
    Execution continues as required.
    """
    numbers: List[float] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for idx, raw in enumerate(file, start=1):
            value = raw.strip()
            if value == "":
                # Ignore empty lines silently (or you can warn if you want)
                continue
            if not is_number(value):
                print(f"[ERROR] Line {idx}: invalid data -> {value!r}")
                continue
            numbers.append(float(value))
    return numbers


def merge_sort(values: List[float]) -> List[float]:
    """Sort list using merge sort (no reliance on built-in sort for the core algorithm)."""
    if len(values) <= 1:
        return values[:]
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    return merge(left, right)


def merge(left: List[float], right: List[float]) -> List[float]:
    """Merge two sorted lists."""
    result: List[float] = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def mean(values: List[float]) -> float:
    """Compute the arithmetic mean of a list of numbers."""
    total = 0.0
    for v in values:
        total += v
    return total / float(len(values))


def median(sorted_values: List[float]) -> float:
    """Compute the median from a sorted list of numbers."""
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 1:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def mode(values: List[float]) -> Optional[float]:
    """
    Return one mode if there are repeated values.
    If no value repeats, return None.
    """
    freq = {}
    for v in values:
        freq[v] = freq.get(v, 0) + 1

    max_count = 0
    mode_value = None

    for v, count in freq.items():
        if count > max_count:
            max_count = count
            mode_value = v

    if max_count <= 1:
        return None

    return mode_value


def variance_population(values: List[float], avg: float) -> float:
    """Compute the population variance (divide by n)."""
    total = 0.0
    for v in values:
        diff = v - avg
        total += diff * diff
    return total / float(len(values))


def sqrt_newton(x: float, iterations: int = 30) -> float:
    """Square root using Newton-Raphson (basic algorithm)."""
    if x < 0:
        raise ValueError("Cannot sqrt negative number.")
    if x == 0:
        return 0.0
    guess = x if x >= 1.0 else 1.0
    for _ in range(iterations):
        guess = 0.5 * (guess + x / guess)
    return guess


def format_value(val: Optional[float]) -> str:
    """Format a value for display; return '#N/A' if None."""
    if val is None:
        return "#N/A"
    return f"{val}"


def build_report(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    count: int,
    avg: float,
    med: float,
    mod: Optional[float],
    sd: float,
    var_: float,
    elapsed_sec: float,
) -> str:
    """Build the statistics report as a formatted string."""
    lines = [
        f"COUNT: {count}",
        f"MEAN: {avg}",
        f"MEDIAN: {med}",
        f"MODE: {format_value(mod)}",
        f"STANDARD_DEVIATION: {sd}",
        f"VARIANCE: {var_}",
        f"ELAPSED_TIME_SECONDS: {elapsed_sec}",
    ]
    return "\n".join(lines) + "\n"


def main(argv: List[str]) -> int:
    """Parse arguments and compute statistics from the given file."""
    if len(argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return 2

    file_path = argv[1]
    start = time.perf_counter()

    try:
        values = read_numbers(file_path)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return 1

    if len(values) == 0:
        print("[ERROR] No valid numeric data found.")
        return 1

    sorted_values = merge_sort(values)

    avg = mean(values)
    med = median(sorted_values)
    mod = mode(values)
    var_ = variance_population(values, avg)
    sd = sqrt_newton(var_)

    elapsed = time.perf_counter() - start

    report = build_report(
        count=len(values),
        avg=avg,
        med=med,
        mod=mod,
        sd=sd,
        var_=var_,
        elapsed_sec=elapsed,
    )

    # Output to console
    print(report)

    # Output to file (same folder where you run it)
    with open("StatisticsResults.txt", "w", encoding="utf-8") as out:
        out.write(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
