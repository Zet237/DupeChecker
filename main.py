# /// script
# dependencies = [
#   "pandas",
#   "openpyxl",
# ]
# ///

import pandas as pd

input_file = 'checksums.txt'
output_file = 'duplicates.xlsx'


def process_duplicates(input_path, output_path):
    md5_counts = {}
    duplicates_data = []

    print("Step 1: Counting MD5 occurrences...")
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            # Split by the FIRST occurrence of two spaces
            # This separates the hash from the path reliably
            parts = line.split('  ', 1)
            if len(parts) < 2: continue

            md5 = parts[0].strip()
            md5_counts[md5] = md5_counts.get(md5, 0) + 1

    print("Step 2: Extracting duplicate details...")
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.split('  ', 1)
            md5 = parts[0].strip()

            # Only process if this MD5 appeared more than once
            if md5_counts[md5] > 1:
                full_path = parts[1].strip()

                # Split at the first "/" to separate Batch from Filename
                if '/' in full_path:
                    batch, filename = full_path.split('/', 1)
                else:
                    batch, filename = "Unknown", full_path

                duplicates_data.append({
                    "md5sum": md5,
                    "Batch": batch,
                    "Filename": filename
                })

    print(f"Step 3: Writing {len(duplicates_data)} rows to Excel...")
    df = pd.DataFrame(duplicates_data)
    # Sorting helps keep the duplicates grouped together visually
    df.sort_values(by='md5sum', inplace=True)
    df.to_excel(output_path, index=False)
    print("Done!")


process_duplicates(input_file, output_file)