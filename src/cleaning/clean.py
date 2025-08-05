import re

# Define a rough pattern that matches strange lines (Tregex-like)
pattern = re.compile(r"[<>:\[\]|\\]")  # adjust as needed

with open("syntactic_stages_all.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f]

# Keep only clean lines
clean_lines = [line for line in lines if not pattern.search(line)]

# Save cleaned lines
with open("cleaned.txt", "w", encoding="utf-8") as out:
    for line in clean_lines:
        out.write(line + "\n")
