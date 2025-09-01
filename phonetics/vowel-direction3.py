import itertools
import pandas as pd

# Define vowel vectors
vowel_vectors = {
    'a': (0, -1, 0),
    'i': (-1, 0, 0),
    'u': (0, 0, -1)
}

# Define phonetic merger rules
merger_rules = {
    ('a', 'a'): 'A', ('i', 'i'): 'I', ('u', 'u'): 'U', ('e', 'e'): 'E', ('o', 'o'): 'O',
    ('a', 'u'): 'o', ('a', 'i'): 'e',
    ('u', 'a'): 'wa', ('u', 'i'): 'wi', ('u', 'e'): 'we', ('u', 'o'): 'wo',
    ('i', 'a'): 'ya', ('i', 'u'): 'yu', ('i', 'e'): 'ye', ('i', 'o'): 'yo'    
}

# Generate all destination coordinates in a 2x2x2 cube (excluding origin)
destinations = [(x, y, z) for x in range(3) for y in range(3) for z in range(3) if (x, y, z) != (0, 0, 0)]

# Function to add vectors
def add_vectors(vectors):
    x, y, z = 0, 0, 0
    for v in vectors:
        dx, dy, dz = vowel_vectors[v]
        x += dx
        y += dy
        z += dz
    return (-x, -y, -z)

# Recursive right-to-left phonetic merger
def merge_phonetics(seq):
    while len(seq) > 1:
        merged = False
        for i in range(len(seq) - 1, 0, -1):
            pair = (seq[i - 1], seq[i])
            if pair in merger_rules:
                seq[i - 1:i + 1] = [merger_rules[pair]]
                merged = True
                break
        if not merged:
            break
    return ''.join(seq)

# Generate all valid paths and apply mergers
results = []
global_path_id = 1
for idx, dest in enumerate(destinations, start=1):
    x, y, z = dest
    path_elements = ['a'] * y + ['i'] * x + ['u'] * z
    permutations = set(itertools.permutations(path_elements))
    valid_paths = [p for p in permutations if add_vectors(p) == dest]
    for path in valid_paths:
        merged = merge_phonetics(list(path))
        results.append({
            'Valid Path': ''.join(path),
            'Path Number': global_path_id,
            'Destination Coordinate': dest,
            'Destination Index': idx,
            'After Phonetic Merger': merged
        })
        global_path_id += 1

# Save to phonetic_output folder
import os
os.makedirs('phonetic_output', exist_ok=True)
df = pd.DataFrame(results)
df.to_csv('phonetic_output/phonetic_output.csv', index=False)
print(df.to_string(index=False))