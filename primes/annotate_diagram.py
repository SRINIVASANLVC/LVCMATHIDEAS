import json
import matplotlib.pyplot as plt
import numpy as np
import os

def draw_annotated_cycle(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    prime = data["prime"]
    cycles = data["cycles"]

    for idx, cycle in enumerate(cycles):
        n = len(cycle)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        radius = 1.0

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.axis('off')

        for i, node in enumerate(cycle):
            x = radius * np.cos(angles[i])
            y = radius * np.sin(angles[i])

            label = node["semantic_role"] or node["first"]
            desc = node["description"] or node["fraction"]

            ax.text(x * 1.2, y * 1.2, label, ha='center', va='center',
                    fontsize=12, bbox=dict(facecolor='lightblue', boxstyle='round'))

            ax.text(x * 1.5, y * 1.5, desc, ha='center', va='center',
                    fontsize=10, color='gray')

            x_next = radius * np.cos(angles[(i + 1) % n])
            y_next = radius * np.sin(angles[(i + 1) % n])
            ax.plot([x, x_next], [y, y_next], color='gray', linestyle='--')

        # Center label
        ax.text(0, 0, f"Prime {prime}", ha='center', va='center',
                fontsize=14, weight='bold')

        # Save image
        output_dir = "semantic_cycle_images"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{prime}_c{str(idx + 1).zfill(3)}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath)
        plt.close()