import decimal

decimal.getcontext().prec = 10

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def extract_decimal_triplets(prime):
    triplets = []
    for i in range(1, prime):
        frac = decimal.Decimal(i) / decimal.Decimal(prime)
        digits = str(frac)[2:].ljust(4, '0')
        first_two = digits[:2]
        next_two = digits[2:4]
        triplets.append((f"{i}/{prime}", first_two, next_two))
    return triplets

def build_linked_chains(triplets):
    chains = []
    while triplets:
        chain = {}
        current = triplets.pop(0)
        fraction, first_two, next_two = current
        chain[fraction] = {'first': first_two, 'next': next_two}

        while True:
            match = next((t for t in triplets if t[1] == next_two), None)
            if match:
                triplets.remove(match)
                fraction, first_two, next_two = match
                chain[fraction] = {'first': first_two, 'next': next_two}
            else:
                break
        chains.append(chain)
    return chains

def reorder_chain_by_flow(chain, start_key=None):
    if not chain:
        return {}
    keys = list(chain.keys())
    if start_key is None or start_key not in chain:
        start_key = keys[0]
    ordered = [start_key]
    visited = set(ordered)

    while True:
        last = ordered[-1]
        next_val = chain[last]['next']
        next_key = next((k for k in chain if chain[k]['first'] == next_val and k not in visited), None)
        if next_key:
            ordered.append(next_key)
            visited.add(next_key)
        else:
            break
    return {k: chain[k] for k in ordered}

def find_complement_pairings(chains, prime):
    pairings = []
    used = set()

    for i, chain in enumerate(chains):
        if i in used:
            continue
        first_fraction = list(chain.keys())[0]
        first_num = int(first_fraction.split('/')[0])
        complement = prime - first_num
        complement_key = f"{complement}/{prime}"

        for j, other_chain in enumerate(chains):
            if i != j and complement_key in other_chain and j not in used:
                chain_a = reorder_chain_by_flow(chain, start_key=first_fraction)
                chain_b = reorder_chain_by_flow(other_chain, start_key=complement_key)
                pairings.append({'primary': chain_a, 'complement': chain_b})
                used.add(i)
                used.add(j)
                break
    return pairings

def build_nested_chain_structure(prime):
    triplets = extract_decimal_triplets(prime)
    chains = build_linked_chains(triplets)
    paired_chains = find_complement_pairings(chains, prime)
    return {
        "prime": prime,
        "paired_chains": paired_chains
    }

def run_modular_audit(start, end):
    results = []
    for p in range(start, end + 1):
        if is_prime(p):
            result = build_nested_chain_structure(p)
            results.append(result)

    for result in results:
        print(f"\n🔷 Prime {result['prime']} Paired Chains:")
        for i, pair in enumerate(result['paired_chains'], 1):
            print(f"\nPair {i}:")
            print("  Primary Chain:")
            for k, v in pair['primary'].items():
                print(f"    {k} → {v}")
            print("  Complement Chain:")
            for k, v in pair['complement'].items():
                print(f"    {k} → {v}")
    return results

# Example usage
if __name__ == "__main__":
    run_modular_audit(13, 19)