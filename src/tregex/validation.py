import random
from pathlib import Path

random.seed(1337)

def sample_validation_set(input_path, output_path, target_token_count):
    total_tokens = 0
    selected_lines = []

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        random.shuffle(lines)

    for line in lines:
        tokens = line.split()
        total_tokens += len(tokens)
        selected_lines.append(line)
        if total_tokens >= target_token_count:
            break

    with open(output_path, "w") as f:
        f.write("\n".join(selected_lines))

    print(f"{output_path}: {len(selected_lines)} lines, {total_tokens} tokens")

# Paths
base_dir = Path("/Users/argy/workspace/extractor/data/captures/compiled/clean")
output_dir = Path("/Users/argy/workspace/extractor/data/captures/compiled/clean/valid_sets")
output_dir.mkdir(exist_ok=True)

files = {
    "simple": "syntactic_stages_stage_s.txt",
    "question": "syntactic_stages_stage_q.txt",
    "complex": "syntactic_stages_stage_c.txt"
}

for name, fname in files.items():
    in_path = base_dir / fname
    out_path = output_dir / f"valid_{name}.txt"
    sample_validation_set(in_path, out_path, target_token_count=333_000)
