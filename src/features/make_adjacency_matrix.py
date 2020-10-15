import click
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import csv


@click.command()
@click.argument("reviews_path", type=click.Path(exists=True))
@click.argument("output_adjacency_matrix_path", type=click.Path())
def main(reviews_path, output_adjacency_matrix_path):
    reviews = pd.read_csv(reviews_path)

    with open(output_adjacency_matrix_path, mode="w", encoding="utf-8") as w_file:
        for user_id in reviews["user_id"].unique():
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

            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow(result)


if __name__ == "__main__":
    main()
