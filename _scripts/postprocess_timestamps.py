#!/usr/bin/env python3
"""
Post-process timestamps to fix gaps between words.

This script fills gaps between consecutive words by extending the previous
word's end time to meet the next word's start time. This ensures smooth
continuous highlighting without "jumping" during karaoke playback.

Usage:
    python postprocess_timestamps.py <timestamp_json_file>
    python postprocess_timestamps.py --all  # Process all timestamp files
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict


def fix_gaps(words: List[Dict]) -> List[Dict]:
    """
    Fill gaps between consecutive words.

    For each pair of words, if there's a gap (word[i].end < word[i+1].start),
    extend word[i].end to meet word[i+1].start.

    This ensures continuous highlighting without dead time.
    Fast words remain fast - we don't enforce minimum durations.
    """
    if not words or len(words) < 2:
        return words

    fixed = [word.copy() for word in words]

    for i in range(len(fixed) - 1):
        current_end = fixed[i]['end']
        next_start = fixed[i + 1]['start']

        gap = next_start - current_end

        if gap > 0:
            # Fill the gap by extending current word's end
            fixed[i]['end'] = next_start

    return fixed


def process_timestamp_file(input_path: str, output_path: str = None) -> dict:
    """
    Process a single timestamp JSON file.

    Args:
        input_path: Path to input JSON file
        output_path: Path to output JSON file (defaults to overwriting input)

    Returns:
        Processed timestamp data
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_words = data.get('words', [])

    # Count gaps before processing
    gaps_before = sum(
        1 for i in range(len(original_words) - 1)
        if original_words[i + 1]['start'] - original_words[i]['end'] > 0
    )

    # Apply gap fixing
    data['words'] = fix_gaps(original_words)

    # Mark as post-processed
    data['postprocessed'] = True
    data['gaps_fixed'] = gaps_before

    # Save
    output_path = output_path or input_path
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def process_all_timestamps(timestamps_dir: Path) -> None:
    """Process all timestamp files in the directory."""
    for year_dir in ['1_ano', '2_ano']:
        year_path = timestamps_dir / year_dir
        if not year_path.exists():
            continue

        for json_file in sorted(year_path.glob('*.json')):
            print(f"Processing: {json_file.name}...", end=' ')
            try:
                result = process_timestamp_file(str(json_file))
                print(f"OK (fixed {result.get('gaps_fixed', 0)} gaps)")
            except Exception as e:
                print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Post-process timestamps to fix gaps between words"
    )
    parser.add_argument(
        "file",
        nargs='?',
        help="Path to timestamp JSON file (or --all to process all)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all timestamp files in _timestamps directory"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (defaults to overwriting input)"
    )

    args = parser.parse_args()

    if args.all:
        # Find project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        timestamps_dir = project_root / "_timestamps"

        if not timestamps_dir.exists():
            print(f"Error: Timestamps directory not found: {timestamps_dir}")
            return 1

        process_all_timestamps(timestamps_dir)
    elif args.file:
        input_path = Path(args.file)
        if not input_path.exists():
            print(f"Error: File not found: {input_path}")
            return 1

        result = process_timestamp_file(str(input_path), args.output)
        print(f"Processed: {input_path.name}")
        print(f"  Words: {len(result.get('words', []))}")
        print(f"  Gaps fixed: {result.get('gaps_fixed', 0)}")
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
