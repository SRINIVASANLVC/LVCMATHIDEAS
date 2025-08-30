import decimal
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os
from sympy import primerange
import json


decimal.getcontext().prec = 100  # High precision for long decimal cycles

def get_group_size(prime):
    return len(str(prime))  # Group size equals number of digits in prime

def generate_triplets(prime):
    group_size = get_group_size(prime)
    triplets = []
    for i in range(1, prime):
        frac = decimal.Decimal(i) / decimal.Decimal(prime)
        digits = str(frac)[2:].ljust(group_size * 2, '0')
        first = digits[:group_size]
        next_ = digits[group_size:group_size * 2]
        triplets.append((f"{i}/{prime}", first, next_))
    return triplets

def build_chains(triplets):
    chains = []
    used = set()
    lookup = defaultdict(list)
    for triplet in triplets:
        lookup[triplet[1]].append(triplet)

    for triplet in triplets:
        if triplet in used:
            continue
        chain = [triplet]
        used.add(triplet)
        current = triplet
        while True:
            next_candidates = lookup.get(current[2], [])
            found = False
            for candidate in next_candidates:
                if candidate not in used:
                    chain.append(candidate)
                    used.add(candidate)
                    current = candidate
                    found = True
                    break
            if not found:
                break
        chains.append(chain)
    return chains

def resequence_chain(chain, start_fraction):
    start_index = next((i for i, t in enumerate(chain) if t[0] == start_fraction), 0)
    return chain[start_index:] + chain[:start_index]

def get_complement(fraction, prime):
    num = int(fraction.split('/')[0])
    return f"{prime - num}/{prime}"

def merge_chains_with_complement(chains, prime):
    merged_cycles = []
    used = set()

    for i, chain in enumerate(chains):
        if i in used:
            continue
        base = chain
        complement_start = get_complement(base[0][0], prime)

        for j, other in enumerate(chains):
            if i != j and complement_start in {t[0] for t in other} and j not in used:
                reordered_other = resequence_chain(other, complement_start)
                full_cycle = base + reordered_other
                merged_cycles.append(full_cycle)
                used.add(i)
                used.add(j)
                break
        else:
            merged_cycles.append(base)
            used.add(i)

    return merged_cycles

def run_modular_cycle_audit(primes):
    results = {}
    for prime in primes:
        triplets = generate_triplets(prime)
        chains = build_chains(triplets)
        cycles = merge_chains_with_complement(chains, prime)
        results[prime] = cycles
    return results

def draw_cycle(cycle, prime, cycle_index):
    n = len(cycle)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 1.0
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # Plot each node
    for i in range(n):
        label, inside, _ = cycle[i]
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        ax.text(x * 1.2, y * 1.2, label, ha='center', va='center', fontsize=10)
        ax.text(x, y, inside, ha='center', va='center', fontsize=12, weight='bold',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))
    ax.text(0, 0, str(prime), ha='center', va='center', fontsize=16, weight='bold')

    # Optional: draw chaining lines
    for i in range(n):
        x1, y1 = radius * np.cos(angles[i]), radius * np.sin(angles[i])
        x2, y2 = radius * np.cos(angles[(i + 1) % n]), radius * np.sin(angles[(i + 1) % n])
        ax.plot([x1, x2], [y1, y2], color='gray', linestyle='--', linewidth=1)

    # Save image
    total_digits = max(3, len(str(prime)))
    filename = f"{prime}_c{str(cycle_index + 1).zfill(total_digits)}.png"
    output_dir = "prime_cycle_images"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    # plt.title(f"Modular Cycle {cycle_index + 1} for Prime {prime}", fontsize=14)
    plt.savefig(filepath)
    plt.close()

def display_cycles(results):
    for prime, cycles in results.items():
        print(f"\n🔷 Prime {prime} Modular Cycles:")
        for i, cycle in enumerate(cycles, 1):
            print(f"\nCycle {i}:")
            # for triplet in cycle:
            #     print(f"  {triplet}")
            draw_cycle(cycle, prime, i - 1)


def save_prime_cycles_to_json(results, output_dir="prime_json"):
    os.makedirs(output_dir, exist_ok=True)
    for prime, cycles in results.items():
        data = {
            "prime": prime,
            "cycles": [
                [
                    {
                        "fraction": frac,
                        "first": first,
                        "next": next_,
                        "semantic_role": None,
                        "description": None
                    }
                    for frac, first, next_ in cycle
                ]
                for cycle in cycles
            ]
        }
        filename = f"{prime}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    # primes = [103, 107]
    # primes = [7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    # primes = list(primerange(5001, 6000))


    # primes = [13]  
    primes = [73 , 101  , 37 , 137 , 41 , 211 , 241 , 271 , 127 , 239 , 757 , 89 , 53 , 79 , 157 , 859 , 61 , 353 , 449 , 641 , 103 , 613 , 109]
    results = run_modular_cycle_audit(primes)
    print(results)
    save_prime_cycles_to_json(results)
    display_cycles(results)-``