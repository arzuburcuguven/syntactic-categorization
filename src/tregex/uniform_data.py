from itertools import cycle, islice
import random

def load_corpus(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Dummy datasets to illustrate (replace with your actual lists of examples)
simple_examples = load_corpus("/Users/argy/workspace/extractor/data/captures/compiled/clean/syntactic_stages_stage_s.txt")
question_examples = load_corpus("/Users/argy/workspace/extractor/data/captures/compiled/clean/syntactic_stages_stage_q.txt")
complex_examples = load_corpus("/Users/argy/workspace/extractor/data/captures/compiled/clean/syntactic_stages_stage_c.txt")

# Your target counts from previous calculation
target_examples_per_corpus = 2_794_662

def build_balanced_dataset(simple, question, complex_, target_count):
    # Create cycles for upsampling
    simple_cycle = cycle(simple)
    question_cycle = cycle(question)
    complex_cycle = cycle(complex_)

    balanced_dataset= []
    for _ in range(target_count):
        batch = [next(simple_cycle), next(simple_cycle),
                 next(question_cycle), next(question_cycle),
                 next(complex_cycle), next(complex_cycle)]
        random.shuffle(batch)  # optional, mixes the 6 samples
        balanced_dataset.extend(batch)
    
    return balanced_dataset

# Build the dataset
balanced_dataset = build_balanced_dataset(
    simple_examples,
    question_examples,
    complex_examples,
    target_examples_per_corpus // 2  # divide by 2 since we take 2 per corpus per batch
)

with open("/Users/argy/workspace/extractor/data/captures/compiled/clean/balanced_corpus.txt", "w", encoding="utf-8") as f:
    for example in balanced_dataset:
        f.write(example + "\n")

print(f"Total dataset size: {len(balanced_dataset)} examples")
print(f"Expected batches: {len(balanced_dataset) // 6}")

