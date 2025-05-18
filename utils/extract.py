import requests
from bs4 import BeautifulSoup
import time
import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}
 
def fetching_content(url):
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None
 
def extract_data(product):
    try:
        title = product.find('h3', class_='product-title').get_text(strip=True)
        price = product.find('span', class_='price')
        price = price.get_text(strip=True) if price else 'Price Unavailable'

        details = product.find_all('p')
        data_fields = {"Rating": "N/A", "Gender": "N/A", "Colors": "N/A", "Size": "N/A"}

        for detail in details:
            text = detail.get_text(strip=True)
            if 'Rating:' in text:
                data_fields["Rating"] = text.replace('Rating:', '').replace('⭐', '').strip()
            elif 'Gender:' in text:
                data_fields["Gender"] = text.replace('Gender:', '').strip()
            elif 'Colors' in text:
                data_fields["Colors"] = text.replace('Colors', '').strip()
            elif 'Size:' in text:
                data_fields["Size"] = text.replace('Size:', '').strip()

        current_time = datetime.datetime.now().isoformat()

        return {
            "Title": title,
            "Price": price,
            **data_fields,
            "Timestamp": current_time
        }

    except Exception as e:
        print(f"failed to extract data: {e}")
        return {
            "Title": 'Title Unavailable',
            "Price": 'Price Unavailable',
            "Rating": 'N/A',
            "Gender": 'N/A',
            "Colors": 'N/A',
            "Size": 'N/A',
            "Timestamp": datetime.datetime.now().isoformat()
        }

def scrape_products(base_url, start_page=1, delay=2):
    data = []
    page_number = start_page
 
    while True:
        url = f"{base_url}/page{page_number}" if page_number > 1 else base_url
        
        print(f"Scraping halaman: {url}")
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            products = soup.find_all('div', class_='collection-card')
            for product in products:
                product_data = extract_data(product)
                if product_data:
                    data.append(product_data)
 
            next_button = soup.find("li", class_="next")
            if next_button and "disabled" not in next_button.get("class", []):
                page_number += 1
                time.sleep(delay)
            else:
                print("Scraping selesai!")
                break
        else:
            break 
 
    return data
