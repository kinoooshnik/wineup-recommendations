import click
import logging
from pathlib import Path
import pandas as pd


def rename_me(user_id, adjacency_matrix_path, filtered_adjacency_matrix_path):
    return [1, 2, 3, 4, 5]


@click.command()
@click.argument("user_id", type=int)
@click.argument("adjacency_matrix_path", type=click.Path(exists=True))
@click.argument("filtered_adjacency_matrix_path", type=click.Path(exists=True))
@click.argument("n", type=int)
def main(user_id, adjacency_matrix_path, filtered_adjacency_matrix_path, n):
    print(rename_me(user_id, adjacency_matrix_path, filtered_adjacency_matrix_path)[:n])


if __name__ == "__main__":
    main()
