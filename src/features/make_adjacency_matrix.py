import click
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import csv
from tqdm import tqdm


@click.command()
@click.argument("reviews_path", type=click.Path(exists=True))
@click.argument("output_adjacency_matrix_path", type=click.Path())
def main(reviews_path, output_adjacency_matrix_path):
    reviews = pd.read_csv(reviews_path)
    adjacency_matrix = []
    wines = reviews["wine_id"].sort_values().unique()
    for user_id in tqdm(reviews["user_id"].unique()):
        user_wines = (
            reviews[["wine_id", "rating", "variants"]]
            .where(reviews["user_id"] == user_id)
            .dropna()
        )
        result = [int(user_id)] + [None] * len(wines)
        for _, user_wine in user_wines.iterrows():
            result[int(user_wine["wine_id"]) + 1] = (
                user_wine["rating"] / user_wine["variants"]
            )

        adjacency_matrix.append(result)
    adjacency_matrix = pd.DataFrame(adjacency_matrix, columns=["user_id", *wines])
    adjacency_matrix.to_csv(output_adjacency_matrix_path, index=False)


if __name__ == "__main__":
    main()
