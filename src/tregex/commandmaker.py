import os
import re
import sys
import argparse

# Define age ranges and extra corpora
ages = [
    "0_12", "12_24", "24_36", "36_48", "48_60",
    "60_72", "72_84", "84_96", "96_108", "108_120", "120_192"
]
extras = [
    "bnc_spoken",
    "open_subtitles",
    "simple_wiki",
    "switchboard",
    "gutenberg"
]

# Paths
parsed_path     = "/users/argy/workspace/extractor/data/parsed"
stats_base_path = "/users/argy/workspace/extractor/data/stats"


def generate_count_commands(script_path, category):
    out_folder = os.path.join(stats_base_path, category)
    suffix = f"_{category}.txt"
    os.makedirs(out_folder, exist_ok=True)

    # age-based files
    for age in ages:
        inp = os.path.join(parsed_path, f"CHILDES/age_{age}.parsed")
        out = os.path.join(out_folder, f"age_{age}{suffix}")
        print(f"python {script_path} {inp} {out}")

    # extra corpora
    for name in extras:
        inp = os.path.join(parsed_path, f"{name}/{name}.parsed")
        out = os.path.join(out_folder, f"{name}{suffix}")
        print(f"python {script_path} {inp} {out}")


def generate_save_commands(category):
    # Save mode: uses save_captures.py on directories, not individual files
    # Ensure output directory exists
    out_folder = os.path.join(stats_base_path, category)
    os.makedirs(out_folder, exist_ok=True)

    # CHILDES directory
    childes_dir = os.path.join(parsed_path, "CHILDES")
    print(f"python save_captures.py {childes_dir} {category}")

    # extra corpora directories
    for name in extras:
        corp_dir = os.path.join(parsed_path, name)
        print(f"python save_captures.py {corp_dir} {category}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate shell commands for counting or saving captures"
    )
    subparsers = parser.add_subparsers(dest='mode', required=True)

    # Count sub-command
    count_parser = subparsers.add_parser('count', help='Generate count commands')
    count_parser.add_argument(
        'script_path',
        help='Path to the analysis script (e.g. a01_mycategory.py)'
    )

    # Save sub-command
    save_parser = subparsers.add_parser('save', help='Generate save_captures commands')
    save_parser.add_argument(
        'category',
        help='Category name to use for save commands'
    )

    args = parser.parse_args()

    if args.mode == 'count':
        script_name = os.path.basename(args.script_path)
        match = re.search(r'^cat\d+_?([a-zA-Z_]+)\.py$', script_name)
        if not match:
            print(f"Invalid script name format: {script_name}")
            sys.exit(1)
        category = match.group(1)
        generate_count_commands(args.script_path, category)

    elif args.mode == 'save':
        generate_save_commands(args.category)


if __name__ == "__main__":
    main()
