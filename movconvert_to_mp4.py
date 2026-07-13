#!/usr/bin/env python3
"""
convert_to_mp4.py
------------------
Batch convert video files (.mov, .avi, .mkv, etc.) to .mp4 while keeping
the original frame rate and quality (no fps change, just container/codec conversion).

Requirements:
    - ffmpeg installed and available in PATH
      (Windows: download from https://ffmpeg.org/download.html and add to PATH)
      (Mac: brew install ffmpeg)
      (Linux: sudo apt install ffmpeg)

Usage:
    python convert_to_mp4.py                  # converts all .mov in current folder
    python convert_to_mp4.py /path/to/folder
    python convert_to_mp4.py --ext mov,avi,mkv # convert multiple extensions
"""

import subprocess
import sys
import shutil
from pathlib import Path


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("❌ ffmpeg nahi mila. Pehle ffmpeg install karein:")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   Mac:     brew install ffmpeg")
        print("   Linux:   sudo apt install ffmpeg")
        sys.exit(1)


def convert_file(input_path: Path, output_dir: Path):
    output_path = output_dir / f"{input_path.stem}.mp4"

    # -c:v libx264 -c:a aac -> widely compatible mp4 (re-encode, fps untouched)
    # -crf 18 -> visually near-lossless quality
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_path),
    ]

    print(f"🎬 Converting: {input_path.name} -> {output_path.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed: {input_path.name}")
        print(result.stderr[-500:])
        return False

    print(f"✅ Done: {output_path.name}")
    return True


def main():
    args = sys.argv[1:]

    extensions = ["mov"]
    if "--ext" in args:
        idx = args.index("--ext")
        extensions = [e.strip().lower() for e in args[idx + 1].split(",")]
        del args[idx:idx + 2]

    folder = Path(args[0]) if args else Path.cwd()
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    check_ffmpeg()

    files = []
    for ext in extensions:
        files += sorted(folder.glob(f"*.{ext}"))
        files += sorted(folder.glob(f"*.{ext.upper()}"))
    files = sorted(set(files))

    if not files:
        print(f"⚠️  Koi matching file nahi mili is folder mein: {folder} (extensions: {extensions})")
        sys.exit(0)

    output_dir = folder / "converted_mp4"
    output_dir.mkdir(exist_ok=True)

    print(f"📂 Folder: {folder}")
    print(f"🎚️  FPS: original same rahegi (no frame rate change)")
    print(f"📦 Found {len(files)} file(s)\n")

    success, failed = 0, 0
    for f in files:
        if convert_file(f, output_dir):
            success += 1
        else:
            failed += 1

    print(f"\n🎉 Summary: {success} converted, {failed} failed")
    print(f"📁 Output folder: {output_dir}")


if __name__ == "__main__":
    main()
