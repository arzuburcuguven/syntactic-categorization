#!/usr/bin/env python3
"""
Dump each Tregex match to text files.
"""

import os
import argparse
import subprocess
import re
from pathlib import Path

PREDECESSORS = {
    'relative':   [],
    'coord':  ['relative'],
    'embedded':  ['relative', 'coord'],
    'to':   ['relative', 'embedded', 'coord'],
    'questions':    ['relative', 'to', 'coord', 'embedded'],
    # the “simple” categories aren’t in this dict—you’ll run them normally
}


def load_patterns(category_name: str):
    """
    Read txt_files/tregex_patterns_<category_name>.txt and return a dict of pattern_name -> tregex string.
    """
    path = os.path.join("txt_files", f"{category_name}.txt")
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
    parsed_dir = Path(parsed_dir)
    corpus_name = parsed_dir.stem
    patterns = load_patterns(category_name)

    script_dir = Path(__file__).resolve().parent       
    project_root = script_dir.parent.parent             

    out_dir = project_root / "data" / "captures" / "clean_q" / category_name
    out_dir.mkdir(parents=True, exist_ok=True)  
    
    out_path = os.path.join(out_dir, f"{corpus_name}_{category_name}.txt")
    if os.path.exists(out_path):
        os.remove(out_path)

    # Load previously captured lines from predecessors
    pred_lines = set()
    for pred in PREDECESSORS.get(category_name, []):
        pred_path = project_root / "data" / "captures" / pred / f"{corpus_name}_{pred}.txt"
        if pred_path.exists():
            pred_lines |= set(pred_path.read_text().splitlines())

    # Deduplicate only for selected categories
    dedup_categories = {'to', 'relative', 'questions', 'coord', 'embedded'}
    seen_lines = set() if category_name in dedup_categories else None

    for parsed_file in sorted(os.listdir(parsed_dir)):
        if not parsed_file.endswith(".parsed"):
            continue
        full_path = os.path.join(parsed_dir, parsed_file)

        for name, pattern in patterns.items():
            cmd = f"./tregex.sh {pattern} '{full_path}' -w -t -o"
            matches = subprocess.getoutput(cmd)

            for line in matches.splitlines():
                if line.startswith("(") and any(sym in line for sym in ['[', ']', '|', '<', '>']):
                    continue

                tokens = line.split()
                if len(tokens) <= 1 or any('/' not in tok for tok in tokens):
                    continue

                # Remove tags and reconstruct sentence
                words = [tok.rsplit('/', 1)[0] for tok in tokens if '/' in tok and tok.rsplit('/', 1)[0]]
                clean = ''
                for w in words:
                    if w in {'.', ',', '!', '?', ';', ':', ')', ']', '}', '”', "''"}:
                        clean = clean.rstrip() + w
                    elif w in {"'s", "'ve", "'re", "'ll", "'d", "n't", "’s", "’re", "’ll", "’d", "n’t"}:
                        clean = clean.rstrip() + w
                    elif w in {'(', '[', '{', '“', "``"}:
                        clean += w
                    else:
                        clean += ' ' + w
                clean = clean.strip()
                norm = ' '.join(clean.split())

                if not norm or norm in pred_lines or (seen_lines is not None and norm in seen_lines):
                    continue
                if seen_lines is not None:
                    seen_lines.add(norm)
                with open(out_path, "a") as outf:
                    outf.write(norm + "\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("parsed")
    parser.add_argument("category")
    return parser.parse_args()


def main():
    args = parse_args()
    save_captures(args.parsed, args.category)


if __name__ == "__main__":
    main()
