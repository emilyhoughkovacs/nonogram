#!/usr/bin/env python3
# Emits every 5x5 grid's clues (not deduped), one CSV row: r1..r5,c1..c5
# Use OS sort to uniquify.

from sys import stdout

def runs5(mask: int) -> str:
    # mask is 5-bit; bit 0 = leftmost cell
    out = []
    cnt = 0
    for i in range(5):
        if (mask >> i) & 1:
            cnt += 1
        else:
            if cnt:
                out.append(str(cnt))
                cnt = 0
    if cnt:
        out.append(str(cnt))
    return "0" if not out else "-".join(out)

# Precompute clue strings for all 32 possible lines.
CLUE = [runs5(m) for m in range(32)]

def col_mask(r0,r1,r2,r3,r4,j):
    # Build j-th column mask from rows (bit j of each row), top cell = bit 0
    return ((r0>>j)&1) | (((r1>>j)&1)<<1) | (((r2>>j)&1)<<2) | (((r3>>j)&1)<<3) | (((r4>>j)&1)<<4)

def main():
    # Header omitted here; we’ll add it before unique.
    # Iterate all 5 rows as 5-bit masks (0..31) → 32^5 rows
    write = stdout.write
    for r0 in range(32):
        r0s = CLUE[r0]
        for r1 in range(32):
            r1s = CLUE[r1]
            for r2 in range(32):
                r2s = CLUE[r2]
                for r3 in range(32):
                    r3s = CLUE[r3]
                    for r4 in range(32):
                        r4s = CLUE[r4]
                        c0s = CLUE[col_mask(r0,r1,r2,r3,r4,0)]
                        c1s = CLUE[col_mask(r0,r1,r2,r3,r4,1)]
                        c2s = CLUE[col_mask(r0,r1,r2,r3,r4,2)]
                        c3s = CLUE[col_mask(r0,r1,r2,r3,r4,3)]
                        c4s = CLUE[col_mask(r0,r1,r2,r3,r4,4)]
                        write(f"{r0s},{r1s},{r2s},{r3s},{r4s},{c0s},{c1s},{c2s},{c3s},{c4s}\n")

if __name__ == "__main__":
    main()