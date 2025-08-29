import decimal
from collections import defaultdict

decimal.getcontext().prec = 50  # High precision for repeating decimals

def generate_triplets(prime):
    triplets = []
    for i in range(1, prime):
        frac = decimal.Decimal(i) / decimal.Decimal(prime)
        digits = str(frac)[2:].ljust(4, '0')  # Skip '0.' and pad if needed
        first_two = digits[:2]
        next_two = digits[2:4]
        triplets.append((f"{i}/{prime}", first_two, next_two))
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

def merge_chains(chains, prime):
    def get_indices(chain):
        return set(int(trip[0].split('/')[0]) for trip in chain)

    merged = []
    while chains:
        base = chains.pop(0)
        base_indices = get_indices(base)
        complements_needed = {prime - i for i in base_indices if (prime - i) not in base_indices}
        merged_flag = False
        for i, other in enumerate(chains):
            other_indices = get_indices(other)
            if complements_needed & other_indices:
                base.extend(other)
                chains.pop(i)
                chains.insert(0, base)
                merged_flag = True
                break
        if not merged_flag:
            merged.append(base)
    return merged

def run_modular_cycle_audit(primes):
    results = {}
    for prime in primes:
        triplets = generate_triplets(prime)
        chains = build_chains(triplets)
        cycles = merge_chains(chains, prime)
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
    primes = [13, 17, 19]
    results = run_modular_cycle_audit(primes)
    display_cycles(results)