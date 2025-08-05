import numpy as np
import random

simple = "/Users/argy/workspace/extractor/data/captures/compiled/clean/syntactic_stages_stage_s.txt"

complex = "/Users/argy/workspace/extractor/data/captures/compiled/clean/syntactic_stages_stage_cq.txt"

with open(simple, "r") as s:
    simple_c = s.readlines()

with open(complex, "r") as c:
    complex_c = c.readlines()

random.shuffle(simple_c)
random.shuffle(complex_c)

print(complex_c[0])

def interweave_function(simple, complex, total):
    s_idx = 0
    c_idx = 0
    final_lines = []

    for i in range(0,total):
        progress = i/(total - 1)
        if random.random() < 0.1696 + 0.8304 * progress and c_idx < len(complex_c):
            final_lines.append(complex[c_idx])
            c_idx += 1
            if c_idx % 1000 == 0:
                print("Complex")
        elif s_idx < len(simple_c): 
            final_lines.append(simple[s_idx])
            s_idx += 1
            if s_idx % 1000 == 0:
                print(f"{s_idx}")


    return final_lines

final_lines = interweave_function(simple_c, complex_c, len(simple_c) + len(complex_c))

output_file = "/Users/argy/workspace/extractor/data/captures/compiled/clean/prob_comp.txt"

with open(output_file, "w") as f:
    f.writelines(final_lines)

