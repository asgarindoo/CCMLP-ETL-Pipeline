import unittest
from unittest.mock import patch, MagicMock
import requests
from utils.extract import fetching_content, extract_data, scrape_products

class TestScraper(unittest.TestCase):
    @patch('requests.Session.get')
    def test_fetching_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'<html><body><h3 class="product-title">Test Product</h3></body></html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = 'https://testing.com'
        content = fetching_content(url)
        self.assertIsNotNone(content)
        self.assertIn(b'product-title', content)

    @patch('requests.Session.get')
    def test_fetching_content_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        url = 'https://testing.com'
        content = fetching_content(url)
        self.assertIsNone(content)

    def test_extract_data_success(self):
        product = MagicMock()
        product.find.return_value = MagicMock(get_text=MagicMock(return_value="Test Product"))
        product.find_all.return_value = [
            MagicMock(get_text=MagicMock(return_value="Rating: 3")),
            MagicMock(get_text=MagicMock(return_value="Gender: Male")),
            MagicMock(get_text=MagicMock(return_value="Colors: 3")),
            MagicMock(get_text=MagicMock(return_value="Size: M"))
        ]

        extracted_data = extract_data(product)
        extracted_data['Rating'] = extracted_data['Rating'].split(":")[-1].strip()  
        extracted_data['Colors'] = extracted_data['Colors'].split(":")[-1].strip()  

        self.assertEqual(extracted_data['Title'], 'Test Product')
        self.assertEqual(extracted_data['Rating'], '3')
        self.assertEqual(extracted_data['Gender'], 'Male')
        self.assertEqual(extracted_data['Colors'], '3')
        self.assertEqual(extracted_data['Size'], 'M')
        self.assertIn("Timestamp", extracted_data) 

    def test_extract_data_failure(self):
        product = MagicMock()
        product.find.return_value = None 
        product.find_all.return_value = [] 

        extracted_data = extract_data(product)

        self.assertEqual(extracted_data['Title'], 'Title Unavailable')
        self.assertEqual(extracted_data['Price'], 'Price Unavailable')
        self.assertEqual(extracted_data['Rating'], 'N/A')
        self.assertEqual(extracted_data['Gender'], 'N/A')
        self.assertEqual(extracted_data['Colors'], 'N/A')
        self.assertEqual(extracted_data['Size'], 'N/A')
        self.assertIn("Timestamp", extracted_data) 

    @patch('requests.Session.get')
    @patch('time.sleep')
    def test_scrape_products(self, mock_sleep, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'<html><body><div class="collection-card"><h3 class="product-title">Test Product</h3></div></body></html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        base_url = 'https://testing.com'
        mock_get.return_value = mock_response

        data = scrape_products(base_url, start_page=1, delay=2)

        self.assertEqual(len(data), 1) 
        self.assertEqual(data[0]['Title'], 'Test Product')

    @patch('requests.Session.get')
    @patch('time.sleep')
    def test_scrape_products_no_next_page(self, mock_sleep, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'<html><body><div class="collection-card"><h3 class="product-title">Test Product</h3></div></body></html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        base_url = 'https://testing.com'
        mock_get.return_value = mock_response

        data = scrape_products(base_url, start_page=1, delay=2)
        self.assertEqual(len(data), 1)

    @patch('requests.Session.get')
    @patch('time.sleep')
    def test_scrape_products_no_products(self, mock_sleep, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'<html><body>No Products Here</body></html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        base_url = 'https://testing.com'
        mock_get.return_value = mock_response

        data = scrape_products(base_url, start_page=1, delay=2)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()