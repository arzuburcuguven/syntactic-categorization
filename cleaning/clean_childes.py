from typing import List, Optional
from pathlib import Path
import os
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
import re
import argparse
from collections import defaultdict
from dict import w2string
import string

root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_folder = os.path.join(root_folder, "data/raw/CHILDES")
output_folder = os.path.join(root_folder, "data/clean/CHILDES")

ignore_regex = re.compile(r'(�|www|xxx|yyy|\[=! singing\])')

file_metadata = []

# === Filler Words ===
FILLERS = set([
    "o", "mhm", "yeah", "huh", "hm", "um", "ah", "oh", "aha", "uh", "whoops", "whoop", "wow",
    "ouch", "yay", "oop", "oops", "aw", "awoh", "kay", "whoa", "ugh", "oy", "mm", "hey",
    "yum", "whee", "ssh", "moo", "eh", "voom", "boom", "gib", "zoom", "da", "ba", "bonk"
])

""" Filtering Functions """
def extract_age_from_file(file_path: Path) -> Optional[int]:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("@ID:") and ("Target_Child" in line or "Child" in line):
                match = re.search(r'eng\|[^|]*\|[^|]*\|(\d+);(\d*)', line)
                if match:
                    years = int(match.group(1))
                    month_str = match.group(2)
                    months = int(month_str) if (month_str := match.group(2)) and month_str.isdigit() else 0
                    return years * 12 + months
    return None


def extract_activity_types(file_path: Path) -> List[str]:
    activities = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("@Types:"):
                activities = line.strip().split(":")[1].strip().split(", ")
                break
    return activities


def find_cha_files(data_folder: Path, min_age: int, max_age: int) -> List:
    selected_files = []
    for dirpath, _, filenames in os.walk(data_folder):
        for file in filenames:
            if file.endswith(".cha"):
                file_path = os.path.join(dirpath, file)
                child_age_months = extract_age_from_file(file_path)
                if child_age_months is not None and min_age <= child_age_months < max_age:
                    selected_files.append(file_path)
    print(f"Found {len(selected_files)} files")
    return selected_files


def clean_redundant_patterns(line: str) -> str:
    # Remove repeated patterns like "zoom &zoom &zoom ..."
    line = re.sub(r'\b(\w+)(?:\s+&*\1){2,}', r'\1', line)
    # Remove pairs like "ba &ba"
    line = re.sub(r'\b(\w+)\s+&\1\b', r'\1', line)
    return line


def remove_fillers_inline(text: str) -> str:
    tokens = text.split()
    tokens = [t for t in tokens if t.strip(string.punctuation) not in FILLERS]
    return " ".join(tokens)


def is_only_filler_line(line: str) -> bool:
    tokens = [t.strip(string.punctuation) for t in line.split()]
    tokens = [t for t in tokens if t]
    return all(t in FILLERS for t in tokens)



def clean_line(line: str) -> Optional[str]:
    line = re.sub(r'\d+_\d+', '', line)
    line = re.sub(r'^\*\w+:\s*', '', line)

    if ignore_regex.search(line):
        return None

    line = line.lower()


    if re.match(r'^[\s\-\.\?\!\,\/\\]+$', line):
        return None
    # remove annotations: [=! mock]
    line = re.sub(r'\[=!\s.*?\]', "", line)
    line = re.sub(r'\[:!\s.*?\]', "", line)
    line = re.sub(r'\(=!\s.*?\)', "", line)
    line = re.sub(r'\(:!\s.*?\)', "", line)
    # remove annotations: &= laughs
    line = re.sub(r'&=\s[a-z]*', "", line)
    # remove annotations: [+ sng]
    line = re.sub(r'\[+\s.*?\]', "", line)
    # daddy [: dad] -> dad
    line = re.sub(r'\w+\s+\[(?::|=)\s(.*?)\]', r'\1', line)
    line = re.sub(r'\w+\s+\((?::|=)\s(.*?)\)', r'\1', line)
    line = re.sub(r'\w+\s+\<(?::|=)\s(.*?)\>', r'\1', line)
    line = re.sub(r'\w+\s+\{(?::|=)\s(.*?)\}', r'\1', line)

    #remove 1 or 1 =
    line = re.sub(r'\b\d+\s*[\.\=\!]*\b', '', line)
    line = re.sub(r'ss-sā-ss-amsam\s+ss\s+\/\.', '', line)
    line = re.sub(r'ee\s+ee\s+aa\s+\/\.', '', line)
    #remove annotations of &=voc, (3.) and x@x
    line = re.sub(r'\&=[^\s]+|\w+@\w+|\(\d+\.\)', '', line)
    line = re.sub(r'-um\b|\bee\b|~y', '', line)
    #remove &-uh
    line = re.sub(r'&-\w*|\&y', '', line)
    # remove symbols and some punctuation
    line = re.sub(r'[\x15‡↫→@↑~&:\^]', '', line)
    #remove sentence initial punctuation
    line = re.sub(r'^\W+', '', line)
    #remove brackets
    line = re.sub(r'[\[\]\<\>\{\}\/\\\(\)]', '', line)
    #two or more spaces to single
    line = re.sub(r'\s{2,}', ' ', line)

    # Clean reduplications
    line = clean_redundant_patterns(line)

    # collapse “..”, “??”, “!!?”, etc. → one punctuation
    line = re.sub(r'([.?!]){2,}', r'\1', line)
    line = line.strip()
    if not line:
        return None

    # Apply w2string mappings
    words = [w2string.get(word, word) for word in line.split()]
    line = " ".join(words).replace('+', ' ').replace('_', ' ')

    if len(line.split()) < 2:
        return None

    return line


def process_chat_files(file_path: Path, collected_lines: List[str]):
    activities = extract_activity_types(file_path)
    filename = os.path.basename(file_path)
    child_age_months = extract_age_from_file(file_path)

    activity_sentence_counts = defaultdict(int)

    with open(file_path, "r", encoding="utf-8") as file:
        recording = False
        for line in file:
            line = line.strip()
            if line.startswith("@Begin"):
                recording = True
                continue
            if not recording or line.startswith(("@", "%")):
                continue
            cleaned = clean_line(line)
            if not cleaned:
                continue
            for sent in sent_tokenize(cleaned):
                sent = remove_fillers_inline(sent)
                if is_only_filler_line(sent) or len(sent.split()) < 2:
                    continue
                collected_lines.append(sent)
                for act in activities:
                    activity_sentence_counts[act] += 1

    for act, sent_count in activity_sentence_counts.items():
        file_metadata.append({
            "filename": filename,
            "act_type": act,
            "sent_count": sent_count,
            "age_months": child_age_months
        })

    print(f"Processed: {file_path}")


""" Main Execution """
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter CHILDES .cha files based on child age.")
    parser.add_argument("min_age", type=int, help="Minimum child age in months")
    parser.add_argument("max_age", type=int, help="Maximum child age in months")
    args = parser.parse_args()

    filtered_files = find_cha_files(data_folder, args.min_age, args.max_age)
    print(f"Found {len(filtered_files)} files for age range {args.min_age}-{args.max_age} months.")
    print(filtered_files)

    collected_lines = []
    for file_path in filtered_files:
        process_chat_files(file_path, collected_lines)

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"age_{args.min_age}_{args.max_age}.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(collected_lines))

    print(f"Processed data saved to {output_file}")

    """ Generate Metadata Output """
    metadata_output = os.path.join(output_folder, f"metadata_{args.min_age}_{args.max_age}.csv")
    df_metadata = pd.DataFrame(file_metadata)
    df_metadata.to_csv(metadata_output, index=False)

    print(f"Metadata saved to {metadata_output}")
