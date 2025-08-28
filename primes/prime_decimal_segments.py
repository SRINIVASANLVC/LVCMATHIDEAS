def extract_decimal_triplets(prime):
    segment_triplets = []

    for i in range(1, prime):
        decimal_str = f"{i / prime:.10f}"  # High-precision decimal
        digits = decimal_str.split('.')[1]  # Get digits after decimal

        first_two = digits[:2]
        next_two = digits[2:4]
        fraction_label = f"{i}/{prime}"

        segment_triplets.append((fraction_label, first_two, next_two))

    print(f"Prime: {prime}")
    print("Fraction → First 2 Digits → Next 2 Digits:")
    for triplet in segment_triplets:
        print(triplet)


# Example usage
if __name__ == "__main__":
    extract_decimal_triplets(17)