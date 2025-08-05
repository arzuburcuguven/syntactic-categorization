from collections import Counter

# Load lines
with open("/Users/argy/workspace/extractor/data/captures/compiled/syntactic_stages_all.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f]

# Count duplicates
counts = Counter(lines)
duplicates = {line: count for line, count in counts.items() if count > 1}

# Save to file
with open("duplicates.txt", "w", encoding="utf-8") as out:
    for line, count in sorted(duplicates.items(), key=lambda x: -x[1]):
        out.write(f"{count}x\t{line}\n")
