#!/usr/bin/env python3
"""
Generate word-level timestamps from audio files using whisper-timestamped.

Usage:
    python generate_timestamps.py <audio_file> [--language pt] [--model base]

Example:
    python scripts/generate_timestamps.py _assets/audios/1_ano/11_lgp21.mp3 --language pt

Output:
    JSON file in _timestamps/ folder with word-level timing data.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import whisper_timestamped as whisper
except ImportError:
    print("Error: whisper-timestamped not installed.")
    print("Install with: pip install openai-whisper whisper-timestamped torch")
    sys.exit(1)


def generate_timestamps(audio_path: str, language: str = "pt", model_name: str = "base") -> dict:
    """
    Generate word-level timestamps from an audio file.

    Args:
        audio_path: Path to the audio file (mp3, wav, etc.)
        language: Language code (default: "pt" for Portuguese)
        model_name: Whisper model to use (tiny, base, small, medium, large)

    Returns:
        Dictionary with word-level timestamps
    """
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"Processing audio: {audio_path}")
    result = whisper.transcribe(model, audio_path, language=language)

    # Extract word-level timestamps
    words = []
    for segment in result.get("segments", []):
        for word_info in segment.get("words", []):
            words.append({
                "word": word_info["text"].strip().upper(),
                "start": round(word_info["start"], 3),
                "end": round(word_info["end"], 3)
            })

    return {
        "audio_file": os.path.basename(audio_path),
        "language": language,
        "model": model_name,
        "duration": result.get("duration", 0),
        "words": words,
        "full_text": result.get("text", "").strip().upper()
    }


def save_timestamps(data: dict, output_path: str):
    """Save timestamps to JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Timestamps saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate word-level timestamps from audio using Whisper"
    )
    parser.add_argument(
        "audio_file",
        help="Path to the audio file (mp3, wav, etc.)"
    )
    parser.add_argument(
        "--language", "-l",
        default="pt",
        help="Language code (default: pt for Portuguese)"
    )
    parser.add_argument(
        "--model", "-m",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: _timestamps/<year>/<filename>.json)"
    )

    args = parser.parse_args()

    # Validate input file
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    # Generate timestamps
    timestamps = generate_timestamps(
        str(audio_path),
        language=args.language,
        model_name=args.model
    )

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Auto-detect year folder from path (e.g., "1_ano" or "2_ano")
        year_folder = "1_ano"  # default
        path_parts = audio_path.parts
        for part in path_parts:
            if part in ["1_ano", "2_ano"]:
                year_folder = part
                break

        # Get script directory to find project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        output_dir = project_root / "_timestamps" / year_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{audio_path.stem}.json"

    # Save timestamps
    save_timestamps(timestamps, str(output_path))

    # Print summary
    print(f"\nSummary:")
    print(f"  Words detected: {len(timestamps['words'])}")
    print(f"  Duration: {timestamps['duration']:.2f}s")
    print(f"  Full text: {timestamps['full_text'][:100]}...")


if __name__ == "__main__":
    main()
