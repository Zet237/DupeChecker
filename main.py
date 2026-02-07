# /// script
# dependencies = [
#   "pandas",
#   "openpyxl",
# ]
# ///

import pandas as pd
import os

input_file = 'checksums.txt'
output_file = 'duplicates.xlsx'


def process_duplicates(input_path, output_path):
    md5_counts = {}
    duplicates_data = []

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return

    print("Step 1: Counting MD5 occurrences...")
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split('  ', 1)
            if len(parts) < 2: continue
            md5 = parts[0].strip()
            md5_counts[md5] = md5_counts.get(md5, 0) + 1

    print("Step 2: Extracting duplicate details...")
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split('  ', 1)
            if len(parts) < 2: continue
            md5 = parts[0].strip()

            if md5_counts[md5] > 1:
                full_path = parts[1].strip()
                if '/' in full_path:
                    batch, filename = full_path.split('/', 1)
                else:
                    batch, filename = "Unknown", full_path

                duplicates_data.append({
                    "md5sum": md5,
                    "Batch": batch,
                    "Filename": filename,
                    "Amount": md5_counts[md5]  # It's definitely here!
                })

    if not duplicates_data:
        print("No duplicates found. Lucky you!")
        return

    print(f"Step 3: Creating DataFrame and sorting...")
    df = pd.DataFrame(duplicates_data)

    # Sort by Amount (High to Low) so you see the biggest problems first
    df = df.sort_values(by=['Amount', 'md5sum'], ascending=[False, True])

    print(f"Step 4: Writing to {output_path}...")
    # Using a context manager ensures the file is closed properly
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print("Success! Check the 'Amount' column.")


if __name__ == "__main__":
    process_duplicates(input_file, output_file)