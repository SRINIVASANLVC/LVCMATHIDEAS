import itertools
import pandas as pd

# Vowel vectors
vowel_vectors = {
    'a': (0, -1, 0),
    'i': (-1, 0, 0),
    'u': (0, 0, -1)
}

# Destination coordinates (excluding origin)
destinations = [
    (1, 0, 0),  # i
    (0, 1, 0),  # a
    (0, 0, 1),  # u
    (1, 1, 0),  # i+a
    (1, 0, 1),  # i+u
    (0, 1, 1),  # a+u
    (1, 1, 1)   # i+a+u
]

# Merger rules (right-to-left)
merger_rules = {
    ('a','u'): 'o', ('a','i'): 'e', ('u','a'): 'wa', ('u','i'): 'wi',
    ('u','e'): 'we', ('u','o'): 'wo', ('i','a'): 'ya', ('i','u'): 'yu',
    ('i','e'): 'ye', ('i','o'): 'yo', ('a','a'): 'A', ('i','i'): 'I',
    ('u','u'): 'U', ('e','e'): 'E', ('o','o'): 'O'
}

# Vector sum function
def vector_sum(path):
    x, y, z = 0, 0, 0
    for v in path:
        dx, dy, dz = vowel_vectors[v]
        x += dx
        y += dy
        z += dz
    return (-x, -y, -z)  # negate to get positive coordinates

# Right-to-left recursive merger
def right_merge(seq):
    while len(seq) > 1:
        right = seq.pop()
        left = seq.pop()
        merged = merger_rules.get((left, right), left + right)
        seq.append(merged)
    return seq[0]

# Generate paths
rows = []
global_path_id = 1
for dest_index, coord in enumerate(destinations, start=1):
    dx, dy, dz = coord
    base = ['i'] * dx + ['a'] * dy + ['u'] * dz
    perms = sorted(set(itertools.permutations(base)))
    for path_num, path in enumerate(perms, start=1):
        if vector_sum(path) != coord:
            continue
        merged = right_merge(list(path))
        rows.append({
            'Valid Path': ''.join(path),
            'Path Number': global_path_id,
            'Destination Coordinate': coord,
            'Destination Index': dest_index,
            'After Phonetic Merger': merged
        })
        global_path_id += 1

# Display table
df = pd.DataFrame(rows)
print(df.to_string(index=False))