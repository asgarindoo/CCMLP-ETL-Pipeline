from utils.extract import scrape_products
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, store_to_database
import pandas as pd

def main():
    base_url = 'https://fashion-studio.dicoding.dev'
    db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/product_databases'
    data = scrape_products(base_url)
    clean_df = transform_data(data)
    
    if data:
        print(f"\nTotal produk yang berhasil diambil: {len(data)} produk\n")
        df = pd.DataFrame(data)

        print("Contoh data yang berhasil diambil:\n")
        print(df.head(2))

        print(f"\nJumlah data setelah pembersihan: {len(clean_df)} produk")
        print("\nContoh data yang sudah bersih:\n")
        print(clean_df.head(2), "\n")
        
        print(clean_df.info(),"\n")

        save_to_csv(clean_df)
        save_to_google_sheets(clean_df)
        store_to_database(clean_df, db_url)
    else:
        print("Gagal mendapatkan data produk!")

if __name__ == '__main__':
    main()
