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

def extract_age_group(filename):
    match = re.search(r'(\d+_\d+)', filename)
    return match.group(1) if match else "unknown"

def save_captures(parsed_dir: str, category_name: str):
    parsed_dir = Path(parsed_dir)
    patterns = load_patterns(category_name)

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent

    # 1) For each parsed file & each pattern
    for parsed_file in sorted(os.listdir(parsed_dir)):
        print(parsed_file)
        if not parsed_file.endswith(".parsed"):
            print("not found!")
            continue

        age_group = extract_age_group(parsed_file)
        full_path = os.path.join(parsed_dir, parsed_file)

        out_dir = project_root / "data" / "captures" / "aochildes" / age_group 
        out_dir.mkdir(parents=True, exist_ok=True)

        out_path = os.path.join(out_dir, f"{parsed_file.replace('.parsed', '')}_{category_name}.txt")
        if os.path.exists(out_path):
            os.remove(out_path)

        pred_lines = set()
        for pred in PREDECESSORS.get(category_name, []):
            pred_path = project_root / "data" / "captures" / "aochildes" / age_group / pred / f"{parsed_file.replace('.parsed', '')}_{pred}.txt"
            if pred_path.exists():
                pred_lines |= set(pred_path.read_text().splitlines())

        for name, pattern in patterns.items():
            cmd = f"./tregex.sh {pattern} '{full_path}' -w -t -o"
            matches = subprocess.getoutput(cmd)

            for line in matches.splitlines():
                tokens = line.split()
                if len(tokens) <= 1 or any('/' not in tok for tok in tokens):
                    continue

                clean = re.sub(
                    r'(?:\/-?(?:LRB|RRB|LSB|RSB)-?'
                    r'|\/\w+[$]?'
                    r'|-?\/(?:LRB|RRB|LSB|RSB)-?'
                    r'|\/[^\w\s])', # "-\LRB-", "-\RRB-"             # "\CD", "\XYZ", etc.
                    '',
                    line
                ).strip()
                if clean in pred_lines:
                    continue

                with open(out_path, "a") as outf:
                    outf.write(clean + "\n")

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
