import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import random
import math
import pandas as pd
import numpy as np

from src.errors.app_error import (
    EmptyDatasetError,
    ZeroCentroidsError,
    MoreCentroidsError,
    NoNumericColumnsError,
)

random.seed(42)
np.random.seed(32)


class Kmeans:

    def __init__(self, dataset: pd.DataFrame, num_centroids: int, max_i: int):
        self.dataset = dataset
        self.num_centroids = num_centroids
        self.max_i = max_i

    def proccess_data(self):
        self.dataset = self.dataset.copy()
        self.dataset = self.dataset.dropna()
        for column in self.dataset.columns:
            self.dataset[column] = self.dataset[column].apply(
                lambda x: (x - self.dataset[column].min())
                / (self.dataset[column].max() - self.dataset[column].min())
            )

    def calculate_euclidean_distance_between_points(
        self,
        centroids: list[tuple[float, float, float]],
        point: tuple[float, float, float],
    ):
        radicants_dict = {}
        for i, centroid in enumerate(centroids):
            x1, y1, z1 = centroid
            x2, y2, z2 = point
            radicant = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            radicants_dict[i] = radicant

        key, min_radicant = min(radicants_dict.items(), key=lambda item: item[1])
        return key, math.sqrt(min_radicant)

    def calculate_centroid_probability(self, distances_list: list[float]):
        distances_array = np.array(distances_list)
        sum_of_squares = np.sum(distances_array**2)
        probabilities = (distances_array**2) / sum_of_squares

        return probabilities.tolist()

    def assign_centroid_probabilities(
        self,
        centroids_list: list[tuple[float, float, float]],
        data_subset: pd.DataFrame,
    ):
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

        for _ in range(self.max_i):

            new_centroids_df = self.dataset.groupby("assigned_cluster")[
                ["GDP_per_capita", "life_expectancy", "literacy_rate"]
            ].mean()
            centroids_list = new_centroids_df.to_records(index=False).tolist()

            assigned_clusters = []
            for point in data_subset.itertuples(index=False):
                key, _ = self.calculate_euclidean_distance_between_points(
                    centroids_list, point
                )
                assigned_clusters.append(key)

            self.dataset["assigned_cluster"] = assigned_clusters

        return centroids_list

    def k_means_logic(self):
        if self.dataset.empty:
            raise EmptyDatasetError()
        if not self.num_centroids:
            raise ZeroCentroidsError()

        invalid_columns = self.dataset.select_dtypes(
            exclude=["int64", "float64"]
        ).columns
        if not invalid_columns.empty:
            raise NoNumericColumnsError(invalid_columns)

        self.proccess_data()

        if self.num_centroids > self.dataset.shape[0]:
            raise MoreCentroidsError(self.num_centroids, self.dataset.shape[0])

        random_centroid = tuple(self.dataset.sample(n=1).values[0])
        centroids_list = [random_centroid]

        relevant_columns = ["GDP_per_capita", "life_expectancy", "literacy_rate"]
        data_subset = self.dataset[relevant_columns].copy()

        self.assign_centroid_probabilities(centroids_list, data_subset)

        while len(centroids_list) < self.num_centroids:
            options = data_subset.to_records(index=False)
            weights = self.dataset["centroid_probability"].tolist()
            random_centroid = random.choices(options, weights=weights, k=1)[0]
            centroids_list.append(random_centroid)
            self.assign_centroid_probabilities(centroids_list, data_subset)

        centroid_refined = self.calculate_clusters(data_subset)

        return centroid_refined, self.dataset
