import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
import pandas as pd
import numpy as np

from src.app import clustering_logic


class TestClustering(unittest.TestCase):

    def test_normal_case_1(self):
        # Setup test data: 3 países, k = 2
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 40000],
                "life_expectancy": [78, 75, 82],
                "literacy_rate": [95, 90, 98],
            }
        )
        num_centroids = 2

        # Test de la lógica de clustering
        result = clustering_logic(dataset=dataset, num_centroids=num_centroids)

        # Verificamos que se hayan generado 2 clusters
        self.assertEqual(result["cluster"].nunique(), 2)

    def test_normal_case_2(self):
        # Setup test data: 5 países, k = 3
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 40000, 32000, 28000],
                "life_expectancy": [78, 75, 82, 80, 76],
                "literacy_rate": [95, 90, 98, 96, 92],
            }
        )
        num_centroids = 3

        result = clustering_logic(dataset=dataset, num_centroids=num_centroids)
        self.assertEqual(result["cluster"].nunique(), 3)

    def test_normal_case_3(self):
        # Setup test data: 4 países, k = 4 (cada país en un cluster único)
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 40000, 35000],
                "life_expectancy": [78, 75, 82, 79],
                "literacy_rate": [95, 90, 98, 94],
            }
        )
        num_centroids = 4

        result = clustering_logic(dataset=dataset, num_centroids=num_centroids)
        self.assertEqual(result["cluster"].nunique(), 4)
        # Verificamos que cada fila se asigne a un cluster distinto
        for cluster_label in result["cluster"].unique():
            self.assertEqual((result["cluster"] == cluster_label).sum(), 1)

    def test_extraordinary_nan_cleaning(self):
        # Setup test data: datos con NaN, que deben limpiarse
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, np.nan, 40000],
                "life_expectancy": [78, 75, 82],
                "literacy_rate": [95, 90, 98],
            }
        )
        num_centroids = 2

        # Se asume que clustering_logic limpia eliminando filas con NaN
        result = clustering_logic(dataset=dataset, num_centroids=num_centroids)

        # Tras limpiar, se deben quedar 2 filas y 2 clusters únicos
        self.assertEqual(len(result), 2)
        self.assertEqual(result["cluster"].nunique(), 2)

    def test_extraordinary_outlier(self):
        # Setup test data: datos con un outlier
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 1000000],
                "life_expectancy": [78, 75, 82],
                "literacy_rate": [95, 90, 98],
            }
        )
        num_centroids = 2

        result = clustering_logic(dataset=dataset, num_centroids=num_centroids)
        self.assertEqual(result["cluster"].nunique(), 2)

        # Verificamos que el outlier (1000000) se aísle en su propio cluster
        outlier_cluster = result.loc[
            dataset["GDP_per_capita"] == 1000000, "cluster"
        ].iloc[0]
        self.assertEqual((result["cluster"] == outlier_cluster).sum(), 1)

    def test_extraordinary_duplicates(self):
        # Setup test data: datos con entradas duplicadas
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 30000, 40000, 40000],
                "life_expectancy": [78, 78, 82, 82],
                "literacy_rate": [95, 95, 98, 98],
            }
        )
        num_centroids = 2

        result = clustering_logic(dataset=dataset, num_centroids=num_centroids)
        self.assertEqual(result["cluster"].nunique(), 2)

        # Verificamos que las filas duplicadas se asignen al mismo cluster
        group1 = result[result["GDP_per_capita"] == 30000]
        group2 = result[result["GDP_per_capita"] == 40000]
        self.assertEqual(group1["cluster"].nunique(), 1)
        self.assertEqual(group2["cluster"].nunique(), 1)


if __name__ == "__main__":
    unittest.main()
