# Extractor
Scripts to clean, parse, extract syntactic patterns, compile them into corpora and visualize stats.

## Installation

```sh
pip install -r requirements.txt

## Usage

Clean childes: 
python src/cleaning/clean_childes.py data/raw/childes data/raw/clean_childes

Parse: 
python src/parsing/parse_with_berkeley.py --in data/raw/clean_childes --out data/parsed

Extract stats:
python src/tregex/extract_stats.py --parsed data/parsed --patterns src/tregex/patterns --out data/stats

Save captures:
python src/tregex/save_captures.py --trees data/parsed --patterns src/tregex/patterns --out data/captures

Compile corpora:
python src/tregex/compile_corpora.py --in data/captures --out data/corpora

Organize stats:
python src/stats/organize_stats.py --stats_dir data/stats --out data/stats/master.csv

Visualize: 
python src/stats/visualize_stats.py --csv data/stats/master.csv --out outputs/figures