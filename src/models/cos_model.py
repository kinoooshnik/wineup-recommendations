import click
import logging
from pathlib import Path
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

TOP_N = 3  # number of vectors which are the most similar to user vector


def baseline_model(user_id, adjacency_matrix_path, filtered_adjacency_matrix_path):
    adjacency_matrix = pd.read_csv(
        adjacency_matrix_path
    )  # read csv file of adjacency matrix
    filtered_adjacency_matrix = pd.read_csv(
        filtered_adjacency_matrix_path
    )  # read csv file of filtered matrix
    user_vec = adjacency_matrix[
        adjacency_matrix.user_id == user_id
    ]  # find a user vector
    numpy_user_vec = user_vec.to_numpy()  # convert to numpy
    numpy_filtered_adjacency_matrix = (
        filtered_adjacency_matrix.to_numpy()
    )  # convert to numpy
    raws, columns = numpy_filtered_adjacency_matrix.shape  # shape of filtered matrix
    wine_popularity = np.zeros(
        columns - 1
    )  # array to count wine popularity, -1 because we don`t count column with user_id
    # chenging values of array from [0;1] to [-1;1]
    for i in range(raws):
        for j in range(1, columns):
            if type(numpy_filtered_adjacency_matrix[i][j]) == str:
                numpy_filtered_adjacency_matrix[i][j] = 0
            else:
                if numpy_filtered_adjacency_matrix[i][j] >= 0.5:
                    numpy_filtered_adjacency_matrix[i][j] = (
                        numpy_filtered_adjacency_matrix[i][j] * 2 - 1
                    )
                else:
                    numpy_filtered_adjacency_matrix[i][j] = (
                        -1 + numpy_filtered_adjacency_matrix[i][j] * 2
                    )
    short_filtered_matrix = np.zeros((raws, columns - 1))  # matrix without user_id
    for i in range(raws):
        for j in range(1, columns):
            short_filtered_matrix[i][j - 1] = numpy_filtered_adjacency_matrix[i][j]
    short_user_vec = numpy_user_vec[0][1:]  # user vector without user_id
    similarity_vector = cosine_similarity(
        short_user_vec.reshape(1, -1), short_filtered_matrix
    )  # measure cosine similarity between user vector and filtered_matrix
    sorted_indexes = np.argsort(similarity_vector)  # sort similarity`s vector indices
    top_n_sorted_indexes = sorted_indexes[0][::-1][
        :TOP_N
    ]  # take TOP_N vectors in descending order
    # count wine popularity
    for i in top_n_sorted_indexes:
        for j in range(len(short_filtered_matrix[i])):
            wine_popularity[j] += short_filtered_matrix[i][j]
    wine_popularity_indexes = np.argsort(
        wine_popularity
    )  # sort indexes of most popular wine
    wine_popularity_indexes += 1  # adding 1 because numbering begin from 0
    # returning descending order
    return wine_popularity_indexes[::-1]


@click.command()
@click.argument("user_id", type=int)
@click.argument("adjacency_matrix_path", type=click.Path(exists=True))
@click.argument("filtered_adjacency_matrix_path", type=click.Path(exists=True))
@click.argument("n", type=int)
def main(user_id, adjacency_matrix_path, filtered_adjacency_matrix_path, n):
    print(
        baseline_model(user_id, adjacency_matrix_path, filtered_adjacency_matrix_path)[
            :n
        ]
    )


if __name__ == "__main__":
    main()
