#!/usr/bin/env python3
"""
Generate plots from master CSV.
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
from io import StringIO

raw = """[paste the entire data block here]"""

df = pd.read_csv("stats_by_category.csv", header=None, names=['corpus','category_name','category_count','total'])

def map_corpus(name):
    if name.startswith('age_'):
        return 'Childes'
    if name.startswith('bnc_spoken'):
        return 'BNC'
    if name.startswith('open_subtitles'):
        return 'OpenSubtitles'
    if name.startswith('simple_wiki'):
        return 'Simple Wiki'
    if name.startswith('switchboard'):
        return 'Switchboard'
    if name.startswith('TD'):
        return 'TinyDialogues'
    return None

df['corpus'] = df['corpus'].apply(map_corpus)
df["category_count"] = pd.to_numeric(df["category_count"], errors="coerce")
df["total"]          = pd.to_numeric(df["total"],          errors="coerce")

agg = (
    df
    .groupby('corpus', as_index=False)
    .agg(
        category_count_sum = ('category_count','sum'),
        total               = ('total','first')
    )
)

# 2) override Childes total
agg.loc[agg['corpus']=='Childes', 'total'] = 4849328


agg["pct_of_total"] = agg["category_count_sum"] / agg["total"] * 100

agg["pct_of_total"] = agg["pct_of_total"].round(2)

print(agg)

def visualize_stats(csv_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    # TODO: load CSV, create figures, save to output_dir
    pass


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, help="Master CSV path")
    p.add_argument("--out", required=True, help="Figures output dir")
    return p.parse_args()


def main():
    print(agg)
    args = parse_args()
    visualize_stats(args.csv, args.out)


if __name__ == "__main__":
    main()