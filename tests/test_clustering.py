import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
import pandas as pd
import numpy as np

from src.app import k_means_logic


class TestClustering(unittest.TestCase):

    def test_normal_case_1(self):
        """
        Test Description:
        This test checks the normal scenario with 3 countries and k=2 clusters.
        It verifies that the calculated centroids (after normalization) match the expected normalized values.

        Data Setup:
        - GDP_per_capita: [30000, 25000, 40000]
        - life_expectancy: [78, 75, 82]
        - literacy_rate: [95, 90, 98]

        Expected Results (Normalized):
        Assuming min-max normalization is applied as:
          normalized = (value - min) / (max - min)
        For GDP_per_capita: min=25000, max=40000
        For life_expectancy: min=75, max=82
        For literacy_rate: min=90, max=98

        Then, for example, expected original centers:
          Center1: (40000, 82, 98)  -> normalized: (1.0, 1.0, 1.0)
          Center2: (27500, 76.5, 92.5) -> normalized: (0.16667, 0.21429, 0.31250)

        Expected number of clusters: 2
        """
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 40000],
                "life_expectancy": [78, 75, 82],
                "literacy_rate": [95, 90, 98],
            }
        )
        num_centroids = 2
        max_i = 50

        centroids_list, updated_dataset = k_means_logic(
            dataset=dataset, num_centroids=num_centroids, max_i=max_i
        )

        expected_centers = [
            (1.0, 1.0, 1.0),
            (0.16667, 0.21429, 0.31250),
        ]
        expected_num_clusters = 2

        centroids_sorted = sorted(centroids_list, key=lambda c: c[0])
        expected_sorted = sorted(expected_centers, key=lambda c: c[0])

        for res_center, exp_center in zip(centroids_sorted, expected_sorted):
            self.assertAlmostEqual(res_center[0], exp_center[0], places=2)
            self.assertAlmostEqual(res_center[1], exp_center[1], places=2)
            self.assertAlmostEqual(res_center[2], exp_center[2], places=2)

        self.assertEqual(len(centroids_list), expected_num_clusters)

    def test_normal_case_2(self):
        """
        Test Description:
        This test checks a normal scenario with 5 countries and k=3 clusters.

        Data Setup:
        - GDP_per_capita: [30000, 25000, 40000, 32000, 28000]
        - life_expectancy: [78, 75, 82, 80, 76]
        - literacy_rate: [95, 90, 98, 96, 92]

        Expected Result:
        The updated dataset should have exactly 3 unique cluster assignments in the "assigned_cluster" column.
        """
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 40000, 32000, 28000],
                "life_expectancy": [78, 75, 82, 80, 76],
                "literacy_rate": [95, 90, 98, 96, 92],
            }
        )
        num_centroids = 3
        max_i = 10

        _, updated_dataset = k_means_logic(
            dataset=dataset, num_centroids=num_centroids, max_i=max_i
        )

        self.assertEqual(updated_dataset["assigned_cluster"].nunique(), num_centroids)

    def test_normal_case_3(self):
        """
        Test Description:
        This test checks the scenario with 4 countries and k=4 clusters,
        ensuring that each country is assigned to a unique cluster.

        Data Setup:
        - GDP_per_capita: [30000, 25000, 40000, 35000]
        - life_expectancy: [78, 75, 82, 79]
        - literacy_rate: [95, 90, 98, 94]

        Expected Result:
        There should be 4 unique clusters, and each cluster should contain exactly one country.
        """
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 40000, 35000],
                "life_expectancy": [78, 75, 82, 79],
                "literacy_rate": [95, 90, 98, 94],
            }
        )
        num_centroids = 4
        max_i = 10

        centroids_list, updated_dataset = k_means_logic(
            dataset=dataset, num_centroids=num_centroids, max_i=max_i
        )

        self.assertEqual(updated_dataset["assigned_cluster"].nunique(), num_centroids)
        for cluster_label in updated_dataset["assigned_cluster"].unique():
            self.assertEqual(
                (updated_dataset["assigned_cluster"] == cluster_label).sum(), 1
            )

    def test_extraordinary_nan_cleaning(self):
        """
        Test Description:
        This test verifies that rows containing NaN values are properly handled (cleaned/dropped),
        ensuring that only valid rows are used for clustering.

        Data Setup:
        - GDP_per_capita: [30000, NaN, 40000]
        - life_expectancy: [78, 75, 82]
        - literacy_rate: [95, 90, 98]

        Expected Result:
        After cleaning, only 2 rows should remain and the "assigned_cluster" column should have exactly 2 unique clusters.
        """
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, np.nan, 40000],
                "life_expectancy": [78, 75, 82],
                "literacy_rate": [95, 90, 98],
            }
        )
        num_centroids = 2
        max_i = 10

        centroids_list, updated_dataset = k_means_logic(
            dataset=dataset, num_centroids=num_centroids, max_i=max_i
        )

        expected_centers = [(1.0, 1.0, 1.0), (0.0, 0.0, 0.0)]

        centroids_sorted = sorted(centroids_list, key=lambda c: c[0])
        expected_sorted = sorted(expected_centers, key=lambda c: c[0])

        for res_center, exp_center in zip(centroids_sorted, expected_sorted):
            self.assertAlmostEqual(res_center[0], exp_center[0], places=2)
            self.assertAlmostEqual(res_center[1], exp_center[1], places=2)
            self.assertAlmostEqual(res_center[2], exp_center[2], places=2)

        self.assertEqual(len(updated_dataset), 2)
        self.assertEqual(updated_dataset["assigned_cluster"].nunique(), num_centroids)

    def test_extraordinary_outlier(self):
        """
        Test Description:
        This test checks the handling of an outlier.
        The outlier (GDP_per_capita == 1000000) should be isolated in its own cluster.

        Data Setup:
        - GDP_per_capita: [30000, 25000, 1000000]
        - life_expectancy: [78, 75, 82]
        - literacy_rate: [95, 90, 98]

        Expected Result:
        The updated dataset should have exactly 2 unique clusters,
        and the outlier should belong to a cluster containing only that row.
        """
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 25000, 1000000],
                "life_expectancy": [78, 75, 82],
                "literacy_rate": [95, 90, 98],
            }
        )
        num_centroids = 2
        max_i = 50

        centroids_list, updated_dataset = k_means_logic(
            dataset=dataset, num_centroids=num_centroids, max_i=max_i
        )

        self.assertEqual(updated_dataset["assigned_cluster"].nunique(), num_centroids)
        # Instead of filtering by GDP_per_capita value (which may have been normalized),
        # use the original dataset index to locate the outlier row.
        outlier_idx = dataset[dataset["GDP_per_capita"] == 1000000].index[0]
        outlier_cluster = updated_dataset.loc[outlier_idx, "assigned_cluster"]
        self.assertEqual(
            (updated_dataset["assigned_cluster"] == outlier_cluster).sum(), 1
        )

    def test_extraordinary_duplicates(self):
        """
        Test Description:
        This test verifies that duplicate rows are assigned to the same cluster,
        ensuring that the clustering algorithm groups identical entries together.

        Data Setup:
        - GDP_per_capita: [30000, 30000, 40000, 40000]
        - life_expectancy: [78, 78, 82, 82]
        - literacy_rate: [95, 95, 98, 98]

        Expected Result:
        The updated dataset should have exactly 2 unique clusters.
        Duplicate rows should share the same cluster assignment.
        """
        dataset = pd.DataFrame(
            {
                "GDP_per_capita": [30000, 30000, 40000, 40000],
                "life_expectancy": [78, 78, 82, 82],
                "literacy_rate": [95, 95, 98, 98],
            }
        )
        num_centroids = 2
        max_i = 10

        centroids_list, updated_dataset = k_means_logic(
            dataset=dataset, num_centroids=num_centroids, max_i=max_i
        )

        self.assertEqual(updated_dataset["assigned_cluster"].nunique(), num_centroids)
        group1 = updated_dataset[
            updated_dataset["GDP_per_capita"] == 0.0
        ]  # Normalized value for 30000
        group2 = updated_dataset[
            updated_dataset["GDP_per_capita"] == 1.0
        ]  # Normalized value for 40000
        self.assertEqual(group1["assigned_cluster"].nunique(), 1)
        self.assertEqual(group2["assigned_cluster"].nunique(), 1)


if __name__ == "__main__":
    unittest.main()
