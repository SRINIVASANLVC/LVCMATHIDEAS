import decimal
from collections import defaultdict

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

def display_cycles(results):
    for prime, cycles in results.items():
        print(f"\n🔷 Prime {prime} Modular Cycles:")
        for i, cycle in enumerate(cycles, 1):
            print(f"\nCycle {i}:")
            for triplet in cycle:
                print(f"  {triplet}")

if __name__ == "__main__":
    # primes = [103, 107]
    primes = [19, 13]
    results = run_modular_cycle_audit(primes)
    display_cycles(results)