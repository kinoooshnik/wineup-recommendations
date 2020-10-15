import click
import logging
from pathlib import Path
import pandas as pd


@click.command()
@click.argument("reviews_path", type=click.Path(exists=True))
@click.argument("output_adjacency_matrix_path", type=click.Path())
def main(reviews_path, output_adjacency_matrix_path):
    df = pd.DataFrame(
        {
            "user_id": [1, 2],
            "1": [1, 0],
            "2": [0.6, 0],
            "3": [1, 0],
            "4": [0.8, 0],
            "5": [0, 1],
        }
    )
    df.to_csv(output_adjacency_matrix_path, index=False)


if __name__ == "__main__":
    main()
