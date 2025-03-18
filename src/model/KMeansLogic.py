import sys

# Agregar la raíz del proyecto al sistema de rutas
sys.path.append("src")

import random
import pandas as pd
import numpy as np

from model.errors.KMeansError import (
    EmptyDatasetError,
    ZeroCentroidsError,
    MoreCentroidsError,
    NoNumericColumnsError,
)

# Se define una seed para el random en busca de que el comportamiento sea replicable y de esta manera sea testeable
FIXED_RANDOM_SEED = 42
FIXED_NUMPY_SEED= 32
random.seed(FIXED_RANDOM_SEED)
np.random.seed(FIXED_NUMPY_SEED)


class Kmeans:
    """
    Implementación del algoritmo K-Means Clustering.

    Atributos:
        - dataset (pd.DataFrame): Conjunto de datos a procesar.
        - num_centroids (int): Número de centroides a utilizar.
        - max_iteration (int): Número máximo de iteraciones para la optimización.
    """

    def __init__(self, dataset: pd.DataFrame, num_centroids: int, max_iteration: int) -> None:
        self.dataset = dataset
        self.num_centroids = num_centroids
        self.max_iteration = max_iteration

    def proccess_data(self) -> None:
        """
        Preprocesa el conjunto de datos:
            - Elimina filas con valores nulos.
            - Normaliza cada columna a un rango entre 0 y 1 usando Min-Max Scaling.
        """

        self.dataset = self.dataset.copy().dropna()
        for column in self.dataset.columns:
            min_value = self.dataset[column].min()
            max_value = self.dataset[column].max()
            self.dataset[column] = self.dataset[column].apply(
                lambda x: (x - min_value) / (max_value - min_value)
            )

    def calculate_euclidean_distance_between_points(
        self,
        centroids: list[tuple[float, float, float]],
        point: tuple[float, float, float],
    ) -> tuple[int, float]:
        """
        Calcula la distancia euclidiana entre un punto y todos los centroides,
        asignando el punto al centroide más cercano.

        Args:
            centroids (list): Lista de coordenadas de los centroides.
            point (tuple): Coordenadas del punto a evaluar.

        Returns:
            tuple: Índice del centroide asignado y la distancia mínima calculada.
        """

        # Calcular la suma de las diferencias al cuadrado para cada centroide
        distances = {
            i: (sum((c - p) ** 2 for c, p in zip(centroid, point)))
            for i, centroid in enumerate(centroids)
        }

        assigned_cluster, min_distance = min(
            distances.items(), key=lambda item: item[1]
        )
        return assigned_cluster, min_distance

    def calculate_centroid_probability(
        self, distances_list: list[float]
    ) -> list[float]:
        """
        Calcula la probabilidad de que un punto sea elegido como nuevo centroide,
        basada en el cuadrado de su distancia al centroide más cercano.

        Args:
            distances_list (list): Lista de distancias para cada punto.

        Returns:
            list: Probabilidades normalizadas.
        """
        distances_array = np.array(distances_list) ** 2
        sum_of_squares = np.sum(distances_array**2)
        probabilities = distances_array / sum_of_squares

        return probabilities.tolist()

    def assign_centroid_probabilities(
        self,
        centroids_list: list[tuple[float, float, float]],
        data_subset: pd.DataFrame,
    ):
        """
        Asigna a cada punto su cluster más cercano y calcula la probabilidad de
        ser seleccionado como nuevo centroide.

        Args:
            centroids_list (list): Lista actual de centroides.
            data_subset (pd.DataFrame): Subconjunto del dataset con las columnas relevantes.
        """
        distances_list = []
        cluster_list = []
        for point in data_subset.itertuples(index=False):
            key, distance = self.calculate_euclidean_distance_between_points(
                centroids_list, point
            )
            distances_list.append(distance)
            cluster_list.append(key)

        probabilities_list = self.calculate_centroid_probability(distances_list)
        self.dataset["centroid_probability"] = probabilities_list
        self.dataset["assigned_cluster"] = cluster_list

    def calculate_clusters(self, data_subset: pd.DataFrame):
        """
        Refina la asignación de clusters y actualiza los centroides iterativamente.

        Args:
            data_subset (pd.DataFrame): Subconjunto del dataset con las características relevantes.

        Returns:
            list: Lista con las nuevas coordenadas de los centroides.
        """
        for _ in range(self.max_iteration):
            # Actualizar centroides como el promedio de los puntos asignados a cada cluster
            new_centroids_df = self.dataset.groupby("assigned_cluster")[
                ["GDP_per_capita", "life_expectancy", "literacy_rate"]
            ].mean()
            centroids_list = new_centroids_df.to_records(index=False).tolist()

            # Reasignar cada punto al centroide más cercano
            assigned_clusters = []
            for point in data_subset.itertuples(index=False):
                key, _ = self.calculate_euclidean_distance_between_points(
                    centroids_list, point
                )
                assigned_clusters.append(key)

            self.dataset["assigned_cluster"] = assigned_clusters

        return (
            centroids_list
        )

    def k_means_logic(self):
        """
        Ejecuta el algoritmo completo de K-Means:
            - Valida y preprocesa los datos.
            - Inicializa el primer centroide de forma aleatoria.
            - Selecciona los centroides restantes basados en probabilidades.
            - Refina los centroides mediante iteraciones.

        Returns:
            tuple: (Lista de centroides finales, DataFrame con la asignación de clusters)
        """

        if self.dataset.empty:
            raise EmptyDatasetError()
        if not self.num_centroids:
            raise ZeroCentroidsError()

        # Verificar que todas las columnas sean numéricas
        invalid_columns = self.dataset.select_dtypes(
            exclude=["int64", "float64"]
        ).columns
        if not invalid_columns.empty:
            raise NoNumericColumnsError(invalid_columns)

        self.proccess_data()

        if self.num_centroids > self.dataset.shape[0]:
            raise MoreCentroidsError(self.num_centroids, self.dataset.shape[0])

        # Seleccionar un centroide aleatorio como inicio
        random_centroid = tuple(
            self.dataset.sample(n=1).values[0]
        ) 
        centroids_list = [random_centroid]

        relevant_columns = ["GDP_per_capita", "life_expectancy", "literacy_rate"]
        data_subset = self.dataset[
            relevant_columns
        ].copy()

        # Inicializar la asignación de probabilidades y clusters
        self.assign_centroid_probabilities(centroids_list, data_subset)

        # Seleccionar los nuevos centroides basados en la probabilidad calculada
        while len(centroids_list) < self.num_centroids:
            options = data_subset.to_records(index=False)
            weights = self.dataset["centroid_probability"].tolist()
            random_centroid = random.choices(options, weights=weights, k=1)[0]
            centroids_list.append(random_centroid)
            self.assign_centroid_probabilities(centroids_list, data_subset)

        # Refinar los centroides con iteraciones
        final_centroid = self.calculate_clusters(data_subset)

        return final_centroid, self.dataset
