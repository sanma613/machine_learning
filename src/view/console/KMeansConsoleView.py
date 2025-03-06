import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Agregar la raíz del proyecto al sistema de rutas
sys.path.append("src")

from model.KMeansLogic import Kmeans
from model.errors.KMeansError import KmeansError

# Obtener entrada del usuario
file_path = input("Ingresa la ruta del dataset: ")
num_centroids = int(input("Ingresa el numero de centroides: "))
max_i = int(input("Ingresa las iteraciones que deseas realizar: "))


def process_file_path(file_path):
    path = Path(file_path)
    dataset = pd.read_csv(path)
    return dataset


dataset = process_file_path(file_path)
filtered_dataset = dataset[["GDP_per_capita", "life_expectancy", "literacy_rate"]]

try:
    kmeans = Kmeans(filtered_dataset, num_centroids, max_i)
    centroid_centers, updated_dataset = kmeans.k_means_logic()
except KmeansError as e:
    print(str(e))
    sys.exit(1)

# Gráfico de dispersión 3D de los clusters
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# Graficar puntos de datos coloreados según su cluster asignado
scatter = ax.scatter(
    updated_dataset["GDP_per_capita"],
    updated_dataset["life_expectancy"],
    updated_dataset["literacy_rate"],
    c=updated_dataset["assigned_cluster"],
    cmap="viridis",
    s=100,
    label="Puntos de datos",
)

# Convertir la lista de centroides a un array de NumPy
centroid_centers_np = np.array(centroid_centers)

# Graficar los centroides con mayor tamaño, borde rojo y marcador 'X'
ax.scatter(
    centroid_centers_np[:, 0],
    centroid_centers_np[:, 1],
    centroid_centers_np[:, 2],
    c="blue",
    marker="X",
    s=250,
    linewidths=2,
    label="Centroides",
    edgecolors="black",
)

ax.set_xlabel("GDP per capita (normalizado)")
ax.set_ylabel("Life expectancy (normalizado)")
ax.set_zlabel("Literacy rate (normalizado)")
plt.title("Gráfico 3D de clusters")
plt.colorbar(scatter, label="Cluster")
ax.legend()
plt.show()

# Gráficos 2D: Comparación de características y clusters
features = ["GDP_per_capita", "life_expectancy", "literacy_rate"]
fig2, axes = plt.subplots(1, 3, figsize=(18, 5))

# Definir pares de características para la comparación
pairs = [
    ("GDP_per_capita", "life_expectancy"),
    ("GDP_per_capita", "literacy_rate"),
    ("life_expectancy", "literacy_rate"),
]

for ax, (feat_x, feat_y) in zip(axes, pairs):
    # Graficar puntos de datos
    sc = ax.scatter(
        updated_dataset[feat_x],
        updated_dataset[feat_y],
        c=updated_dataset["assigned_cluster"],
        cmap="viridis",
        s=100,
        label="Puntos de datos",
    )
    # Graficar centroides en el mismo gráfico
    ax.scatter(
        centroid_centers_np[:, features.index(feat_x)],
        centroid_centers_np[:, features.index(feat_y)],
        c="blue",
        marker="X",
        s=250,
        linewidths=2,
        label="Centroides",
        edgecolors="black",
    )
    ax.set_xlabel(feat_x)
    ax.set_ylabel(feat_y)
    ax.grid(True)
    ax.legend()

plt.suptitle("Gráficos 2D: Comparación de características y clusters")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
