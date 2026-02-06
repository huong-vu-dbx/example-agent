#!/usr/bin/env python3
"""
Script to clean up FCA Handbook files by removing navigation header and footer content.
"""

import os
import re

def clean_file(file_path):
    """
    Remove navigation header and footer from a scraped file.

    Args:
        file_path: Path to the file to clean
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find where the actual CASS content starts
        # The pattern is usually after "FCA Handbook" and before "CASS"
        markers = [
            'Sign Up / Sign In\nSearch\nClear\nHome\nFCA Handbook',
            'FCA Handbook in print\nSign Up / Sign In',
        ]

        # Try to find the end of navigation content
        cleaned_content = content
        for marker in markers:
            if marker in content:
                # Split at the marker and take everything after it
                parts = content.split(marker, 1)
                if len(parts) > 1:
                    cleaned_content = parts[1].strip()
                    break

        # Also try to find where "CASS" chapter actually starts
        # Look for patterns like "CASS 1", "CASS 7", etc.
        cass_pattern = r'\n(CASS \d+[a-z]*)'
        match = re.search(cass_pattern, cleaned_content)
        if match:
            # Find the position of this match and keep everything from there
            start_pos = match.start()
            cleaned_content = cleaned_content[start_pos:].strip()

        # Remove footer content - find common footer markers
        footer_markers = [
            'Previous Chapter',
            'Next Chapter\nAccessibility',
            'Accessibility\nTerms & Conditions',
        ]

        for marker in footer_markers:
            if marker in cleaned_content:
                # Split at the marker and take everything before it
                parts = cleaned_content.split(marker, 1)
                cleaned_content = parts[0].strip()
                break

        # Write back the cleaned content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"✓ Cleaned {os.path.basename(file_path)}")
        return True

    except Exception as e:
        print(f"✗ Error cleaning {file_path}: {e}")
        return False

def main():
    """Clean all files in the fca_handbook_cass directory."""
    directory = "fca_handbook_cass"

    if not os.path.exists(directory):
        print(f"Directory {directory} not found!")
        return

    files = [f for f in os.listdir(directory) if f.endswith('.txt')]

    success_count = 0
    for filename in sorted(files):
        file_path = os.path.join(directory, filename)
        if clean_file(file_path):
            success_count += 1

    print(f"\nCleaned {success_count}/{len(files)} files successfully")

if __name__ == "__main__":
    main()
