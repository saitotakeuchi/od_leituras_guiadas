#!/usr/bin/env python3
"""
Update HTML files with timestamps from JSON files.

This script reads timestamp JSON files and updates the corresponding HTML files
with the correct data-start and data-end attributes on each word span.

Usage:
    python update_html_timestamps.py <timestamp_json> <html_file>
    python update_html_timestamps.py --all  # Update all HTML files from timestamps
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Dict


def update_html_with_timestamps(html_path: str, words: List[Dict]) -> bool:
    """
    Update HTML file with new timestamp data.

    Matches words from JSON to spans in HTML and updates data-start/data-end.

    Args:
        html_path: Path to HTML file
        words: List of word dictionaries with 'word', 'start', 'end' keys

    Returns:
        True if successful, False otherwise
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all spans with data-start attributes
    # Pattern: <span data-start="X.XX" data-end="Y.YY">WORD</span>
    span_pattern = re.compile(
        r'<span\s+data-start="[\d.]+"(?:\s+data-end="[\d.]+")?>([^<]+)</span>',
        re.IGNORECASE
    )

    matches = list(span_pattern.finditer(content))

    if len(matches) != len(words):
        print(f"  Warning: Word count mismatch - HTML has {len(matches)} spans, JSON has {len(words)} words")
        # Try to proceed anyway if counts are close
        if abs(len(matches) - len(words)) > 5:
            print(f"  Skipping due to large mismatch")
            return False

    # Build replacement map
    new_content = content
    offset = 0  # Track offset as we modify the string

    for i, match in enumerate(matches):
        if i >= len(words):
            break

        word_data = words[i]
        original_span = match.group(0)
        word_text = match.group(1)

        # Create new span with updated timestamps
        new_span = f'<span data-start="{word_data["start"]}" data-end="{word_data["end"]}">{word_text}</span>'

        # Calculate positions with offset
        start_pos = match.start() + offset
        end_pos = match.end() + offset

        # Replace in content
        new_content = new_content[:start_pos] + new_span + new_content[end_pos:]

        # Update offset for next replacement
        offset += len(new_span) - len(original_span)

    # Write updated content
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def find_html_for_timestamp(timestamp_path: Path, project_root: Path) -> Path:
    """
    Find the corresponding HTML file for a timestamp JSON file.

    Examples:
        11_lgp36.json -> 1_ano/lgp36/index.html
        21_lgp15.json -> 2_ano/lgp15/index.html
    """
    filename = timestamp_path.stem  # e.g., "11_lgp36" or "21_lgp15"

    # Parse year and page number
    if filename.startswith("11_"):
        year = "1_ano"
        page = filename[3:]  # "lgp36"
    elif filename.startswith("21_"):
        year = "2_ano"
        page = filename[3:]  # "lgp15"
    else:
        # Fallback: try to detect from parent directory
        year = timestamp_path.parent.name
        page = filename

    html_path = project_root / year / page / "index.html"
    return html_path


def process_single(timestamp_path: str, html_path: str = None) -> bool:
    """Process a single timestamp/HTML pair."""
    timestamp_path = Path(timestamp_path)

    with open(timestamp_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    words = data.get('words', [])

    if html_path:
        html_path = Path(html_path)
    else:
        # Auto-detect HTML path
        project_root = timestamp_path.parent.parent.parent
        html_path = find_html_for_timestamp(timestamp_path, project_root)

    if not html_path.exists():
        print(f"  HTML file not found: {html_path}")
        return False

    print(f"  Updating: {html_path}")
    return update_html_with_timestamps(str(html_path), words)


def process_all(project_root: Path) -> None:
    """Process all timestamp files and update corresponding HTML files."""
    timestamps_dir = project_root / "_timestamps"

    for year_dir in ['1_ano', '2_ano']:
        year_path = timestamps_dir / year_dir
        if not year_path.exists():
            continue

        print(f"\nProcessing {year_dir}:")
        for json_file in sorted(year_path.glob('*.json')):
            print(f"  {json_file.name}...", end=' ')
            try:
                success = process_single(str(json_file))
                print("OK" if success else "SKIPPED")
            except Exception as e:
                print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Update HTML files with timestamps from JSON"
    )
    parser.add_argument(
        "timestamp_file",
        nargs='?',
        help="Path to timestamp JSON file"
    )
    parser.add_argument(
        "html_file",
        nargs='?',
        help="Path to HTML file (auto-detected if not provided)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Update all HTML files from timestamp files"
    )

    args = parser.parse_args()

    if args.all:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        process_all(project_root)
    elif args.timestamp_file:
        success = process_single(args.timestamp_file, args.html_file)
        return 0 if success else 1
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
