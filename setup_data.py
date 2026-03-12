"""
setup_data.py — Download all required data files for Phishing Analyzer.

Downloads:
  - majestic_million.csv   (root of project)
"""

import os
import sys
import requests

MAJESTIC_MILLION_URL = "https://downloads.majestic.com/majestic_million.csv"
MAJESTIC_MILLION_PATH = "majestic_million.csv"
SPAM_TXT_PATH = os.path.join("data_collection", "spam.txt")


def download_with_progress(url: str, dest: str) -> None:
    print(f"Downloading {url}")
    print(f"  -> {dest}")

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0
    bar_len = 40

    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                pct = min(downloaded / total_size * 100, 100)
                filled = int(bar_len * pct / 100)
                bar = "#" * filled + "-" * (bar_len - filled)
                sys.stdout.write(f"\r  [{bar}] {pct:.1f}%")
                sys.stdout.flush()
    print()  # newline after progress bar


def main() -> None:
    # Download Majestic Million
    if os.path.exists(MAJESTIC_MILLION_PATH):
        answer = input(f"{MAJESTIC_MILLION_PATH} already exists. Re-download? [y/N] ").strip().lower()
        if answer != "y":
            print("  Skipping download.")
        else:
            download_with_progress(MAJESTIC_MILLION_URL, MAJESTIC_MILLION_PATH)
    else:
        download_with_progress(MAJESTIC_MILLION_URL, MAJESTIC_MILLION_PATH)

    # Check required resource file
    if not os.path.exists(SPAM_TXT_PATH):
        print(
            f"\nWARNING: {SPAM_TXT_PATH} is missing.\n"
            "  This file contains phishing keyword(s) used by the dynamic model.\n"
            "  It should be committed to the repository. Add it and run:\n"
            "    git add data_collection/spam.txt && git commit -m 'Add spam keywords'"
        )
    else:
        print(f"  {SPAM_TXT_PATH} found.")

    print("\nAll data files are ready.")


if __name__ == "__main__":
    main()
