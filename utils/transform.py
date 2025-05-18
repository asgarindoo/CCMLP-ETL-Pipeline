import pandas as pd
def convert_price(price):
    try:
        if "$" in price:
            return float(price.replace("$", "").replace(",", "")) * 16000
        return None
    except ValueError:
        return None
def clean_data(product):
    try:
        product['Price'] = convert_price(product['Price'])

        if product['Rating'] not in ["N/A", "Invalid Rating"]:
            rating_value = product['Rating'].split('/')[0].strip()
            product['Rating'] = float(rating_value) if rating_value.replace('.', '', 1).isdigit() else None
        else:
            product['Rating'] = None
        
        product['Colors'] = pd.to_numeric(product['Colors']).astype(int)

        product['Size'] = product['Size'].replace("Size: ", "").strip() if product['Size'] else None
        product['Gender'] = product['Gender'].replace("Gender: ", "").strip() if product['Gender'] else None

        if not product['Title'] or product['Title'] == "Unknown Product":
            return None
        if product['Price'] is None or product['Rating'] is None:
            return None

        return product

    except Exception as e:
        print(f"Error cleaning data: {e}!")
        return None

def transform_data(raw_data):
    clean_products = []
    seen_titles = set()
    
    for product in raw_data:
        cleaned_product = clean_data(product)
        if cleaned_product and cleaned_product['Title'] not in seen_titles:
            clean_products.append(cleaned_product)
            seen_titles.add(cleaned_product['Title'])

    clean_df = pd.DataFrame(clean_products)
    return clean_df