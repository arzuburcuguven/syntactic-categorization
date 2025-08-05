#!/usr/bin/env python3
import re
import nltk
from nltk.tokenize import sent_tokenize
import argparse

def clean_text(text):
    text = re.sub(r"\*\*.*?\*\*:\s*", "", text)
    text = re.sub(r"<\|.*?\|>", "", text)
    text = text.replace('"', "").replace("“", "").replace("”", "")
    text = text.replace(r"\n\n", " ")
    text = re.sub(r"\*.*?\*", "", text)
    text = re.sub(r"---+", "", text)
    text = re.sub(r"___+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    args = p.parse_args()

    raw = open(args.input, encoding="utf-8").read()
    cleaned = clean_text(raw)

    sentences = sent_tokenize(cleaned)

    with open(args.output, "w", encoding="utf-8") as out:
        for s in sentences:
            out.write(s + "\n")

if __name__ == "__main__":
    main()