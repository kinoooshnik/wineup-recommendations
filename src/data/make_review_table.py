import click
import logging
from pathlib import Path
import pandas as pd


@click.command()
@click.argument("irecommend_path", type=click.Path(exists=True))
@click.argument("vinofan_path", type=click.Path(exists=True))
@click.argument("somelie_path", type=click.Path(exists=True))
@click.argument("output_reviews_path", type=click.Path())
def main(irecommend_path, vinofan_path, somelie_path, output_reviews_path):
    df = pd.DataFrame(
        {
            "wine_name": ["Вино 1"],
            "wine_id": [1],
            "username": ["user_1"],
            "user_id": [1],
            "rating": [4],
            "variants": [5],
            "other_wine_names": ["вино 1|Wine 1"],
        }
    )
    df.to_csv(output_reviews_path, index=False)


if __name__ == "__main__":
    main()
