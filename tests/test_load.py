import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine, text
from utils.load import save_to_csv, save_to_google_sheets, store_to_database

class TestLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_url = "postgresql+psycopg2://developer:supersecretpassword@localhost:5432/product_databases"
        cls.sample_data = pd.DataFrame([{
            'Title': 'Hoodie 101',
            'Price': 600000.0,
            'Rating': 3.5,
            'Colors': 6,
            'Size': 'XXL',
            'Gender': 'Unisex',
            'Timestamp': '2025-03-17T12:00:00'
        }])
        cls.engine = create_engine(cls.db_url)

    def setUp(self):
        print("\nMenyiapkan data uji...")

    def tearDown(self):
        print("Data uji selesai.")

    def test_save_to_csv(self):
        file_path = "products.csv"
        save_to_csv(self.sample_data)
        self.assertTrue(os.path.exists(file_path), "File CSV tidak dibuat.")
        loaded_data = pd.read_csv(file_path)
        self.assertEqual(len(loaded_data), len(self.sample_data), "Jumlah data dalam CSV tidak sesuai.")
        self.assertListEqual(loaded_data.columns.tolist(), self.sample_data.columns.tolist(), "Kolom CSV tidak sesuai.")

    @patch("gspread.authorize")
    def test_save_to_google_sheets(self, mock_gspread_auth):
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_gspread_auth.return_value = mock_client
        mock_client.open_by_key.return_value.sheet1 = mock_sheet
        save_to_google_sheets(self.sample_data)
        mock_sheet.clear.assert_called_once()
        mock_sheet.append_rows.assert_called_once()

    def test_store_to_database(self):
        store_to_database(self.sample_data, self.db_url)
        with self.engine.connect() as con:
            result = con.execute(text("SELECT COUNT(*) FROM product_databases WHERE \"Title\" = :title"), {'title': 'Hoodie 101'})
            count = result.scalar()

        self.assertGreater(count, 0, "Data tidak berhasil disimpan ke database")

    @classmethod
    def tearDownClass(cls):
        try:
            with cls.engine.connect() as con:
                con.execute(text('DELETE FROM product_databases WHERE "Title" = :title'), {'title': 'Hoodie 101'})
            print("\nSemua data uji berhasil dihapus.")
        except Exception as e:
            print(f"Error while cleaning up test data: {e}")
            
if __name__ == '__main__':
    unittest.main()
