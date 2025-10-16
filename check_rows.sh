#!/bin/bash

# Usage: ./check_rows.sh small_file.csv large_file.csv output_results.txt

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <small_csv> <large_csv> <output_file>"
    exit 1
fi

SMALL_FILE="$1"
LARGE_FILE="$2"
OUTPUT_FILE="$3"

# Create temporary files
TEMP_DIR=$(mktemp -d)
SMALL_SORTED="$TEMP_DIR/small_sorted.txt"
LARGE_SORTED="$TEMP_DIR/large_sorted.txt"
SMALL_NO_HEADER="$TEMP_DIR/small_no_header.txt"

echo "Processing files..."

# Remove header and sort small file (skip first line)
tail -n +2 "$SMALL_FILE" > "$SMALL_NO_HEADER"
sort "$SMALL_NO_HEADER" > "$SMALL_SORTED"

# Remove header and sort large file (skip first line)
echo "Sorting large file (this may take a while)..."
tail -n +2 "$LARGE_FILE" | sort > "$LARGE_SORTED"

# Find which rows from small file are in large file
echo "Comparing files..."
comm -12 "$SMALL_SORTED" "$LARGE_SORTED" > "$TEMP_DIR/found.txt"

# Create a lookup for found rows
declare -A found_rows
while IFS= read -r line; do
    found_rows["$line"]=1
done < "$TEMP_DIR/found.txt"

# Check each row from original small file (preserving order)
echo "Generating results..."
> "$OUTPUT_FILE"
while IFS= read -r line; do
    if [ -n "${found_rows[$line]}" ]; then
        echo "True" >> "$OUTPUT_FILE"
    else
        echo "False" >> "$OUTPUT_FILE"
    fi
done < "$SMALL_NO_HEADER"

# Cleanup
rm -rf "$TEMP_DIR"

# Summary
FOUND_COUNT=$(grep -c "True" "$OUTPUT_FILE")
echo "Done! Results written to $OUTPUT_FILE"
echo "Found: $FOUND_COUNT / 4162 rows"