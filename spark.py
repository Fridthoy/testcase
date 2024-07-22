import pandas as pd
from decimal import Decimal


def load_and_display_csv(url):
    """
    Load a CSV file from the provided URL and display the first few rows.
    
    Parameters:
    url (str): The URL to the CSV file.
    
    Returns:
    pandas.DataFrame: The loaded DataFrame.
    
    """
    try:
        # Load the CSV file
        df = pd.read_csv(url)
        
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# URL to the CSV file
url = "https://gist.githubusercontent.com/daggerrz/99e766b4660e3c0ed26517beaea6449a/raw/e2d3a3e42ad1895baa430612f921bc87cfff651c/orders.csv"

# Load and display the CSV file
df = load_and_display_csv(url)

#step 1
df.rename(columns={'Order Number': 'OrderID'}, inplace=True)
df['OrderID'] = df['OrderID'].astype(int)

#step 2
df['OrderDate'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1))

#step 3
df.rename(columns={'Product Number': 'ProductId'}, inplace=True)
df['ProductId'] = df['ProductId'].astype(str)

#step 4
df.rename(columns={'Product Name': 'ProductName'}, inplace=True)
df['ProductName'] = df['ProductName'].str.title().astype(str)


# #step 5
df.rename(columns={'Count': 'Quantity'}, inplace=True)
df['Quantity'] = df['Quantity'].apply(lambda x: Decimal(str(x).replace(',', '')))


# #step 6 
df['Unit'] = 'kg'
df['Unit'] = df['Unit'].astype(str)

# step 7
df = df[['OrderID', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit']]

print(df.head())