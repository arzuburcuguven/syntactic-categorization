#!/usr/bin/env python3
"""
Dump each Tregex match to text files.
"""

import os
import argparse
import subprocess
import re
from pathlib import Path

def load_patterns(category_name: str):
    """
    Read txt_files/tregex_patterns_<category_name>.txt and return a dict of pattern_name -> tregex string.
    """
    path = os.path.join("txt_files", f"tregex_patterns_{category_name}.txt")
    patterns = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            name, pat = line.split(':', 1)
            patterns[name.strip()] = pat.strip()
    return patterns


def save_captures(parsed_dir: str, category_name: str):
    """
    For each .parsed file in parsed_dir, run each Tregex pattern and
    save matched subtrees into captures/<category_name>/<pattern>_<file>.txt
    """
    parsed_dir = Path(parsed_dir)
    corpus_name = parsed_dir.stem
    patterns = load_patterns(category_name)

    script_dir = Path(__file__).resolve().parent       
    project_root = script_dir.parent.parent             

    out_dir = project_root / "data" / "captures" / category_name
    out_dir.mkdir(parents=True, exist_ok=True)  
    
    out_path = os.path.join(out_dir, f"{corpus_name}_{category_name}.txt")
    if os.path.exists(out_path):
        os.remove(out_path)

    for parsed_file in sorted(os.listdir(parsed_dir)):
        if not parsed_file.endswith(".parsed"):
            continue
        full_path = os.path.join(parsed_dir, parsed_file)
        base = os.path.splitext(parsed_file)[0]

        for name, pattern in patterns.items():
            # run tregex.sh with -t & -o to print matched subtrees
            cmd = f"./tregex.sh {pattern} '{full_path}' -t -o"
            matches = subprocess.getoutput(cmd)

            # append, don’t overwrite
            with open(out_path, "a") as outf:
                for line in matches.splitlines():
                    tokens = line.split()


                    # keep only lines where every token is form word/POS and there’s more than one
                    if len(tokens) > 1 and all('/' in tok for tok in tokens):
                        line = re.sub(r'\/\.', '', line)
                        clean = re.sub(r'(\w+)\/[\w$]*', r'\1', line)
                        outf.write(clean + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
    )
    parser.add_argument(
        "parsed",
    )
    parser.add_argument(
        "category",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    save_captures(args.parsed, args.category)


if __name__ == "__main__":
    main()
