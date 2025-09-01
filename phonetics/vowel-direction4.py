import itertools
import pandas as pd
from collections import defaultdict
import os

# Define vowel vectors
vowel_vectors = {
    'a': (0, -1, 0),
    'i': (-1, 0, 0),
    'u': (0, 0, -1)
}

# Define phonetic merger rules
merger_rules = {
    ('a', 'u'): 'o', ('a', 'i'): 'e',
    ('u', 'a'): 'wa', ('u', 'i'): 'wi', ('u', 'e'): 'we', ('u', 'o'): 'wo',
    ('i', 'a'): 'ya', ('i', 'u'): 'yu', ('i', 'e'): 'ye', ('i', 'o'): 'yo',
    ('a', 'a'): 'A', ('i', 'i'): 'I', ('u', 'u'): 'U',
    ('e', 'e'): 'E', ('o', 'o'): 'O'
}

# Generate all destination coordinates in 2x2x2 cube excluding origin
destinations = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)
                if (x, y, z) != (0, 0, 0)]

elimination_set = {
    'ayiwu', 'yuwai', 'ayuwa', 'ayiwuwa', 'eou', 'ioua', 'ayiwuo',
    'ayuwai', 'ayiuw', 'ayuwu', 'ayiuwu', 'ayiwuwa', 'yuwaiwa'
}

# Function to generate all valid paths to a destination
def generate_paths(dest):
    dx, dy, dz = dest
    path_counts = {'a': dy, 'i': dx, 'u': dz}
    elements = sum([[v]*path_counts[v] for v in 'aiu'], [])
    return set(itertools.permutations(elements))

# Recursive merger engine (right-to-left)
def recursive_merge(seq):
    if len(seq) == 1:
        return [seq[0]]
    results = set()
    for i in range(len(seq) - 1):
        left = seq[:i]
        pair = (seq[i], seq[i+1])
        if pair in merger_rules:
            merged = merger_rules[pair]
            new_seq = left + [merged] + seq[i+2:]
            for r in recursive_merge(new_seq):
                results.add(r)
    if not results:
        results.add(''.join(seq))
    return results

# Collect results
rows = []
global_path_id = 1
for idx, dest in enumerate(destinations, start=1):
    valid_paths = generate_paths(dest)
    for path in valid_paths:
        fusions = recursive_merge(list(path))
        rows.append({
            'Valid Path': ''.join(path),
            'Path Number': global_path_id,
            'Destination Coordinate': dest,
            'Destination Index': idx,
            'Fusion Lineage(s)': ', '.join(sorted(fusions)),
            'Final Glyph(s)': ', '.join(sorted(set(fusions)))
        })
        global_path_id += 1

# Clean the "Final Glyph(s)" column
def clean_glyphs(glyphs):
    glyph_list = [g.strip() for g in str(glyphs).split(',')]
    cleaned = [g for g in glyph_list if g not in elimination_set]
    return ', '.join(cleaned) if cleaned else '❌ All glyphs eliminated'


# Save to phonetic_output folder
os.makedirs('phonetic_output', exist_ok=True)
df = pd.DataFrame(rows)
df['Final Glyph(s)'] = df['Final Glyph(s)'].apply(clean_glyphs)
df.to_csv('phonetic_output/phonetic_output.csv', index=False)
print(df.to_string(index=False))