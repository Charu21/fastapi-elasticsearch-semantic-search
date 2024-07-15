import pandas as pd
import os

class CSVLoader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load(self) -> pd.DataFrame:
        """Load all products

            Parameters:
            product id (int): Product Id (If empty, all products will be loaded)

            Returns:
            dataframe (pd.DataFrame): Dataframe contains the products
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"{self.csv_path} does not exist")
        
        df = pd.read_csv(self.csv_path)
        return df.to_dict(orient='records')