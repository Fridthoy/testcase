import pandas as pd
from decimal import Decimal
import json
import logging

# Set up logging
logging.basicConfig(filename='data_transformation.log', level=logging.INFO)

class DataTransformer:
    def __init__(self, config_path):
        self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            self.config = json.load(file)

    def load_csv(self, url):
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            logging.error(f"Failed to load CSV: {e}")
            return None

    def rename_columns(self, df):
        try:
            df.rename(columns=self.config["columns_rename"], inplace=True)
        except Exception as e:
            logging.error(f"Failed to rename columns: {e}")

    def convert_order_id(self, df):
        try:
            df['OrderID'] = df['OrderID'].astype(int)
        except Exception as e:
            logging.error(f"Failed to convert OrderID: {e}")

    def create_order_date(self, df):
        try:
            date_columns = self.config["date_columns"]
            df[date_columns["new_date_column"]] = pd.to_datetime(df[[date_columns["Year"], date_columns["Month"], date_columns["Day"]]].astype(str).agg('-'.join, axis=1))
        except Exception as e:
            logging.error(f"Failed to create OrderDate: {e}")

    def convert_product_id(self, df):
        try:
            df['ProductId'] = df['ProductId'].astype(str)
        except Exception as e:
            logging.error(f"Failed to convert ProductId: {e}")

    def format_product_name(self, df):
        try:
            df['ProductName'] = df['ProductName'].str.title().astype(str)
        except Exception as e:
            logging.error(f"Failed to format ProductName: {e}")

    def convert_quantity(self, df):
        try:
            df['Quantity'] = df['Quantity'].apply(lambda x: Decimal(str(x).replace(',', '')))
        except Exception as e:
            logging.error(f"Failed to convert Quantity: {e}")

    def add_new_columns(self, df):
        try:
            for col, value in self.config["new_columns"].items():
                df[col] = value
                df[col] = df[col].astype(str)
        except Exception as e:
            logging.error(f"Failed to add new columns: {e}")

    def transform(self, url):
        df = self.load_csv(url)
        if df is None:
            return

        self.rename_columns(df)
        self.convert_order_id(df)
        self.create_order_date(df)
        self.convert_product_id(df)
        self.format_product_name(df)
        self.convert_quantity(df)
        self.add_new_columns(df)

        df = df[['OrderID', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit']]
        return df

# Usage
config_path = 'config.json'
url = "https://gist.githubusercontent.com/daggerrz/99e766b4660e3c0ed26517beaea6449a/raw/e2d3a3e42ad1895baa430612f921bc87cfff651c/orders.csv"

transformer = DataTransformer(config_path)
df = transformer.transform(url)
if df is not None:
    print(df.head())
