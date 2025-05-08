import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append("src")

from model.kmeans_logic import Kmeans
from model.errors.kmeans_error import KmeansError

file_path = input("Ingresa la ruta del dataset: ")
num_centroids = int(input("Ingresa el numero de centrodes: "))
max_i = int(input("Ingresa las iteraciones que deseas realizar: "))


def process_file_path(file_path):
    path = Path(file_path)
    return pd.read_csv(path)


dataset = process_file_path(file_path)
filtered_dataset = dataset[["GDP_per_capita", "life_expectancy", "literacy_rate"]]

try:
    kmeans = Kmeans(filtered_dataset, num_centroids, max_i)
    centroid_centers, updated_dataset = kmeans.k_means_logic()
except KmeansError as e:
    print(str(e))
    sys.exit(1)

# Gráfico 3D de clusters
figure_3d = plt.figure(figsize=(10, 8))
axis_3d = figure_3d.add_subplot(111, projection="3d")

scatter = axis_3d.scatter(
    updated_dataset["GDP_per_capita"],
    updated_dataset["life_expectancy"],
    updated_dataset["literacy_rate"],
    c=updated_dataset["assigned_cluster"],
    cmap="viridis",
    s=100,
)

centroid_centers_np = np.array(centroid_centers)

axis_3d.scatter(
    centroid_centers_np[:, 0],
    centroid_centers_np[:, 1],
    centroid_centers_np[:, 2],
    c="blue",
    marker="X",
    s=250,
    linewidths=2,
    edgecolors="black",
)

axis_3d.set_xlabel("GDP per capita (normalizado)")
axis_3d.set_ylabel("Life expectancy (normalizado)")
axis_3d.set_zlabel("Literacy rate (normalizado)")
plt.title("Gráfico 3D de clusters")
plt.colorbar(scatter, label="Cluster")
plt.show()

# Gráficos 2D: Comparación de características y clusters
feature_names = ["GDP_per_capita", "life_expectancy", "literacy_rate"]
figure_2d, axis_2d_array = plt.subplots(1, 3, figsize=(18, 5))

feature_pairs = [
    ("GDP_per_capita", "life_expectancy"),
    ("GDP_per_capita", "literacy_rate"),
    ("life_expectancy", "literacy_rate"),
]

for axis_2d, (feature_x, feature_y) in zip(axis_2d_array, feature_pairs):
    sc = axis_2d.scatter(
        updated_dataset[feature_x],
        updated_dataset[feature_y],
        c=updated_dataset["assigned_cluster"],
        cmap="viridis",
        s=100,
    )
    axis_2d.scatter(
        centroid_centers_np[:, feature_names.index(feature_x)],
        centroid_centers_np[:, feature_names.index(feature_y)],
        c="blue",
        marker="X",
        s=250,
        linewidths=2,
        edgecolors="black",
    )
    axis_2d.set_xlabel(feature_x)
    axis_2d.set_ylabel(feature_y)
    axis_2d.grid(True)

plt.suptitle("Gráficos 2D: Comparación de características y clusters")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
