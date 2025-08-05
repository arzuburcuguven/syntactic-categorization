import hashlib

def hash_line(line):
    return hashlib.md5(line.strip().encode('utf-8')).hexdigest()

# Hash test lines (only those > 4 tokens)
test_hashes = set()
with open("/Users/argy/workspace/extractor/data/clean/test/childes_test.txt", "r") as f:
    for line in f:
        stripped = line.strip()
        if len(stripped.split()) > 5:
            test_hashes.add(hash_line(stripped))

# Filter training data
with open("/Users/argy/workspace/extractor/data/captures/compiled/clean/simple_to_complex_complex.txt", "r") as fin, open("/Users/argy/workspace/extractor/data/captures/compiled/clean/simple_to_complex_complex_clean.txt.txt", "w") as fout:
    for line in fin:
        if hash_line(line.strip()) not in test_hashes:
            fout.write(line)
