from collections import defaultdict



def build_destination_dict(start_dict, direction_dict):
    destination_dict = defaultdict(set)

    for start_coord, start_ipa_set in start_dict.items():
        for start_ipa in start_ipa_set:
            for delta_coord, delta_ipa_set in direction_dict.items():
                for delta_ipa in delta_ipa_set:
                    # Compute destination coordinate
                    dest_coord = tuple(start_coord[i] + delta_coord[i] for i in range(3))

                    # Combine IPA strings
                    combined_ipa = start_ipa + delta_ipa if start_ipa != "null" else delta_ipa

                    # Add to destination dict if not already present
                    destination_dict[dest_coord].add(combined_ipa)

    return destination_dict

# Step 2: Define your starting positions (e.g., Tamil consonants or null)

start_dict = defaultdict(set)
start_dict[(0, 0, 0)].add("null")
start_dict[(1, 0, 0)].update(["y", "i"])
start_dict[(2, 0, 0)].update(["iy"])
start_dict[(0, 0, 2)].update(["uw"])
start_dict[(0, 0, 1)].update(["w", "u"])
start_dict[(0, 1, 1)].update(["aw", "o"])
start_dict[(1, 1, 0)].update(["ay", "e"])
start_dict[(1, 0, 1)].update(["iw", "uy"])
start_dict[(1, 1, 1)].update(["ew", "oy"])



direction_dict = defaultdict(set)

direction_dict[(0, 1, 0)].add("a")       # short open
direction_dict[(0, 2, 0)].add("a:")      # long open
direction_dict[(1, 0, 0)].add("i")       # short frontal
direction_dict[(2, 0, 0)].add("i:")      # long frontal
direction_dict[(0, 0, 1)].add("u")       # short rounded
direction_dict[(0, 0, 2)].add("u:")      # long rounded
direction_dict[(2, 2, 0)].add("e:")      # ā + ī
direction_dict[(0, 2, 2)].add("o:")      # ā + ū

# ✅ New entry with multiple IPA forms
direction_dict[(0, 1, 1)].update(["o", "wa"])
direction_dict[(1, 1, 0)].update(["e", "ya"])
direction_dict[(1, 0, 1)].update(["yu", "wi"])
direction_dict[(1, 1, 1)].update(["yo", "we","oi","eu","io","ue","yuwa","wiya"])


# Step 4: Invoke the function
destination_dict = build_destination_dict(start_dict, direction_dict)

# Step 5: Print the resulting destination dictionary
print("📘 Semantic Braid Map:")
for coord in sorted(destination_dict):
    ipa_set = ", ".join(sorted(destination_dict[coord]))
    print(f"  {coord}: {{{ipa_set}}}")