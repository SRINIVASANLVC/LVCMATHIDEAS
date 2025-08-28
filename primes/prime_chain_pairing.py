import decimal
from collections import defaultdict

# Set precision high enough to capture at least 4 digits after decimal
decimal.getcontext().prec = 10

def extract_decimal_triplets(prime):
    triplets = []
    for i in range(1, prime):
        frac = decimal.Decimal(i) / decimal.Decimal(prime)
        digits = str(frac)[2:]  # Get digits after decimal
        digits = digits.ljust(4, '0')  # Pad if needed
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

def find_complement_pairings(chains, prime):
    pairings = []
    used = set()

    for i, chain in enumerate(chains):
        last_fraction = list(chain.keys())[-1]
        last_num = int(last_fraction.split('/')[0])
        complement = prime - last_num
        complement_key = f"{complement}/{prime}"

        for j, other_chain in enumerate(chains):
            if i != j and complement_key in other_chain and j not in used:
                pairings.append((chain, other_chain))
                used.add(i)
                used.add(j)
                break

    return pairings

def reorder_chain_by_flow(chain):
    if not chain:
        return {}

    # Start with any node
    keys = list(chain.keys())
    ordered = [keys[0]]
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

    # Reconstruct ordered chain
    return {k: chain[k] for k in ordered}

def display_chains_and_pairings(prime):
    print(f"\n🔷 Prime {prime} Modular Chains")
    triplets = extract_decimal_triplets(prime)
    chains = build_linked_chains(triplets)

    for i, chain in enumerate(chains, 1):
        print(f"\nChain {i}:")
        for k, v in chain.items():
            print(f"  {k} → {v}")

    pairings = find_complement_pairings(chains, prime)
    
    print(f"\n🔗 Complement Pairings for Prime {prime}:")
    for i, (chain1, chain2) in enumerate(pairings, 1):
        print(f"\nPair {i}:")
        print("  Chain A:")
        chain1= reorder_chain_by_flow(chain1)
        for k, v in chain1.items():
            print(f"    {k} → {v}")
        print("  Chain B:")
        chain2 = reorder_chain_by_flow(chain2)
        for k, v in chain2.items():
            print(f"    {k} → {v}")

if __name__ == "__main__":
    display_chains_and_pairings(19)
    display_chains_and_pairings(13)