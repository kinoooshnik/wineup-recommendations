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
    for user_id in tqdm(reviews["user_id"].unique()):
        result = []
        user_wines = (
            reviews[["wine_id", "rating", "variants"]]
            .where(reviews["user_id"] == user_id)
            .dropna()
        )
        for wine_id in reviews["wine_id"].sort_values().unique():
            if (
                user_wines["rating"]
                .where(user_wines["wine_id"] == wine_id)
                .dropna()
                .tolist()
            ):
                result.append(
                    user_wines["rating"]
                    .where(user_wines["wine_id"] == wine_id)
                    .dropna()
                    .tolist()
                    .pop()
                    / user_wines["variants"]
                    .where(user_wines["wine_id"] == wine_id)
                    .dropna()
                    .tolist()
                    .pop()
                )
            else:
                result.append(None)

        adjacency_matrix.append(result)
    adjacency_matrix = pd.DataFrame(
        adjacency_matrix, columns=reviews["wine_id"].sort_values().unique()
    )
    adjacency_matrix.to_csv(output_adjacency_matrix_path, index=False)


if __name__ == "__main__":
    main()
