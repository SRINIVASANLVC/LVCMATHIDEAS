import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define consonant coordinates from your JSON
consonants = {
    "th": [0, 0, 0],
    "s":  [-1, 0, 0],
    "sh": [-1, 0, -1],
    "z":  [-1, -1, -1],
    "zh": [-1, -1, 0],
    "t":  [0, 0, -1],
    "d":  [0, -1, 0],
    "dh": [0, -1, -1]
}

# Define cube edges (pairs of consonant keys)
edges = [
    ("th", "s"), ("s", "sh"), ("sh", "t"), ("t", "th"),
    ("d", "dh"), ("dh", "z"), ("z", "zh"), ("zh", "d"),
    ("th", "d"), ("s", "zh"), ("sh", "z"), ("t", "dh")
]

# Plot setup
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot consonant points and labels
for label, (x, y, z) in consonants.items():
    ax.scatter(x, y, z, color='black', s=100)
    ax.text(x + 0.05, y + 0.05, z + 0.05, label, fontsize=14, ha='center', va='center', color='blue')

# Draw cube edges
for start, end in edges:
    x_vals = [consonants[start][0], consonants[end][0]]
    y_vals = [consonants[start][1], consonants[end][1]]
    z_vals = [consonants[start][2], consonants[end][2]]
    ax.plot(x_vals, y_vals, z_vals, color='gray', linewidth=1)

# Axis labels (semantic roles)
ax.set_xlabel("→ Lateralization right left (i) ", fontsize=12)
ax.set_ylabel("→  Voicing up down (a)", fontsize=12)
ax.set_zlabel(" depth in out (u)", fontsize=12)

# Set cube limits and view angle
ax.set_xlim([-1.2, 0.2])
ax.set_ylim([-1.2, 0.2])
ax.set_zlim([-1.2, 0.2])
ax.view_init(elev=30, azim=210)

plt.title("Middle-Mouth Consonant Cube", fontsize=16)
plt.tight_layout()
plt.show()