#!/usr/bin/env python3
"""
Regenerate all timestamps and update HTML files.

This is the master script that orchestrates:
1. Post-processing timestamps (fixing gaps)
2. Updating HTML files with fixed timestamps

Usage:
    python regenerate_all.py              # Process all files
    python regenerate_all.py --year 1_ano # Process only 1_ano
    python regenerate_all.py --file lgp36 # Process single file
    python regenerate_all.py --dry-run    # Show what would be done
"""

import argparse
import json
from pathlib import Path
import sys

# Add script directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from postprocess_timestamps import fix_gaps, process_timestamp_file
from update_html_timestamps import update_html_with_timestamps, find_html_for_timestamp


def process_single_oed(timestamp_path: Path, project_root: Path, dry_run: bool = False) -> dict:
    """
    Process a single OED: fix timestamps and update HTML.

    Returns:
        Dictionary with processing results
    """
    result = {
        'file': timestamp_path.name,
        'success': False,
        'gaps_fixed': 0,
        'html_updated': False
    }

    try:
        # Step 1: Read and analyze timestamps
        with open(timestamp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        words = data.get('words', [])

        # Count gaps
        gaps = sum(
            1 for i in range(len(words) - 1)
            if words[i + 1]['start'] - words[i]['end'] > 0
        )
        result['gaps_fixed'] = gaps

        if dry_run:
            print(f"  Would fix {gaps} gaps in {timestamp_path.name}")
            html_path = find_html_for_timestamp(timestamp_path, project_root)
            print(f"  Would update {html_path}")
            result['success'] = True
            return result

        # Step 2: Fix gaps and save
        data['words'] = fix_gaps(words)
        data['postprocessed'] = True
        data['gaps_fixed'] = gaps

        with open(timestamp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Step 3: Update HTML
        html_path = find_html_for_timestamp(timestamp_path, project_root)
        if html_path.exists():
            update_html_with_timestamps(str(html_path), data['words'])
            result['html_updated'] = True

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate timestamps and update HTML files"
    )
    parser.add_argument(
        "--year",
        choices=['1_ano', '2_ano'],
        help="Process only specific year"
    )
    parser.add_argument(
        "--file",
        help="Process single file (e.g., lgp36 or 11_lgp36)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    project_root = script_dir.parent
    timestamps_dir = project_root / "_timestamps"

    if not timestamps_dir.exists():
        print(f"Error: Timestamps directory not found: {timestamps_dir}")
        return 1

    # Determine which files to process
    files_to_process = []

    if args.file:
        # Single file
        file_pattern = args.file
        if not file_pattern.endswith('.json'):
            # Try to find matching file
            for year in ['1_ano', '2_ano']:
                year_path = timestamps_dir / year
                for json_file in year_path.glob('*.json'):
                    if args.file in json_file.stem:
                        files_to_process.append(json_file)
                        break
                if files_to_process:
                    break
        else:
            files_to_process.append(Path(args.file))
    else:
        # All files
        years = [args.year] if args.year else ['1_ano', '2_ano']
        for year in years:
            year_path = timestamps_dir / year
            if year_path.exists():
                files_to_process.extend(sorted(year_path.glob('*.json')))

    if not files_to_process:
        print("No files to process")
        return 1

    print(f"{'DRY RUN - ' if args.dry_run else ''}Processing {len(files_to_process)} files...\n")

    # Process files
    total_gaps = 0
    success_count = 0
    error_count = 0

    for timestamp_path in files_to_process:
        print(f"Processing: {timestamp_path.name}")
        result = process_single_oed(timestamp_path, project_root, args.dry_run)

        if result['success']:
            success_count += 1
            total_gaps += result['gaps_fixed']
            status = "OK"
            if result['gaps_fixed'] > 0:
                status += f" (fixed {result['gaps_fixed']} gaps)"
            if result.get('html_updated'):
                status += " [HTML updated]"
            print(f"  -> {status}")
        else:
            error_count += 1
            print(f"  -> ERROR: {result.get('error', 'Unknown error')}")

    # Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Files processed: {success_count}")
    print(f"  Total gaps fixed: {total_gaps}")
    print(f"  Errors: {error_count}")

    if args.dry_run:
        print(f"\nThis was a dry run. No files were modified.")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
