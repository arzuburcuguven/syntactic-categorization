import os
import re
import sys

ages = [
    "0_12", "12_24", "24_36", "36_48", "48_60",
    "60_72", "72_84", "84_96", "96_108", "108_120", "120_192"
]
extras = [
    "bnc_spoken",
    "open_subtitles",
    "simple_wiki",
    "switchboard",
    "TD"
]

parsed_path     = "/users/argy/workspace/extractor/data/parsed"
stats_base_path = "/users/argy/workspace/extractor/data/stats"

def generate_commands(script_path):
    script_name = os.path.basename(script_path)
    match = re.search(r'^[ab]?\d+_?([a-z_]+)\.py$', script_name)
    if not match:
        print(f"Invalid script name format: {script_name}")
        return

    category      = match.group(1)
    output_folder = os.path.join(stats_base_path, category)
    output_suffix = f"_{category}.txt"
    os.makedirs(output_folder, exist_ok=True)

    # age‐based files
    for age in ages:
        inp = os.path.join(parsed_path, f"CHILDES/age_{age}.parsed")
        out = os.path.join(output_folder, f"age_{age}{output_suffix}")
        print(f"python {script_path} {inp} {out}")

    # extra corpora
    for name in extras:
        inp = os.path.join(parsed_path, f"{name}/{name}.parsed")
        out = os.path.join(output_folder, f"{name}{output_suffix}")
        print(f"python {script_path} {inp} {out}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python command_maker.py <script_path>")
        sys.exit(1)
    generate_commands(sys.argv[1])
