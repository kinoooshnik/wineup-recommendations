import click
import logging
from pathlib import Path
import pandas as pd


@click.command()
@click.argument("adjacency_matrix_path", type=click.Path(exists=True))
@click.argument("output_filtered_adjacency_matrix_path", type=click.Path())
def main(adjacency_matrix_path, output_filtered_adjacency_matrix_path):
    df = pd.read_csv(adjacency_matrix_path)

    df["count"] = data.count(axis=1)
    df = df.drop(df[df["count"] < 4].index).drop("count", axis=1)

    df.to_csv(output_filtered_adjacency_matrix_path, index=False)


if __name__ == "__main__":
    main()
