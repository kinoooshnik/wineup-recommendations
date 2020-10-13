import click
import logging
from pathlib import Path
import pandas as pd


@click.command()
@click.argument("adjacency_matrix_path", type=click.Path(exists=True))
@click.argument("output_filtered_adjacency_matrix_path", type=click.Path())
def main(adjacency_matrix_path, output_filtered_adjacency_matrix_path):
    df = pd.DataFrame(
        {"user_id": [1], "1": [1], "2": [0.6], "3": [1], "4": [0.8], "5": [0]}
    )
    df.to_csv(output_filtered_adjacency_matrix_path, index=False)


if __name__ == "__main__":
    main()
