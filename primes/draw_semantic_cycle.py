import matplotlib.pyplot as plt
import numpy as np
import os

def draw_semantic_cycle(ideas, central_idea, title="Semantic Cycle"):
    n = len(ideas)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 1.0

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    # Plot each idea around the circle
    for i in range(n):
        angle = angles[i]
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        ax.text(x * 1.2, y * 1.2, ideas[i], ha='center', va='center',
                fontsize=12, bbox=dict(facecolor='lightyellow', boxstyle='round'))

        # Optional: draw connecting lines
        x_next = radius * np.cos(angles[(i + 1) % n])
        y_next = radius * np.sin(angles[(i + 1) % n])
        ax.plot([x, x_next], [y, y_next], color='gray', linestyle='--')

    # Center label
    ax.text(0, 0, central_idea, ha='center', va='center',
            fontsize=14, weight='bold')

    # Save image
    output_dir = "semantic_cycle_images"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{central_idea.replace(' ', '_')}.png"
    filepath = os.path.join(output_dir, filename)
    # plt.title(title, fontsize=16)
    plt.savefig(filepath)
    plt.close()

# Example usage
central_idea = "Alchemical Octagram"
ideas = [
    "Calcination", "Dissolution", "Separation", "Conjunction",
    "Fermentation", "Distillation", "Coagulation", "Sublimation"
]

draw_semantic_cycle(ideas, central_idea)