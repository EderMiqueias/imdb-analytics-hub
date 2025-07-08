from pandas import DataFrame


class DFs:
    basics_df: DataFrame
    principals_df: DataFrame
    names_df: DataFrame
    ratings_df: DataFrame

    def __init__(self, basics_df, principals_df, names_df, ratings_df):
        self.basics_df = basics_df
        self.principals_df = principals_df
        self.names_df = names_df
        self.ratings_df = ratings_df
