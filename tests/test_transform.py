import pytest
import pandas as pd
from utils.transform import convert_price, clean_data, transform_data

def test_convert_price():
    assert convert_price("$1,000") == 16000000.0
    assert convert_price("$Invalid") is None
    assert convert_price("1000") is None

def test_clean_data_valid():
    product = {
        'Title': 'Test Product',
        'Price': '$1,000',
        'Rating': '4.5/5',
        'Colors': '3',
        'Size': 'Size: M',
        'Gender': 'Gender: Male'
    }

    cleaned_product = clean_data(product)
    assert cleaned_product['Price'] == 16000000.0
    assert cleaned_product['Rating'] == 4.5
    assert cleaned_product['Colors'] == 3
    assert cleaned_product['Size'] == 'M'
    assert cleaned_product['Gender'] == 'Male'

def test_clean_data_invalid():
    product = {
        'Title': 'Test Product',
        'Price': '$Invalid',
        'Rating': 'N/A',
        'Colors': 'Invalid',
        'Size': None,
        'Gender': None
    }

    cleaned_product = clean_data(product)
    assert cleaned_product is None
    
def test_transform_data():
    raw_data = [
        {
            'Title': 'Product 1',
            'Price': '$1,000',
            'Rating': '4/5',
            'Colors': '3',
            'Size': 'Size: M',
            'Gender': 'Gender: Male'
        },
        {
            'Title': 'Product 2',
            'Price': '$500',
            'Rating': '3.5/5',
            'Colors': '5',
            'Size': 'Size: L',
            'Gender': 'Gender: Female'
        },
        {
            'Title': 'Product 3',
            'Price': '$1,500',
            'Rating': 'N/A',
            'Colors': '4',
            'Size': 'Size: S',
            'Gender': 'Gender: Male'
        }
    ]

    transformed_data = transform_data(raw_data)
    assert len(transformed_data) == 2
    assert isinstance(transformed_data, pd.DataFrame)
    assert len(transformed_data['Title'].unique()) == len(transformed_data)

def test_transform_data_duplicates():
    raw_data = [
        {
            'Title': 'Product 1',
            'Price': '$1,000',
            'Rating': '4/5',
            'Colors': '3',
            'Size': 'Size: M',
            'Gender': 'Gender: Male'
        },
        {
            'Title': 'Product 1',
            'Price': '$1,000',
            'Rating': '4/5',
            'Colors': '3',
            'Size': 'Size: M',
            'Gender': 'Gender: Male'
        }
    ]

    transformed_data = transform_data(raw_data)
    assert len(transformed_data) == 1

if __name__ == '__main__':
    pytest.main()
