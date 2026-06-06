import pandas as pd


class ARDSDataset:

    def __init__(self, csv_file):

        self.df = pd.read_csv(csv_file)

        self.current_index = 0

    def get_current_row(self):

        row = self.df.iloc[
            self.current_index
        ]

        self.current_index = (
            self.current_index + 1
        ) % len(self.df)

        return row