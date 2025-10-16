#!/bin/bash

# Usage: ./check_rows_awk.sh small_file.csv large_file.csv output_results.txt

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <small_csv> <large_csv> <output_file>"
    exit 1
fi

SMALL_FILE="$1"
LARGE_FILE="$2"
OUTPUT_FILE="$3"

echo "Processing files..."

# Use awk to create hash table from large file and check small file
awk '
NR==FNR { 
    # Reading large file (skip header at line 1)
    if (NR > 1) {
        seen[$0] = 1
    }
    next
}
FNR > 1 { 
    # Reading small file (skip header at line 1)
    if ($0 in seen) {
        print "True"
    } else {
        print "False"
    }
}
' "$LARGE_FILE" "$SMALL_FILE" > "$OUTPUT_FILE"

# Summary
FOUND_COUNT=$(grep -c "True" "$OUTPUT_FILE")
TOTAL_COUNT=$(wc -l < "$OUTPUT_FILE")
echo "Done! Results written to $OUTPUT_FILE"
echo "Found: $FOUND_COUNT / $TOTAL_COUNT rows"