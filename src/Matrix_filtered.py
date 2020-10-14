import numpy as np
import pandas as pd

data = pd.read_csv("data/processed/adjacency_matrix.csv")

data["count"] = data.count(axis=1)
data = data.drop(data[data["count"] < 4].index).drop("count", axis=1)

data.to_csv("data/processed/adjacency_matrix_filtered.csv")
