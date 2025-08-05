#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} PATTERN INPUT_FILE OUT_PATH")
        sys.exit(1)

    pattern, input_file, out_path = sys.argv[1:]

    # Run tregex and get all matching lines
    cmd = f"./tregex.sh '{pattern}' '{input_file}' -t -o"
    matches = subprocess.getoutput(cmd)

    # Load already-saved lines (if any) to avoid duplicates
    seen = set()
    if os.path.exists(out_path):
        with open(out_path, 'r') as f:
            for line in f:
                seen.add(line.rstrip('\n'))

    # Append only new lines
    with open(out_path, 'a') as outf:
        for line in matches.splitlines():
            if line not in seen:
                outf.write(line + "\n")
                seen.add(line)  # update set so we don’t repeat within this run

if __name__ == "__main__":
    main()
