#!/usr/bin/env python3
"""
convert_fps.py
--------------
Batch convert .mov files from 120fps to 30fps using ffmpeg.

Requirements:
    - ffmpeg installed and available in PATH
      (Windows: download from https://ffmpeg.org/download.html and add to PATH)
      (Mac: brew install ffmpeg)
      (Linux: sudo apt install ffmpeg)

Usage:
    python convert_fps.py                # converts all .mov in current folder
    python convert_fps.py /path/to/folder
    python convert_fps.py --mode slowmo   # keeps all 120 frames -> slow motion result
    python convert_fps.py --mode normal   # drops frames, keeps real-time speed (default)

Modes:
    normal  -> ffmpeg -filter:v fps=30   (real-time speed, frames dropped)
    slowmo  -> ffmpeg -r 30              (all original frames kept -> slow motion output)
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


def convert_file(input_path: Path, output_dir: Path, mode: str):
    output_path = output_dir / f"{input_path.stem}_30fps{input_path.suffix}"

    if mode == "slowmo":
        cmd = ["ffmpeg", "-y", "-i", str(input_path), "-r", "30", str(output_path)]
    else:  # normal
        cmd = ["ffmpeg", "-y", "-i", str(input_path), "-filter:v", "fps=30", str(output_path)]

    print(f"🎬 Converting: {input_path.name} -> {output_path.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed: {input_path.name}")
        print(result.stderr[-500:])  # show last part of error log
        return False

    print(f"✅ Done: {output_path.name}")
    return True


def main():
    args = sys.argv[1:]

    mode = "normal"
    if "--mode" in args:
        idx = args.index("--mode")
        mode = args[idx + 1]
        del args[idx:idx + 2]

    if mode not in ("normal", "slowmo"):
        print("❌ Invalid --mode. Use 'normal' or 'slowmo'.")
        sys.exit(1)

    folder = Path(args[0]) if args else Path.cwd()
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    check_ffmpeg()

    mov_files = sorted(folder.glob("*.mov")) + sorted(folder.glob("*.MOV"))
    if not mov_files:
        print(f"⚠️  Koi .mov file nahi mili is folder mein: {folder}")
        sys.exit(0)

    output_dir = folder / "converted_30fps"
    output_dir.mkdir(exist_ok=True)

    print(f"📂 Folder: {folder}")
    print(f"🎚️  Mode: {mode}  ({'speed same rahegi, frames drop honge' if mode == 'normal' else 'slow motion result, saare frames keep honge'})")
    print(f"📦 Found {len(mov_files)} .mov file(s)\n")

    success, failed = 0, 0
    for f in mov_files:
        if convert_file(f, output_dir, mode):
            success += 1
        else:
            failed += 1

    print(f"\n🎉 Summary: {success} converted, {failed} failed")
    print(f"📁 Output folder: {output_dir}")


if __name__ == "__main__":
    main()
