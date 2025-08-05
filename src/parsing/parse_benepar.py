"""Main module."""
import benepar
import spacy
import os
import nltk
from tqdm import tqdm
import argparse

# Download benepar model
benepar.download('benepar_en3')

# Load spacy tokenizer
nlp = spacy.load('en_core_web_lg')

# Add benepar parser if not already added
if "benepar" not in nlp.pipe_names:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

# Function to parse a text file
def parse_text_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        text = infile.read().split("\n")

    parsed_sentences = []
    error_lines = []

    for line in tqdm(text, desc=f"Parsing {input_path}"):
        if line.strip():
            try:
                doc = nlp(line)
                parsed_sentences.extend(sent._.parse_string for sent in doc.sents)
            except AssertionError:
                error_lines.append(line)
            except Exception as e:
                # Catch any other unexpected errors
                print(f"Unexpected error: {e} | Line: {line}")
                error_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(parsed_sentences))

    # Save problematic lines
    if error_lines:
        error_log = output_path.replace(".parsed", ".errors")
        with open(error_log, "w", encoding="utf-8") as errfile:
            errfile.write("\n".join(error_lines))
        print(f"\n⚠️  {len(error_lines)} problematic lines logged to {error_log}")

# Define input and output folders
input_folder = "../../data/TD"
output_folder = "../../data/PARSED"
os.makedirs(output_folder, exist_ok=True)

def main():
    
# Process each text file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace(".txt", ".parsed"))
        parse_text_file(input_file, output_file)

if __name__ == "__main__":
    main()