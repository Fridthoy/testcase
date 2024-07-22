import unittest
from main import DataTransformer

class TestDataTransformer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = 'config.json'
        cls.url = 'https://gist.githubusercontent.com/daggerrz/99e766b4660e3c0ed26517beaea6449a/raw/e2d3a3e42ad1895baa430612f921bc87cfff651c/orders.csv'
        cls.transformer = DataTransformer(cls.config_path)

    def test_load_csv(self):
        df = self.transformer.load_csv(self.url)
        self.assertIsNotNone(df)
        self.assertIn('Order Number', df.columns)

    def test_rename_columns(self):
        df = self.transformer.load_csv(self.url)
        self.transformer.rename_columns(df)
        self.assertIn('OrderID', df.columns)
        self.assertNotIn('Order Number', df.columns)

    # More tests can be added for each transformation step...

if __name__ == '__main__':
    unittest.main()



