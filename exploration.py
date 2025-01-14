from typing import List
import pandas as pd

class Exploration():
    def __init__(self, dataframe, media_vars: List[str], target_variable: str):
        self.dataframe = dataframe
        self.media_vars = media_vars
        self.target_variable = target_variable

    def check_multicollinearity(self, threshold: float = 0.65):
        dep_vars = self.dataframe[self.media_vars]
        correlation_matrix = dep_vars.corr(numeric_only=True)
        high_corr_pairs = (
            correlation_matrix
            .stack()
            .reset_index()
            .rename(columns={"level_0": "Variable_1", "level_1": "Variable_2", 0: "Correlation"})
            .query("abs(Correlation) > @threshold and Variable_1 != Variable_2")
        )

        high_corr_pairs["Pair"] = high_corr_pairs.apply(
            lambda row: tuple(sorted([row["Variable_1"], row["Variable_2"]])), axis=1
        )

        high_corr_pairs = (
            high_corr_pairs.drop_duplicates(subset="Pair")
            .drop(columns="Pair")
            .sort_values(by="Correlation", ascending=False)
            .reset_index(drop=True)
        )
        print("Highly correlated variable pairs:\n")
        print(high_corr_pairs)

    def check_correlation(self, low_threshold: float = 0.2, high_threshold: float = 0.65):
        correlation_matrix = self.dataframe.corr(numeric_only=True)

        dependent_corr = correlation_matrix[self.target_variable].drop(self.target_variable).sort_values(ascending=False)

        correlation_df = pd.DataFrame({
            "Variable": dependent_corr.index,
            "Correlation": dependent_corr.values
        })

        high_corr_df = correlation_df[correlation_df["Correlation"].abs() > high_threshold]
        low_corr_df = correlation_df[correlation_df["Correlation"].abs() < low_threshold]

        print("High Correlation Variables:")
        print(high_corr_df)

        print("\nLow Correlation Variables:")
        print(low_corr_df)
