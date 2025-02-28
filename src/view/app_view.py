import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.app.app_logic import Kmeans
from src.errors.app_error import KmeansErrors


file_path = input("Ingresa la direccion del archivo: ")
num_centroids = int(input("Ingresa el numero de centroides que deseas: "))
max_i = int(input("Ingresa el numero de iteraciones que deseas realizar: "))


def process_file_path(file_path):
    path = Path(file_path)
    dataset = pd.read_csv(path)
    return dataset


dataset = process_file_path(file_path)
filtered_dataset = dataset[["GDP_per_capita", "life_expectancy", "literacy_rate"]]
try:
    kmeans = Kmeans(filtered_dataset, num_centroids, max_i)
    centroid_centers, updated_dataset = kmeans.k_means_logic()
except KmeansErrors as e:
    print(str(e))
    sys.exit(1)


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# Graficar los datos (puntos) coloreados según su cluster asignado
scatter = ax.scatter(
    updated_dataset["GDP_per_capita"],
    updated_dataset["life_expectancy"],
    updated_dataset["literacy_rate"],
    c=updated_dataset["assigned_cluster"],
    cmap="viridis",
    s=100,
    label="Datos",
)

# Convertir la lista de centroides a array de NumPy
centroid_centers_np = np.array(centroid_centers)

# Graficar los centroides con mayor tamaño, contorno y marcador "X" en color negro
ax.scatter(
    centroid_centers_np[:, 0],
    centroid_centers_np[:, 1],
    centroid_centers_np[:, 2],
    c="black",
    marker="X",
    s=250,  # tamaño mayor para resaltar
    edgecolors="red",  # contorno rojo (puedes ajustar el color)
    linewidths=2,
    label="Centroides",
)

ax.set_xlabel("GDP per capita (normalizado)")
ax.set_ylabel("Life expectancy (normalizado)")
ax.set_zlabel("Literacy rate (normalizado)")
plt.title("3D Scatter Plot de Clusters")
plt.colorbar(scatter, label="Cluster")
ax.legend()
plt.show()

# --- GRID DE GRÁFICAS 2D (PARA CADA PAR DE CARACTERÍSTICAS) ---
# Definimos las características
features = ["GDP_per_capita", "life_expectancy", "literacy_rate"]

# Crear una figura con subplots para cada par (en este caso, 3 combinaciones)
fig2, axes = plt.subplots(1, 3, figsize=(18, 5))

# Lista de combinaciones de características
pairs = [
    ("GDP_per_capita", "life_expectancy"),
    ("GDP_per_capita", "literacy_rate"),
    ("life_expectancy", "literacy_rate"),
]

for ax, (feat_x, feat_y) in zip(axes, pairs):
    # Scatter de datos
    sc = ax.scatter(
        updated_dataset[feat_x],
        updated_dataset[feat_y],
        c=updated_dataset["assigned_cluster"],
        cmap="viridis",
        s=100,
        label="Datos",
    )
    # Graficar centroides sobre el mismo plot
    ax.scatter(
        centroid_centers_np[:, features.index(feat_x)],
        centroid_centers_np[:, features.index(feat_y)],
        c="black",
        marker="X",
        s=250,
        edgecolors="red",
        linewidths=2,
        label="Centroides",
    )
    ax.set_xlabel(feat_x)
    ax.set_ylabel(feat_y)
    ax.grid(True)
    ax.legend()

plt.suptitle("Gráficas 2D: Comparación de Características y Clusters")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
