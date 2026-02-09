#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Count distinct words and their frequency from a text file.

Usage:
    python wordCount.py fileWithData.txt

Outputs:
    - Prints results to console
    - Writes results to WordCountResults.txt
"""

from __future__ import annotations

import sys
import time


def count_words(file_path: str) -> dict[str, int]:
    """Read words from a file and count their frequencies.

    Each line is stripped and split by whitespace.
    Every token is counted as a word.

    Args:
        file_path: Path to the input file.

    Returns:
        A dictionary mapping each word to its frequency count.
    """
    frequency: dict[str, int] = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            raw = line.strip()
            if not raw:
                continue
            words = raw.split()
            for word in words:
                if not word:
                    continue
                if word in frequency:
                    frequency[word] += 1
                else:
                    frequency[word] = 1
    return frequency


def sort_by_frequency(frequency: dict[str, int]) -> list[tuple[str, int]]:
    """Sort word-frequency pairs by count descending using insertion sort.

    Args:
        frequency: Dictionary mapping words to counts.

    Returns:
        A list of (word, count) tuples sorted by count descending.
    """
    pairs: list[tuple[str, int]] = []
    for word, count in frequency.items():
        pairs.append((word, count))
    for i in range(1, len(pairs)):
        key = pairs[i]
        j = i - 1
        while j >= 0 and pairs[j][1] < key[1]:
            pairs[j + 1] = pairs[j]
            j -= 1
        pairs[j + 1] = key
    return pairs


def main(argv: list[str]) -> int:
    """Parse arguments, count words, and output results."""
    if len(argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        return 1

    input_file = argv[1]
    start_time = time.time()

    try:
        frequency = count_words(input_file)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_file}")
        return 1

    sorted_pairs = sort_by_frequency(frequency)

    total_words = 0
    for _, count in sorted_pairs:
        total_words += count

    elapsed_time = time.time() - start_time

    results_lines = []
    for word, count in sorted_pairs:
        results_lines.append(f"{word}\t{count}")
    results_lines.append(f"Grand Total\t{total_words}")
    results_lines.append(f"Elapsed Time: {elapsed_time:.6f} seconds")

    for line in results_lines:
        print(line)

    with open("WordCountResults.txt", "w", encoding="utf-8") as out:
        for line in results_lines:
            out.write(line + "\n")

    print("\nResults written to WordCountResults.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
