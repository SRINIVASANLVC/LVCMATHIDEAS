import itertools
import pandas as pd

# Define vowel vectors
vowel_vectors = {'a': (0, -1, 0), 'i': (-1, 0, 0), 'u': (0, 0, -1)}

# Define phonetic merger rules (right-to-left)
merger_rules = {
    ('a','u'): 'o', ('a','i'): 'e',
    ('u','a'): 'wa', ('u','i'): 'wi', ('u','e'): 'we', ('u','o'): 'wo',
    ('i','a'): 'ya', ('i','u'): 'yu', ('i','e'): 'ye', ('i','o'): 'yo',
    ('a','a'): 'A', ('i','i'): 'I', ('u','u'): 'U', ('e','e'): 'E', ('o','o'): 'O'
}

# Generate all destination coordinates in 2x2x2 cube (excluding origin)
coordinates = [(x, y, z) for x in range(3) for y in range(3) for z in range(3) if (x, y, z) != (0, 0, 0)]

# Function to generate all valid paths to a destination
def generate_paths(dest):
    paths = []
    for a_count in range(dest[1]+1):
        for i_count in range(dest[0]+1):
            for u_count in range(dest[2]+1):
                total = [0, 0, 0]
                total[0] += i_count * vowel_vectors['i'][0]
                total[1] += a_count * vowel_vectors['a'][1]
                total[2] += u_count * vowel_vectors['u'][2]
                if tuple(total) == (-dest[0], -dest[1], -dest[2]):
                    sequence = ['a'] * a_count + ['i'] * i_count + ['u'] * u_count
                    for perm in set(itertools.permutations(sequence)):
                        paths.append(perm)
    return paths

# Function to apply phonetic merger rules right-to-left
def apply_merger(path):
    merged = list(path)
    i = len(merged) - 2
    while i >= 0:
        pair = (merged[i], merged[i+1])
        if pair in merger_rules:
            merged[i:i+2] = [merger_rules[pair]]
        i -= 1
    return ''.join(merged)

# Collect results
results = []
global_path_id = 1
for idx, coord in enumerate(coordinates, start=1):
    paths = generate_paths(coord)
    for path in paths:
        merged = apply_merger(path)
        results.append({
            'Valid Path': ''.join(path),
            'Path Number': global_path_id,
            'Destination Coordinate': coord,
            'Destination Index': idx,
            'After Phonetic Merger': merged
        })
        global_path_id += 1

# Create DataFrame and save to CSV
df = pd.DataFrame(results)
df.to_csv('phonetic_output/vowel_vector_paths_table.csv', index=False)
# print(df.head(20))
# print(df.to_string(index=False))