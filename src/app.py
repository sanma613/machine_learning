import pandas as pd
import random


import pandas as pd
import random


def calculate_min_max_axis(axis):
    return (axis.min(), axis.max())


def clustering_logic(dataset, num_centroids):

    min_x, max_x = calculate_min_max_axis(dataset["GDP_per_capita"])
    min_y, max_y = calculate_min_max_axis(dataset["life_expectancy"])
    min_z, max_z = calculate_min_max_axis(dataset["literacy_rate"])

    coord_list = []
    for _ in range(num_centroids):
        pt_x = random.uniform(min_x, max_x)
        pt_y = random.uniform(min_y, max_y)
        pt_z = random.uniform(min_z, max_z)
        coord = (pt_x, pt_y, pt_z)
        coord_list.append(coord)
    return coord_list


dataset = pd.DataFrame(
    {
        "GDP_per_capita": [30000, 25000, 40000],
        "life_expectancy": [78, 75, 82],
        "literacy_rate": [95, 90, 98],
    }
)


dataset = pd.DataFrame(
    {
        "GDP_per_capita": [30000, 25000, 40000],
        "life_expectancy": [78, 75, 82],
        "literacy_rate": [95, 90, 98],
    }
)

lista = clustering_logic(dataset, 3)
for item in lista:
    x, y, z = item
    print(x, y, z)
