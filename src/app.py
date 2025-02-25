import random
import math
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(36)


def calculate_euclidean_distance_between_points(
    centroids: list[tuple[float, float, float]], point: tuple[float, float, float]
):
    radicants_dict = {}
    for i, centroid in enumerate(centroids):
        x1, y1, z1 = centroid
        x2, y2, z2 = point
        radicant = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
        radicants_dict[i] = radicant

    key, min_radicant = min(radicants_dict.items(), key=lambda item: item[1])
    return key, math.sqrt(min_radicant)


def calculate_centroid_probability(distances_list: list[float]):
    distances_array = np.array(distances_list)
    sum_of_squares = np.sum(distances_array**2)
    probabilities = (distances_array**2) / sum_of_squares

    return probabilities.tolist()


def assign_centroid_probabilities(
    dataset: pd.DataFrame,
    centroids_list: list[tuple[float, float, float]],
    data_subset: pd.DataFrame,
):
    distances_list = []
    cluster_list = []
    for point in data_subset.itertuples(index=False):
        key, distance = calculate_euclidean_distance_between_points(
            centroids_list, point
        )
        distances_list.append(distance)
        cluster_list.append(key)

    probabilities_list = calculate_centroid_probability(distances_list)
    dataset["centroid_probability"] = probabilities_list
    dataset["assigned_cluster"] = cluster_list


def calculate_clusters(dataset: pd.DataFrame, data_subset: pd.DataFrame, max_i: int):

    for _ in range(max_i):

        new_centroids_df = dataset.groupby("assigned_cluster")[
            ["GDP_per_capita", "life_expectancy", "literacy_rate"]
        ].mean()
        centroids_list = new_centroids_df.to_records(index=False).tolist()

        assigned_clusters = []
        for point in data_subset.itertuples(index=False):
            key, _ = calculate_euclidean_distance_between_points(centroids_list, point)
            assigned_clusters.append(key)

        dataset["assigned_cluster"] = assigned_clusters

    return centroids_list


def proccess_data(dataset: pd.DataFrame):
    dataset = dataset.copy()
    dataset = dataset.dropna()
    for column in dataset.columns:
        dataset[column] = dataset[column].apply(
            lambda x: (x - dataset[column].min())
            / (dataset[column].max() - dataset[column].min())
        )
    return dataset


def k_means_logic(dataset: pd.DataFrame, num_centroids: int, max_i: int):
    dataset = proccess_data(dataset)

    random_centroid = tuple(dataset.sample(n=1).values[0])
    centroids_list = [random_centroid]

    relevant_columns = ["GDP_per_capita", "life_expectancy", "literacy_rate"]
    data_subset = dataset[relevant_columns].copy()

    assign_centroid_probabilities(dataset, centroids_list, data_subset)

    while len(centroids_list) < num_centroids:
        options = data_subset.to_records(index=False)
        weights = dataset["centroid_probability"].tolist()
        random_centroid = random.choices(options, weights=weights, k=1)[0]
        centroids_list.append(random_centroid)
        assign_centroid_probabilities(dataset, centroids_list, data_subset)

    centroid_refined = calculate_clusters(dataset, data_subset, max_i)

    return centroid_refined, dataset
