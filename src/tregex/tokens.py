import nltk
from nltk.tokenize import word_tokenize

with open("/Users/argy/workspace/extractor/data/captures/compiled/clean/syntactic_stages_stage_c.txt", encoding="utf-8") as f:
    text = f.read()
tokens = word_tokenize(text)

print(len(tokens))

