#!/usr/bin/env python3
import os
import glob
import json
import random
import argparse

# --- CONFIG ---
# relative to this script: data/captures/<category>/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'captures'))
AGG_DIR = os.path.join(BASE_DIR, 'agg')
COMP_DIR = os.path.join(BASE_DIR, 'compiled')

CATEGORIES = [
    'aux', 'complexq', 'coord', 'embedded', 'frag', 'negation_simple',
    'pos_adv_categories', 'pp', 'prt_to', 'questions', 'simple_categories',
    'tense', 'to', 'relative'
]

# hard-coded groupings
GROUPINGS = {
    'simple_to_complex': {
        'simple': [
            'simple_categories','pos_adv_categories','pp',
            'prt_to','aux','tense','negation_simple'
        ],
        'complex': [
            'complexq','coord','embedded','frag','questions','to','relative'
        ]
    },
    'syntactic_stages': {
        'stage1': [
            'simple_categories','pos_adv_categories','pp',
            'prt_to','aux','tense','negation_simple'
        ],
        'stage2': ['questions','complexq'],
        'stage3': ['coord','embedded','to','frag','relative']
    }
}

# --- FUNCTIONS ---
def aggregate_all(categories, src_root, agg_root):
    os.makedirs(agg_root, exist_ok=True)
    for cat in categories:
        src = os.path.join(src_root, cat)
        out = os.path.join(agg_root, f"{cat}.txt")
        lines = []
        for fn in glob.glob(os.path.join(src, '*.txt')):
            with open(fn, 'r') as f:
                lines.extend(f.readlines())
        random.shuffle(lines)
        with open(out, 'w') as f:
            f.writelines(lines)
        print(f"[agg] {cat}: {len(lines)} lines → {out}")

def compile_grouping(name, grouping, agg_root, comp_root, shuffle_within=False):
    os.makedirs(comp_root, exist_ok=True)
    for part, cats in grouping.items():
        files = [os.path.join(agg_root, f"{cat}.txt") for cat in cats]
        lines = []
        for fp in files:
            with open(fp, 'r') as f:
                lines.extend(f.readlines())
        if shuffle_within:
            random.shuffle(lines)
        out = os.path.join(comp_root, f"{name}_{part}.txt")
        with open(out, 'w') as f:
            f.writelines(lines)
        print(f"[compile] {name}/{part}: {len(lines)} lines → {out}")

# --- MAIN ---
if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Step1: aggregate category txts; "
                    "Step2: compile them into ordered/shuffled corpora"
    )
    p.add_argument(
        '--skip-agg', action='store_true',
        help="only run compilation (skip aggregation)"
    )
    p.add_argument(
        '--grouping', choices=list(GROUPINGS)+['custom'],
        help="which predefined grouping to use, or 'custom'"
    )
    p.add_argument(
        '--group-file',
        help="JSON file defining {part: [category,...]} (required if --grouping custom)"
    )
    p.add_argument(
        '--shuffle-within', action='store_true',
        help="shuffle lines inside each part after concatenation"
    )
    args = p.parse_args()

    if not args.skip_agg:
        aggregate_all(CATEGORIES, BASE_DIR, AGG_DIR)

    if args.grouping:
        if args.grouping == 'custom':
            if not args.group_file:
                p.error("--group-file is required when --grouping custom")
            with open(args.group_file) as f:
                grouping = json.load(f)
            name = os.path.splitext(os.path.basename(args.group_file))[0]
        else:
            grouping = GROUPINGS[args.grouping]
            name = args.grouping

        compile_grouping(name, grouping, AGG_DIR, COMP_DIR,
                        shuffle_within=args.shuffle_within)
    else:
        print("Done. (no grouping requested)")
