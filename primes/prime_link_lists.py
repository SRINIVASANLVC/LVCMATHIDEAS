def extract_decimal_triplets(prime):
    triplets = []
    for i in range(1, prime):
        decimal_str = f"{i / prime:.10f}"
        digits = decimal_str.split('.')[1]
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
        chain[fraction] = first_two

        while True:
            match = next((t for t in triplets if t[1] == next_two), None)
            if match:
                triplets.remove(match)
                fraction, first_two, next_two = match
                chain[fraction] = first_two
            else:
                break

        chains.append(chain)
    return chains


if __name__ == "__main__":
    prime = 17
    triplets = extract_decimal_triplets(prime)
    chains = build_linked_chains(triplets)
    print (chains)
    print(f"\n🔗 Modular Chains for Prime {prime}:")
    for i, chain in enumerate(chains, 1):
        print(f"\nChain {i}:")
        for k, v in chain.items():
            print(f"  {k} → {v}")